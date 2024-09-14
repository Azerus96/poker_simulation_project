import logging
import logging.handlers

class Logger:
    def __init__(self, log_file="tournament_log.txt", max_log_size=10*1024*1024, backup_count=5):
        """Инициализация логгера с ротацией логов."""
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_log_size, backupCount=backup_count)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def log_event(self, message):
        """Логирование стандартных событий."""
        self.logger.info(message)

    def log_decision(self, player_name, decision, game_state):
        """Логирование решений игроков."""
        current_bet = game_state.get("current_bet", 0)
        stack = game_state.get("current_player").stack if game_state.get("current_player") else "-"
        community_cards = ', '.join([f"{rank} of {suit}" for rank, suit in game_state.get("community_cards", [])])
        self.logger.debug(f"{player_name}, стек: {stack}, принимает решение {decision}, текущая ставка: {current_bet}, общие карты: {community_cards}")

    def log_result(self, winner_name, pot):
        """Логирование результатов раунда."""
        self.logger.info(f"{winner_name} выиграл банк в {pot}")

    def log_strategy(self, player_name, strategy):
        """Логирование стратегий игроков."""
        strategy_str = '; '.join(f"{action}: {prob}" for action, prob in strategy.items())
        self.logger.debug(f"{player_name} стратегия: {strategy_str}")

    def log_fold_equity(self, player_name, opponent_name, fold_equity):
        """Логирование оценки вероятности фолда."""
        self.logger.debug(f"{player_name} оценивает вероятность фолда {opponent_name} как {fold_equity:.2f}")
