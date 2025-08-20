import random
import os

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Card:
    """a single card"""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def get_value(self):
        """converts from card rank to blackjack value"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)


class Deck:
    """full card deck"""

    def __init__(self, num_decks=6):
        self.cards = [Card(suit, rank) for _ in range(num_decks)
                      for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        """pick one card from the deck"""
        if not self.cards:
            print("Reshuffling the deck...")
            self.__init__()
        return self.cards.pop()


class Hand:
    """hand of cards for player or dealer"""

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
        """change value of aces if over 21"""
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)


def get_balance():
    if os.path.exists("balance.txt"):
        with open("balance.txt", "r") as f:
            try:
                return float(f.read())
            except ValueError:
                return 1000.0
    return 1000.0


def save_balance(balance):
    with open("balance.txt", "w") as f:
        f.write(str(balance))


def get_bet(balance):
    """initial bet prompt"""
    while True:
        try:
            bet = float(input(f"Enter your bet (Balance: ${balance:.2f}): "))
            if 0 < bet <= balance:
                return bet
            else:
                print("Invalid bet amount.")
        except ValueError:
            print("Please enter a valid number.")


def play_hand(deck, player_hand, dealer_hand, bet):

    player_turn(deck, player_hand, dealer_hand)

    if player_hand.value > 21:
        print(f"You busted with {player_hand.value}. You lose ${bet:.2f}.")
        return -bet

    dealer_turn(deck, dealer_hand)

    print(f"\nYour hand: {player_hand} ({player_hand.value})")
    print(f"Dealer's hand: {dealer_hand} ({dealer_hand.value})")

    if dealer_hand.value > 21:
        print(f"Dealer busted with {dealer_hand.value}. You win ${bet:.2f}!")
        return bet
    elif player_hand.value > dealer_hand.value:
        print(f"You win ${bet:.2f}!")
        return bet
    elif player_hand.value < dealer_hand.value:
        print(f"You lose ${bet:.2f}.")
        return -bet
    else:
        print("It's a push (tie).")
        return 0


def player_turn(deck, player_hand, dealer_hand):

    while player_hand.value < 21:
        print(f"\nYour hand: {player_hand} ({player_hand.value})")
        print(f"Dealer's showing: {dealer_hand.cards[0]}")

        # check if player can split
        can_split = len(
            player_hand.cards) == 2 and player_hand.cards[0].rank == player_hand.cards[1].rank
        split_prompt = ", (S)plit" if can_split else ""

        action = input(
            f"Do you want to (H)it, (S)tand, (D)ouble{split_prompt}? ").lower()

        if action == 'h':
            player_hand.add_card(deck.deal())
        elif action == 's':
            break
        elif action == 'd':
            if len(player_hand.cards) == 2:
                player_hand.add_card(deck.deal())
                print(
                    f"You doubled down. Your new hand: {player_hand} ({player_hand.value})")
                break
            else:
                print("You can only double down on your first two cards.")
        elif action == 'p' and can_split:
            # will be completed later
            print("split is now treated as a hit.")
            player_hand.add_card(deck.deal())
        else:
            print("Invalid action.")


def dealer_turn(deck, dealer_hand):

    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())


def game():
    """main game loop"""

    balance = get_balance()
    deck = Deck()

    print("Welcome to Blackjack!")

    while True:
        if balance <= 0:
            print("You've run out of money! Game over.")
            save_balance(1000.0)  # reset balance
            break

        print(f"\nYour balance is ${balance:.2f}")

        play_again = input(
            "Press Enter to play a new hand, or type 'quit' to exit: ").lower()
        if play_again == 'quit':
            break

        os.system('cls' if os.name == 'nt' else 'clear')

        bet = get_bet(balance)

        player_hand = Hand()
        dealer_hand = Hand()

        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        print(f"\nYour hand: {player_hand} ({player_hand.value})")
        print(f"Dealer's showing: {dealer_hand.cards[0]}")

        # check for blackjack
        if player_hand.value == 21 and len(player_hand.cards) == 2:
            if dealer_hand.value == 21:
                print(f"Both you and the dealer have Blackjack! It's a push.")
                winnings = 0
            else:
                print(f"Blackjack! You win ${bet * 1.5:.2f}!")
                winnings = bet * 1.5
        elif dealer_hand.value == 21 and len(dealer_hand.cards) == 2:
            print(f"Dealer has Blackjack. You lose ${bet:.2f}.")
            winnings = -bet
        else:
            # handle doubling down
            original_bet = bet
            if len(player_hand.cards) == 2:
                action_check = input(
                    "About to start your turn. (D)ouble available on first move. Type 'd' to double now or any key to continue. ").lower()
                if action_check == 'd' and balance >= bet * 2:
                    bet *= 2
                    print(f"Bet doubled to ${bet:.2f}")
                elif action_check == 'd':
                    print("Insufficient balance to double down.")
                else:
                    print("Continuing without doubling down.")

            winnings = play_hand(deck, player_hand, dealer_hand, bet)

        balance += winnings
        save_balance(balance)

    print(f"\nThanks for playing! Your final balance is ${balance:.2f}.")
    if balance > 0:
        save_balance(balance)
    else:
        save_balance(1000)


if __name__ == "__main__":
    game()
