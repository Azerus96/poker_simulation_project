import os
import asyncio
from flask import Flask
from config import PokerTournamentConfig
from player import PokerPlayer
from poker_game import PokerGame
from logging_system import Logger
from database import TournamentDatabase
from utils import generate_player_name

app = Flask(__name__)

@app.route('/')
def home():
    return "Tournament is running!"

def setup_tournament(num_players=160, load_previous_state=False):
    """Инициализация турнира, создание игроков и загрузка состояний, если это необходимо."""
    config = PokerTournamentConfig()
    
    players = []
    for i in range(num_players):
        player_name = generate_player_name()
        player = PokerPlayer(player_name, config.starting_stack)
        
        if load_previous_state and os.path.exists(f"{player_name}_state.pkl"):
            player.load_state(f"{player_name}_state.pkl")
        
        players.append(player)
    
    return PokerGame(players, config)

async def main():
    """Основная функция запуска турнира."""
    
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
    
    try:
        # Запуск симуляции турнира
        await game.simulate_tournament()
    
        # Сохранение данных игроков и их действий после завершения турнира
        for player in game.players:
            logger.log_event(f"{player.name} закончил игру с стеком {player.stack}")
            
            # Сохранение результатов в базу данных
            player_id = db.save_player(player)
            
            # Сохранение истории действий игрока
            for action in player.history:
                profit = player.stack - player.initial_stack
                db.save_game(player_id, action["decision"], profit)
            
            # Сохранение состояния игрока
            player.save_state()

        # Логгирование события: завершение турнира
        logger.log_event("Tournament finished")
    except Exception as e:
        # Логгирование возникновения ошибки
        logger.log_event(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Запуск Flask на порту 10000
    app.run(host="0.0.0.0", port=10000)

    # Запуск асинхронной симуляции
    asyncio.run(main())
