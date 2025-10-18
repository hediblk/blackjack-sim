import os


class BalanceManager:
    """Handle player balance storage and updates."""

    def __init__(self, filepath="balance.txt", default=1000.0):
        self.filepath = filepath
        self.default = default
        self.balance = self._load_balance()

    def _load_balance(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as fh:
                try:
                    return float(fh.read())
                except ValueError:
                    pass
        self._write_balance(self.default)
        return self.default

    def _write_balance(self, amount):
        with open(self.filepath, "w") as fh:
            fh.write(f"{amount}")

    def update(self, winnings):
        self.balance += winnings
        self._write_balance(self.balance)

    def set(self, amount):
        self.balance = float(amount)
        self._write_balance(self.balance)

    def reset(self):
        self.set(self.default)

    def save(self):
        self._write_balance(self.balance)
