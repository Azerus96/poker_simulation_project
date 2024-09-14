import random
from collections import defaultdict

class MCCFR:
    def __init__(self, player, iterations=1000):
        self.player = player
        self.iterations = iterations
        self.strategy = defaultdict(lambda: [0, 0])  # Хранение стратегии: [регреты, кумулятивная стратегия]

    def run_iterations(self, game_history, iterations=None):
        """Запуск итераций MCCFR для улучшения стратегии."""
        if iterations is None:
            iterations = self.iterations
        
        for _ in range(iterations):
            self.run_simulation(game_history)

    def run_simulation(self, game_history):
        """Запуск симуляции по дереву решений."""
        actions = ['fold', 'call', 'raise']
        for action in actions:
            self.update_regret(game_history, action)

    def update_regret(self, game_history, action):
        """Обновление регрета для конкретного действия."""
        action_probability = self.calculate_action_probability(action)
        regret = self.calculate_regret(game_history, action)
        self.strategy[action][0] += regret  # Обновление регретов
        self.strategy[action][1] += action_probability  # Обновление кумулятивной стратегии

    def calculate_action_probability(self, action):
        """Рассчитывает вероятность выполнения действия на основе текущей стратегии."""
        cumulative = sum(max(self.strategy[a][0], 0) for a in self.strategy)
        if cumulative > 0:
            return max(self.strategy[action][0], 0) / cumulative
        return 1.0 / len(self.strategy)  # Равная вероятность для всех действий если нет регрета

    def calculate_regret(self, game_history, action):
        """Рассчитывает сожаление за выполнение данного действия в игровом контексте."""
        payoffs = self.get_payoffs_for_actions(game_history)
        expected_payoff = sum(payoffs[a] * self.calculate_action_probability(a) for a in ['fold', 'call', 'raise'])
        return payoffs[action] - expected_payoff

    def get_payoffs_for_actions(self, game_history):
        """Рассчитывает ожидаемую выгоду от различных действий на основе истории хода игры."""
        current_bet = game_history[-1]["current_bet"]
        return {
            'fold': -current_bet,
            'call': random.randint(-current_bet, current_bet),
            'raise': random.randint(current_bet, 2 * current_bet),
        }

    def decide(self, game_state, dossier):
        """Принятие решения на основе оптимизированной стратегии MCCFR."""
        self.run_iterations(game_state)
        return max(self.strategy, key=lambda x: self.strategy[x][1])  # Действие с наибольшей кумулятивной стратегией
