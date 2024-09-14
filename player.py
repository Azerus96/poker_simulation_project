import random
import pickle
from mccfr import MCCFR

class PokerPlayer:
    def __init__(self, name, stack, use_mccfr=True, iterations=1000):
        self.name = name
        self.stack = stack
        self.initial_stack = stack
        self.history = []  # История действий игрока
        self.dossier = {}  # Досье на других игроков
        self.use_mccfr = use_mccfr
        
        if use_mccfr:
            self.strategy_system = MCCFR(self, iterations)  # Используем MCCFR
        else:
            self.strategy_system = BasicPokerStrategy()

    def make_decision(self, game_state):
        """Принимаем решение на основе MCCFR стратегии"""
        decision = self.strategy_system.decide(game_state, self.dossier)
        self.store_decision(game_state, decision)
        return decision
    
    def store_decision(self, game_state, decision):
        """Запоминаем принятые решения для анализа их позже"""
        self.history.append({
            "game_state": game_state,
            "decision": decision
        })

    def record_opponent_action(self, opponent_name, action):
        """Запись действия оппонентов в досье для дальнейшего анализа."""
        if opponent_name not in self.dossier:
            self.dossier[opponent_name] = {"aggro": 0, "fold": 0, "call": 0, "bluff": 0}
        self.dossier[opponent_name][action] += 1

    def adjust_strategy(self):
        """Выполнение итераций MCCFR для улучшения стратегии"""
        if self.use_mccfr:
            self.strategy_system.run_iterations(self.history)

    def estimate_fold_equity(self, opponent_name, current_bet, pot_size, stage, aggression_level=1):
        """Оценка вероятности фолда противника."""
        dossier = self.dossier.get(opponent_name, None)
        if not dossier:
            return 0  # Недостаточно данных, чтобы оценить вероятность фолда
        
        fold_rate = dossier['fold'] / sum(dossier.values()) if sum(dossier.values()) > 0 else 0
        pot_odds = current_bet / (pot_size + current_bet)

        # Агрессивность учитывается, чем выше агрессия, тем ниже вероятность фолда
        adjusted_fold_rate = fold_rate * (1 - aggression_level)
        
        # Учёт стадии игры (на ранней стадии процент фолда может быть выше)
        stage_factor = 1 - stage / 4  # Например, на ривере (_stage = 4_) stage_factor = 0
        return adjusted_fold_rate * stage_factor * pot_odds

    def save_state(self, file_name=None):
        """Сохраняем текущее состояние игрока в файл."""
        if file_name is None:
            file_name = f'{self.name}_state.pkl'
        with open(file_name, 'wb') as file:
            pickle.dump({
                "history": self.history,
                "dossier": self.dossier,
                "strategy": self.strategy_system.strategy
            }, file)

    def load_state(self, file_name):
        """Загружаем состояние игрока из файла."""
        with open(file_name, 'rb') as file:
            state = pickle.load(file)
            self.history = state["history"]
            self.dossier = state["dossier"]
            self.strategy_system.strategy = state["strategy"]

class BasicPokerStrategy:
    def decide(self, game_state, dossier):
        """Простое принятие решения на основе случайности."""
        return random.choice(['fold', 'call', 'raise'])
