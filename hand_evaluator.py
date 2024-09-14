from collections import Counter
from functools import lru_cache

class HandEvaluator:
    @staticmethod
    @lru_cache(maxsize=None)
    def evaluate_hand(hand):
        """Оценивает комбинацию у игрока и возвращает название комбинации и ранжированные значения карт."""
        values = sorted([HandEvaluator.rank_to_value(card[0]) for card in hand], reverse=True)
        is_flush = len(set(suit for _, suit in hand)) == 1
        is_straight = HandEvaluator.is_straight(values)
        
        if is_flush and is_straight:
            return "Straight Flush", values
        elif HandEvaluator.is_four_of_a_kind(values):
            return "Four of a Kind", values
        elif HandEvaluator.is_full_house(values):
            return "Full House", values
        elif is_flush:
            return "Flush", values
        elif is_straight:
            return "Straight", values
        elif HandEvaluator.is_three_of_a_kind(values):
            return "Three of a Kind", values
        elif HandEvaluator.is_two_pair(values):
            return "Two Pair", values
        elif HandEvaluator.is_one_pair(values):
            return "One Pair", values
        else:
            return "High Card", values

    @staticmethod
    def compare_hands(hand1, hand2):
        """Сравнивает две руки, возвращает 1, если первая рука лучше, -1 если вторая рука лучше, иначе 0 (ничья)."""
        score1, high_card1 = HandEvaluator.evaluate_hand(hand1)
        score2, high_card2 = HandEvaluator.evaluate_hand(hand2)

        hand_rankings = [
            'High Card', 'One Pair', 'Two Pair', 'Three of a Kind', 'Straight', 
            'Flush', 'Full House', 'Four of a Kind', 'Straight Flush'
        ]
        
        if hand_rankings.index(score1) > hand_rankings.index(score2):
            return 1  # hand1 выигрывает
        elif hand_rankings.index(score1) < hand_rankings.index(score2):
            return -1  # hand2 выигрывает
        else:
            # Сравниваем старшие карты
            for hc1, hc2 in zip(high_card1, high_card2):
                if hc1 > hc2:
                    return 1
                elif hc1 < hc2:
                    return -1
            return 0  # Ничья

    @staticmethod
    def determine_winner(hands):
        """Определяет победителя среди списка рук."""
        if not hands:
            return None

        best_hand = hands[0]
        for next_hand in hands[1:]:
            if HandEvaluator.compare_hands(next_hand, best_hand) > 0:
                best_hand = next_hand
        
        return best_hand

    ####### Вспомогательные методы #######

    @staticmethod
    def rank_to_value(rank):
        """Преобразует ранг карты в числовое значение для удобства оценки."""
        rank_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return int(rank) if rank.isdigit() else rank_values.get(rank, rank)

    @staticmethod
    def is_straight(values):
        """Проверяет, является ли набор карт стритом."""
        return all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1))

    @staticmethod
    def is_four_of_a_kind(values):
        """Проверяет, содержит ли рука каре (4 карты одного ранга)."""
        return 4 in Counter(values).values()

    @staticmethod
    def is_full_house(values):
        """Проверяет, является ли рука фул-хаусом."""
        value_counts = Counter(values).values()
        return 3 in value_counts and 2 in value_counts

    @staticmethod
    def is_three_of_a_kind(values):
        """Проверяет, содержит ли рука сет (3 карты одного ранга)."""
        return 3 in Counter(values).values()

    @staticmethod
    def is_two_pair(values):
        """Проверяет, содержит ли рука две пары."""
        value_counts = Counter(values).values()
        return list(value_counts).count(2) == 2

    @staticmethod
    def is_one_pair(values):
        """Проверяет, содержит ли рука одну пару."""
        return 2 in Counter(values).values()

    @staticmethod
    def estimate_hand_strength(hand, community_cards):
        """Оценка силы руки относительно всех возможных рук противника."""
        better_hands, worse_hands, tie_hands = 0, 0, 0
        all_possible_hands = HandEvaluator.generate_possible_hands(community_cards)

        player_best_hand = HandEvaluator.evaluate_hand(hand + community_cards)
        for opponent_hand in all_possible_hands:
            opponent_best_hand = HandEvaluator.evaluate_hand(opponent_hand)

            result = HandEvaluator.compare_hands(player_best_hand, opponent_best_hand)
            if result == 1:
                better_hands += 1
            elif result == -1:
                worse_hands += 1
            else:
                tie_hands += 1

        total_hands = better_hands + worse_hands + tie_hands
        return better_hands / total_hands if total_hands > 0 else 0

    @staticmethod
    def generate_possible_hands(community_cards):
        """Генерация всех возможных комбинаций рук оппонентов."""
        deck = [(rank, suit) for suit in ['hearts', 'diamonds', 'clubs', 'spades'] 
                for rank in list(range(2, 11)) + ['J', 'Q', 'K', 'A']]
        for card in community_cards:
            if card in deck:
                deck.remove(card)

        possible_hands = []
        for i in range(len(deck)):
            for j in range(i + 1, len(deck)):
                possible_hands.append([deck[i], deck[j]])
        
        return possible_hands
