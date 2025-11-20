import os


class BalanceManager:
    """Handle player balance storage and updates."""

    def __init__(self, db_manager):
        self.db = db_manager
        self.balance = self.db.get_balance()

    def update(self, winnings):
        self.balance += winnings
        self.db.update_balance(self.balance)

    def set(self, amount):
        self.balance = float(amount)
        self.db.update_balance(self.balance)

    def reset(self):
        self.set(1000.0)

