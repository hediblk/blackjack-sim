import random

from card import Card

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Deck:
    """A standard shoe of one or more shuffled decks."""

    def __init__(self, num_decks=6, counter=None):
        self.num_decks = num_decks
        self.counter = counter
        self._build_deck()

    def _build_deck(self):
        self.cards = [
            Card(suit, rank)
            for _ in range(self.num_decks)
            for suit in SUITS
            for rank in RANKS
        ]
        self.shuffle()
        if self.counter:
            self.counter.reset()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        """Deal one card from the shoe, reshuffling if necessary."""
        if not self.cards:
            print("Reshuffling the deck...")
            self._build_shoe()
        card = self.cards.pop()
        if self.counter:
            self.counter.record(card)
        return card
