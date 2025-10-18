HILO_VALUES = {
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 0,
    '8': 0,
    '9': 0,
    '10': -1,
    'J': -1,
    'Q': -1,
    'K': -1,
    'A': -1,
}


class CardCounter:
    """Tracks a running Blackjack Hi-Lo count."""

    def __init__(self, enabled=False):
        self.enabled = enabled
        self.count = 0

    def enable(self):
        self.enabled = True

    def reset(self):
        self.count = 0

    def record(self, card):
        if not self.enabled:
            return
        self.count += HILO_VALUES.get(card.rank, 0)

    def get_count(self):
        return self.count
