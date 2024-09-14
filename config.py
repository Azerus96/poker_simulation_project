class PokerTournamentConfig:
    def __init__(self):
        self.round_duration_minutes = 6
        self.initial_blinds_structure = {
            1: {'small_blind': 50, 'big_blind': 100, 'ante': 10},
            2: {'small_blind': 100, 'big_blind': 200, 'ante': 20},
            3: {'small_blind': 150, 'big_blind': 300, 'ante': 30},
            4: {'small_blind': 200, 'big_blind': 400, 'ante': 40},
            5: {'small_blind': 300, 'big_blind': 600, 'ante': 60},
            6: {'small_blind': 400, 'big_blind': 800, 'ante': 80},
            7: {'small_blind': 500, 'big_blind': 1000, 'ante': 100},
            8: {'small_blind': 600, 'big_blind': 1200, 'ante': 120},
            9: {'small_blind': 800, 'big_blind': 1600, 'ante': 160},
            10: {'small_blind': 1000, 'big_blind': 2000, 'ante': 200},
            11: {'small_blind': 1200, 'big_blind': 2400, 'ante': 240},
        }
        self.blinds_structure = self.initial_blinds_structure.copy()
        self.starting_stack = 10000
        self.payout_structure = {1: 0.5, 2: 0.3, 3: 0.2}
        self.additional_rounds = 0  # Для расчета общего количества добавленных раундов

    def get_blinds_for_round(self, round_number):
        """Возвращает структуру блайндов для конкретного раунда."""
        if round_number in self.blinds_structure:
            return self.blinds_structure[round_number]
        
        last_round = max(self.blinds_structure.keys())

        if round_number > last_round:
            self.additional_rounds += 1
            new_small_blind = self.blinds_structure[last_round]['small_blind'] * 2
            new_big_blind = self.blinds_structure[last_round]['big_blind'] * 2
            new_ante = self.blinds_structure[last_round]['ante'] * 2

            self.blinds_structure[round_number] = {
                'small_blind': new_small_blind,
                'big_blind': new_big_blind,
                'ante': new_ante
            }
            return self.blinds_structure[round_number]
        else:
            raise ValueError(f"Round {round_number} out of range!")

    def get_payouts(self, prize_pool):
        """Возвращает структуру выплаты на основе призового фонда."""
        return {position: prize_pool * percentage for position, percentage in self.payout_structure.items()}

    def validate_configuration(self):
        """Валидация конфигурации турнира."""
        if not self.blinds_structure or not isinstance(self.blinds_structure, dict):
            raise ValueError("Некорректная структура блайндов")
        if not isinstance(self.starting_stack, int) or self.starting_stack <= 0:
            raise ValueError("Начальный стек должен быть положительным целым числом")

    def dynamic_adjustment(self, current_round):
        """Динамическая корректировка, например, увеличение количества итераций MCCFR в поздних раундах."""
        if current_round > 5:
            self.mccfr_iterations *= 1.5  # Увеличение итераций на 50%, начиная с 6-го раунда
