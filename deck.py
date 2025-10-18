import random

from card import Card

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Deck:
    """A standard shoe of one or more shuffled decks."""

    def __init__(self, num_decks=6):
        self.cards = [
            Card(suit, rank)
            for _ in range(num_decks)
            for suit in SUITS
            for rank in RANKS
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        """Deal one card from the shoe, reshuffling if necessary."""
        if not self.cards:
            print("Reshuffling the deck...")
            self.__init__()
        return self.cards.pop()
