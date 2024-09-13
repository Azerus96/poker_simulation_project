# config.py

class PokerTournamentConfig:
    def __init__(self):
        self.round_duration_minutes = 15
        self.blinds_structure = {
            1: {'small_blind': 50, 'big_blind': 100, 'ante': 10},
            2: {'small_blind': 100, 'big_blind': 200, 'ante': 25},
            # Добавьте больше раундов при необходимости
        }
        self.starting_stack = 5000
        self.payout_structure = {1: 0.5, 2: 0.3, 3: 0.2}  # Призовой фонд в процентах

        # Конфигурация MCCFR
        self.mccfr_iterations = 1000  # Количество итераций для MCCFR

    def get_blinds_for_round(self, round_number):
        return self.blinds_structure.get(round_number, None)

    def get_payouts(self, prize_pool):
        return {position: prize_pool * percentage for position, percentage in self.payout_structure.items()}
