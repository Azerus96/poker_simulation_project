import random
from mccfr import MCCFR
import pickle

class PokerPlayer:
    def __init__(self, name, stack, use_mccfr=True):
        self.name = name
        self.stack = stack
        self.initial_stack = stack
        self.history = []  # История действий игрока
        self.dossier = {}  # Досье на других игроков
        self.use_mccfr = use_mccfr
        
        if use_mccfr:
            self.strategy_system = MCCFR(self)
        else:
            self.strategy_system = BasicPokerStrategy()

    def make_decision(self, game_state):
        decision = self.strategy_system.decide(game_state, self.dossier)
        self.store_decision(game_state, decision)
        return decision
    
    def store_decision(self, game_state, decision):
        self.history.append({
            "game_state": game_state,
            "decision": decision
        })

    def record_opponent_action(self, opponent_name, action):
        if opponent_name not in self.dossier:
            self.dossier[opponent_name] = {"aggro": 0, "fold": 0, "call": 0, "bluff": 0}
        self.dossier[opponent_name][action] += 1

    def adjust_strategy(self):
        if self.use_mccfr:
            self.strategy_system.run_iterations(self.history)

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
