class Hand:
    """Hand of cards for a player or dealer."""

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.get_value()
        if card.rank == 'A':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        """Adjust ace values when the hand would otherwise bust."""
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
