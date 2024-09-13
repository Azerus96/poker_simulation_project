import random
from hand_evaluator import HandEvaluator
from logging_system import Logger

class PokerGame:
    def __init__(self, players, config):
        self.players = players
        self.config = config
        self.current_round = 1
        self.pot = 0
        self.tables = self.create_tables()  # Создаем несколько столов для турнира
        self.community_cards = []
        self.deck = self.create_deck()
        self.logger = Logger()

    def create_tables(self):
        """Создаем столы и распределяем игроков."""
        # Принимаем, что на каждом столе должно быть равное количество игроков
        players_per_table = 8  # В нашем примере на столе будет по 8 игроков
        num_tables = len(self.players) // players_per_table
        
        tables = []
        for i in range(num_tables):
            table = self.players[i*players_per_table:(i+1)*players_per_table]
            tables.append(table)
        return tables

    def play_round(self):
        """Симуляция раунда для каждого стола в турнире."""
        for table in self.tables:
            self.deck = self.create_deck()  # Перемешиваем колоду для каждого стола
            self.community_cards.clear()
            
            blinds = self.config.get_blinds_for_round(self.current_round)
            if not blinds:
                print(f"No blinds found for round {self.current_round}. Ending tournament.")
                return
            
            self.play_one_table(table, blinds)
        
        self.current_round += 1

        # Перераспределение игроков по столам после завершения раунда
        self.reorganize_tables()

    def play_one_table(self, table, blinds):
        """Игра на одном столе с заданными блайндами."""
        self.collect_blinds(table, blinds)
        self.deal_hole_cards(table)

        self.conduct_betting_round(table, "Pre-Flop")
        self.deck.pop()  # Burn card

        self.deal_community_cards(3)
        self.conduct_betting_round(table, "Flop")
        self.deck.pop()  # Burn card

        self.deal_community_cards(1)
        self.conduct_betting_round(table, "Turn")
        self.deck.pop()  # Burn card

        self.deal_community_cards(1)
        self.conduct_betting_round(table, "River")

        winner = self.showdown(table)
        if winner:
            self.award_pot_to_winner(winner)

    def collect_blinds(self, table, blinds):
        """Собираем блайнды для конкретного стола."""
        small_blind, big_blind = blinds['small_blind'], blinds['big_blind']
        table[0].stack -= small_blind  
        table[1].stack -= big_blind
        self.pot += small_blind + big_blind

        self.logger.log_event(f"{table[0].name} posts small blind of {small_blind}")
        self.logger.log_event(f"{table[1].name} posts big blind of {big_blind}")

    def deal_hole_cards(self, table):
        """Раздаем карманные карты каждому игроку на столе."""
        for player in table:
            player.hole_cards = [self.deck.pop(), self.deck.pop()]
            self.logger.log_event(f"{player.name} receives hole cards {player.hole_cards}")

    def conduct_betting_round(self, table, stage):
        """Проводим круг ставок для каждого игрока на этом столе."""
        for player in table:
            game_state = {
                "current_bet": random.randint(10, 100),  # Пример текущей ставки
                "current_player": player,
                "community_cards": self.community_cards
            }
            decision = player.make_decision(game_state)
            self.logger.log_decision(player.name, decision, game_state)
            
            if decision == "call":
                self.pot += game_state["current_bet"]
            elif decision == "raise":
                raise_amount = random.randint(10, 100)
                self.pot += raise_amount

    def showdown(self, table):
        """Определение победителя на конкретном столе."""
        hands = {player.name: player.hole_cards + self.community_cards for player in table}
        best_hand = None
        best_player = None
        for player_name, cards in hands.items():
            hand_rank, hand_value = HandEvaluator.evaluate_hand(cards)
            self.logger.log_event(f"{player_name} has {hand_rank} with {cards}")

            if not best_hand or HandEvaluator.compare_hands(cards, best_hand) == 1:
                best_hand = cards
                best_player = player_name

        if best_player:
            self.logger.log_event(f"{best_player} wins the round.")
            return best_player
        return None

    def award_pot_to_winner(self, winner):
        """Переводит выигрыш в стек победителя."""
        winner.stack += self.pot
        self.logger.log_result(winner.name, self.pot)
        self.pot = 0

    def reorganize_tables(self):
        """Перераспределяем игроков по столам после каждого раунда."""
        self.players = [player for table in self.tables for player in table if player.stack > 0]
        
        # Если игроков стало меньше чем 8, объединяем столы
        self.tables = self.create_tables()
        
        if len(self.players) <= 8:
            self.tables = [self.players]

    def simulate_tournament(self):
        """Запускаем симуляцию турнира и продолжаем до тех пор, пока не останется один победитель."""
        while len(self.players) > 1 and self.current_round <= len(self.config.blinds_structure):
            self.play_round()

        if len(self.players) == 1:
            self.logger.log_event(f"The tournament winner is {self.players[0].name} with a stack of {self.players[0].stack}")
        else:
            self.logger.log_event("Tournament ended with multiple players still in the game.")

# Пример использования класса:
if __name__ == "__main__":
    from config import PokerTournamentConfig
    from player import PokerPlayer
    from utils import generate_player_name

    config = PokerTournamentConfig()
    players = [PokerPlayer(generate_player_name(), config.starting_stack) for _ in range(160)]
    game = PokerGame(players, config)
    game.simulate_tournament()
