# logging_system.py

import logging
import os

class Logger:
    def __init__(self, log_file="tournament_log.txt"):
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def log_event(self, message):
        self.logger.info(message)

    def log_decision(self, player_name, decision, game_state):
        self.logger.debug(f"{player_name} decided to {decision} with state: {game_state}")

    def log_result(self, winner_name, pot):
        self.logger.info(f"{winner_name} won the pot of {pot}")

# Пример использования логгера
if __name__ == "__main__":
    logger = Logger()
    logger.log_event("Tournament started.")
