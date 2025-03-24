import os 
os.system("clear")

from operator import itemgetter
from collections import defaultdict

RESULT = ["Loss", "Tie", "Win"]

SUITS = {
    'S': ('Spades', 1),
    'H': ('Hearts', 1),
    'D': ('Diamonds', 1),
    'C': ('Clubs', 1)
}

RANKS = {
    'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 11, 'Q': 12, 'K': 13
}

class PokerHand:
    #Represents a Poker Hand and allows comparison with another hand
    def __init__(self, hand):
        #Initialise a poker hand from a string of 5 cards.
        hand = hand.replace(' ', '').upper()  # Remove spaces & standardise case
        self.vals = [c for c in hand if c in RANKS.keys()]
        self.suits = [c for c in hand if c in SUITS.keys()]
        self.hand = sorted([RANKS[c] for c in self.vals], reverse=True)
        self.val_cnt = defaultdict(int)

        for card in self.vals:
            self.val_cnt[card] += 1
        self._total_value = self._total_value()

    def _total_value(self):
        #Return a tuple representing hand value and high card values
        if self._is_five_high_straight:
            del self.hand[0]
            self.hand.append(1)
        if self._hand_value in [1, 4]:
            sorted_d = sorted(self.val_cnt.items(), reverse=True)
            return (self._hand_value, sorted_d[0][0], tuple(self.hand))
        return (self._hand_value, tuple(self.hand))

    @property
    def _is_five_high_straight(self):
        return sum(self.hand) == 28

    @property
    def _is_straight(self):
        """Check if hand is a straight."""
        if self._is_five_high_straight:
            return True
        previous_card = self.hand[-1] - 1
        for card in sorted(self.hand):
            if previous_card + 1 != card:
                return False
            previous_card = card
        return True

    @property
    def _is_flush(self):
        """Check if hand is a flush."""
        return len(set(self.suits)) == 1

    @property
    def _hand_value(self):
        """Return the hand rank based on poker rules."""
        hand_value = 0
        if len(set(self.val_cnt.values())) > 1:
            sorted_d = sorted(self.val_cnt.values(), reverse=True)
            if sorted_d[0] == 2 and sorted_d[1] == 2:
                return 3  # Two pair
            for pair_plus in sorted_d:
                if pair_plus == 1:
                    return hand_value
                elif pair_plus == 4:
                    return 8  # Four of a kind
                elif pair_plus == 3:
                    hand_value = 4  # Three of a kind
                elif pair_plus == 2:
                    return 7 if hand_value == 4 else 1  # Full house or One pair
        if self._is_straight:
            return 9 if self._is_flush else 5  # Straight flush or Straight
        if self._is_flush:
            return 6  # Flush
        return hand_value

    def compare_with(self, other):
        #Compare two poker hands and return the result
        if self._total_value > other._total_value:
            return "Player 1 Wins!"
        elif self._total_value < other._total_value:
            return "Player 2 Wins!"
        else:
            return "It's a Tie!"

# Get input from user
player1_hand = input("Please insert Player 1's cards (e.g., '2H 3D 5S 9C JC'): ").strip()
player2_hand = input("Please insert Player 2's cards (e.g., '2D 3H 5C 9H JD'): ").strip()

# Convert inputs into PokerHand objects
hand1 = PokerHand(player1_hand)
hand2 = PokerHand(player2_hand)

# Compare hands and print result
print("\nResult:", hand1.compare_with(hand2))
