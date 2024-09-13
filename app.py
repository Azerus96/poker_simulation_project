from config import PokerTournamentConfig
from player import PokerPlayer
from poker_game import PokerGame
from logging_system import Logger
from database import TournamentDatabase
from utils import generate_player_name
import os

def setup_tournament(num_players=160, load_previous_state=False):
    # Инициализация конфигурации турнира
    config = PokerTournamentConfig()
    
    # Создаем игроков с уникальными именами и распределяем стартовый стек
    players = []
    for i in range(num_players):
        player_name = generate_player_name()
        player = PokerPlayer(player_name, config.starting_stack)
        
        # Загрузить предыдущее состояние, если необходимо
        if load_previous_state and os.path.exists(f"{player_name}_state.pkl"):
            player.load_state(f"{player_name}_state.pkl")
        
        players.append(player)
    
    return PokerGame(players, config)

def main():
    num_players = 160  # Настройка количества игроков

    # Инициализация базы данных для хранения результатов
    db = TournamentDatabase()
    
    # Инициализация логгера для ведения журнала событий
    logger = Logger()
    
    # Настройка и запуск турнира
    load_previous_state = False  # Задайте True, если хотите загружать состояние
    game = setup_tournament(num_players, load_previous_state)
    
    # Логгирование события: старт турнира
    logger.log_event("Tournament started")
    
    # Запуск симуляции турнира
    game.simulate_tournament()
    
    # Сохранение данных игроков и их действий после завершения турнира
    for player in game.players:
        logger.log_event(f"{player.name} ended the game with a stack of {player.stack}")
        
        # Сохраняем результаты игрока в базу данных
        player_id = db.save_player(player)
        
        # Сохраняем действия игрока (историю)
        for action in player.history:
            profit = player.stack - player.initial_stack
            db.save_game(player_id, action["decision"], profit)
        
        # Сохранение состояния игрока
        player.save_state()

    # Логгирование события: завершение турнира
    logger.log_event("Tournament finished")

if __name__ == "__main__":
    main()
