import random
import asyncio
import pickle
from logging_system import Logger
from hand_evaluator import HandEvaluator

class PokerGame:
    def __init__(self, players, config):
        self.players = players
        self.config = config
        self.current_round = 1
        self.pot = 0
        self.tables = self.create_tables()  # Создание нескольких столов для турнира
        self.community_cards = []
        self.deck = self.create_deck()  # Создание и перемешивание колоды
        self.logger = Logger()

    def create_tables(self):
        """Создание столов и рассадка игроков."""
        players_per_table = 8
        num_tables = len(self.players) // players_per_table
        
        tables = []
        for i in range(num_tables):
            table = self.players[i * players_per_table:(i + 1) * players_per_table]
            tables.append(table)
        return tables

    def create_deck(self):
        """Создание и перемешивание новой колоды карт."""
        ranks = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        deck = [(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def deal_hole_cards(self, table):
        """Раздача по две карты каждому игроку за столом."""
        for player in table:
            player.hole_cards = [self.deck.pop(), self.deck.pop()]
            self.logger.log_event(f"{player.name} получает карманные карты {player.hole_cards}")

    def deal_community_cards(self, number):
        """Выдача указанного количества общих карт (флоп, терн, ривер)."""
        for _ in range(number):
            card = self.deck.pop()
            self.community_cards.append(card)
            self.logger.log_event(f"Сдана общая карта: {card}")

    async def play_one_table(self, table, blinds):
        """Игра за одним столом с заданными блайндами."""
        self.collect_blinds(table, blinds)
        self.deal_hole_cards(table)

        await self.conduct_betting_round(table, "Pre-Flop")
        self.deck.pop()  # "Сжигание" карты

        # Флоп: выдача 3 общих карт
        self.deal_community_cards(3)
        await self.conduct_betting_round(table, "Flop")
        self.deck.pop()  # Burn card

        # Терн: выдача 1 общей карты
        self.deal_community_cards(1)
        await self.conduct_betting_round(table, "Turn")
        self.deck.pop()  # Burn card

        # Ривер: выдача 1 общей карты
        self.deal_community_cards(1)
        await self.conduct_betting_round(table, "River")

        winner = self.showdown(table)
        if winner:
            self.award_pot_to_winner(winner)

    def collect_blinds(self, table, blinds):
        """Сбор блайндов для конкретного стола."""
        small_blind, big_blind = blinds['small_blind'], blinds['big_blind']
        table[0].stack -= small_blind  
        table[1].stack -= big_blind
        self.pot += small_blind + big_blind

        self.logger.log_event(f"{table[0].name} поставил маленький блайнд {small_blind}")
        self.logger.log_event(f"{table[1].name} поставил большой блайнд {big_blind}")

    async def conduct_betting_round(self, table, stage):
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
            
            await asyncio.sleep(0)  # Асинхронность
            
    def showdown(self, table):
        """Определение победителя на конкретном столе."""
        hands = {player: player.hole_cards + self.community_cards for player in table}
        
        best_hand_value = None
        best_player = None

        for player, hand in hands.items():
            hand_value = HandEvaluator.evaluate_hand(hand)
            self.logger.log_event(f"{player.name} имеет {hand_value[0]} с {self.format_hand(hand)}")

            if not best_hand_value or HandEvaluator.compare_hands(hand, best_hand_value[1]) > 0:
                best_hand_value = (player, hand)

        if best_hand_value:
            best_player = best_hand_value[0]
            self.logger.log_event(f"{best_player.name} выиграл с {HandEvaluator.evaluate_hand(best_hand_value[1])[0]}")

        return best_player
    
    def award_pot_to_winner(self, winner):
        """Переводит выигрыш в стек победителя."""
        winner.stack += self.pot
        self.logger.log_result(winner.name, self.pot)
        self.pot = 0

    def reorganize_tables(self):
        """Перераспределение игроков по столам после каждого раунда."""
        self.players = [player for table in self.tables for player in table if player.stack > 0]
        
        if len(self.players) <= 8:
            self.tables = [self.players]
        else:
            self.tables = self.create_tables()

    def save_game(self, file_name):
        """Сохранение текущего состояния игры."""
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_game(file_name):
        """Загрузка сохраненного состояния игры."""
        with open(file_name, 'rb') as f:
            return pickle.load(f)

    def simulate_tournament(self):
        """Запуск симуляции турнира, продолжаем до тех пор, пока не останется один победитель."""
        while len(self.players) > 1:
            self.play_round()
            self.current_round += 1

        if len(self.players) == 1:
            self.logger.log_event(f"The tournament winner is {self.players[0].name} with a stack of {self.players[0].stack}")
        else:
            self.logger.log_event("Tournament ended with multiple players still in the game.")

    def play_round(self):
        """Игровой процесс одного раунда."""
        self.deck = self.create_deck()
        blinds = self.config.get_blinds_for_round(self.current_round)
        
        for table in self.tables:
            asyncio.run(self.play_one_table(table, blinds))

        self.reorganize_tables()

    @staticmethod
    def format_hand(hand):
        """Форматирование списка карт для удобного отображения."""
        return ', '.join([f"{rank} of {suit}" for rank, suit in hand])
