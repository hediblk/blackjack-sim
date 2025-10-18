class Card:
    """Represents a single playing card."""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def get_value(self):
        """Return the blackjack value for this card."""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)
