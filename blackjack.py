import os

from deck import Deck
from hand import Hand


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
        split_prompt = ", (SP)lit" if can_split else ""

        action = input(
            f"Do you want to (H)it, (S)tand{split_prompt}? ").lower()

        if action == 'h':
            player_hand.add_card(deck.deal())
        elif action == 's':
            break
        elif action == 'sp' and can_split:
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
            "Press Enter to play a new hand, or type 'q' to exit: ").lower()
        if play_again == 'q':
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
            if len(player_hand.cards) == 2:
                action_check = input(
                    "About to start your turn. (D)ouble available on first move. Type 'd' to double now or any key to continue. ").lower()
                if action_check != 'd':
                    print("Continuing without doubling down.")
                elif balance >= bet * 2:  # balance allows doubling down
                    bet *= 2
                    player_hand.add_card(deck.deal())
                    print(f"Bet doubled to ${bet:.2f}")
                else:
                    print("Insufficient balance to double down.")

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
