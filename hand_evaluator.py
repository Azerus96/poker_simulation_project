# hand_evaluator.py

from collections import Counter

class HandEvaluator:
    @staticmethod
    def evaluate_hand(hand):
        values = sorted([card[0] for card in hand], reverse=True)
        is_flush = len(set(suit for _, suit in hand)) == 1
        is_straight = all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1))
        
        if is_flush and is_straight:
            return "Straight Flush", values
        if len(set(values)) == 1:
            return "Four of a Kind", values
        if is_straight:
            return "Straight", values
        if is_flush:
            return "Flush", values
        return "High Card", values

    @staticmethod
    def compare_hands(hand1, hand2):
        score1, high_card1 = HandEvaluator.evaluate_hand(hand1)
        score2, high_card2 = HandEvaluator.evaluate_hand(hand2)
        
        hand_rankings = {
            'High Card': 0,
            'One Pair': 1,
            'Two Pair': 2,
            'Three of a Kind': 3,
            'Straight': 4,
            'Flush': 5,
            'Full House': 6,
            'Four of a Kind': 7,
            'Straight Flush': 8
        }
        
        if hand_rankings[score1] > hand_rankings[score2]:
            return 1  # hand1 wins
        elif hand_rankings[score1] < hand_rankings[score2]:
            return -1  # hand2 wins
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
        best_hand = max(hands, key=HandEvaluator.evaluate_hand)
        return best_hand
