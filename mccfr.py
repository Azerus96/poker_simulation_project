# mccfr.py

import random
from collections import defaultdict

class MCCFR:
    def __init__(self, player, iterations=1000):
        self.player = player
        self.iterations = iterations
        self.strategy = defaultdict(lambda: [0, 0])  # Хранение стратегии: [регреты, кумулятивная стратегия]

    def run_iterations(self, game_history):
        """Запускает итерации MCCFR для улучшения стратегии."""
        for _ in range(self.iterations):
            self.run_simulation(game_history)

    def run_simulation(self, game_history):
        """Запуск симуляции по дереву решений."""
        for action in ['fold', 'call', 'raise']:
            self.update_regret(game_history, action)

    def update_regret(self, game_history, action):
        action_probability = self.calculate_action_probability(action)
        regret = self.calculate_regret(game_history, action)
        self.strategy[action][0] += regret  # Обновление регретов
        self.strategy[action][1] += action_probability  # Обновление стратегии

    def calculate_action_probability(self, action):
        """Рассчитывает вероятность выполнения данного действия на основе текущей стратегии."""
        cumulative = sum(max(self.strategy[a][0], 0) for a in self.strategy)
        if cumulative > 0:
            return max(self.strategy[action][0], 0) / cumulative
        return 1.0 / len(self.strategy)

    def calculate_regret(self, game_history, action):
        """Рассчитывает сожаление за выполнение данного действия в игровом контексте."""
        payoffs = self.get_payoffs_for_actions(game_history)
        expected_payoff = sum(payoffs[a] * self.calculate_action_probability(a) for a in ['fold', 'call', 'raise'])
        return payoffs[action] - expected_payoff

    def get_payoffs_for_actions(self, game_history):
        """Рассчитывает ожидаемую выгоду от различных действий на базе истории хода игры."""
        # Примерный расчет на основе ставки
        return {
            'fold': -game_history[-1]["current_bet"],
            'call': random.randint(-game_history[-1]["current_bet"], game_history[-1]["current_bet"]),
            'raise': random.randint(1, 2 * game_history[-1]["current_bet"]),
        }

    def decide(self, game_state, dossier):
        """Принятие решения на основе оптимизированной стратегии."""
        self.run_iterations(game_state)
        return max(self.strategy, key=lambda x: self.strategy[x][1])  # Действие с наибольшей общей стратегией
