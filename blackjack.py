import os

from balance_manager import BalanceManager
from card_counter import CardCounter
from deck import Deck
from hand import Hand
from database import DatabaseManager


def display_count(counter):
    if counter and counter.enabled:
        print(f"[Card Counter] Running count: {counter.get_count():+d}")


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


def play_hand(deck, player_hand, dealer_hand, bet, counter=None, initial_actions=None):
    if initial_actions is None:
        initial_actions = []

    turn_actions = player_turn(deck, player_hand, dealer_hand, counter)
    
    # combine actions for db
    all_actions_list = initial_actions + ([turn_actions] if turn_actions else [])
    actions_str = ", ".join(all_actions_list)

    if player_hand.value > 21:
        print(f"You busted with {player_hand.value}. You lose ${bet:.2f}.")
        return -bet, actions_str

    dealer_turn(deck, dealer_hand)

    print(f"\nYour hand: {player_hand} ({player_hand.value})")
    print(f"Dealer's hand: {dealer_hand} ({dealer_hand.value})")

    if dealer_hand.value > 21:
        print(f"Dealer busted with {dealer_hand.value}. You win ${bet:.2f}!")
        return bet, actions_str
    elif player_hand.value > dealer_hand.value:
        print(f"You win ${bet:.2f}!")
        return bet, actions_str
    elif player_hand.value < dealer_hand.value:
        print(f"You lose ${bet:.2f}.")
        return -bet, actions_str
    else:
        print("It's a push (tie).")
        return 0, actions_str


def player_turn(deck, player_hand, dealer_hand, counter=None):
    actions = []
    while player_hand.value < 21:
        print(f"\nYour hand: {player_hand} ({player_hand.value})")
        print(f"Dealer's showing: {dealer_hand.cards[0]}")
        display_count(counter)

        # check if player can split
        can_split = len(
            player_hand.cards) == 2 and player_hand.cards[0].rank == player_hand.cards[1].rank
        split_prompt = ", (SP)lit" if can_split else ""

        action = input(
            f"Do you want to (H)it, (S)tand{split_prompt}? ").lower()

        if action == 'h':
            actions.append("hit")
            player_hand.add_card(deck.deal())
        elif action == 's':
            actions.append("stand")
            break
        elif action == 'sp' and can_split:
            actions.append("split")
            # will be completed later
            print("split is now treated as a hit.")
            player_hand.add_card(deck.deal())
        else:
            print("Invalid action.")
    
    return ", ".join(actions)


def dealer_turn(deck, dealer_hand):

    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())


def game():
    """main game loop"""

    db = DatabaseManager()
    balance_manager = BalanceManager(db)
    counter = CardCounter()
    deck = Deck(counter=counter)

    # start game in db
    session_id = db.start_session(balance_manager.balance)

    print("Welcome to Blackjack!")
    if input("Enable card counting helper? (y/N): ").strip().lower() == 'y':
        counter.enable()
        print("Card counting enabled. Running count starts at +0.")

    while True:
        if balance_manager.balance <= 0:
            print("You've run out of money! Game over.")
            balance_manager.reset()  # reset balance
            break

        print(f"\nYour balance is ${balance_manager.balance:.2f}")

        play_again = input(
            "Press Enter to play a new hand, or type 'q' to exit: ").lower()
        if play_again == 'q':
            break

        os.system('cls' if os.name == 'nt' else 'clear')

        bet = get_bet(balance_manager.balance)

        player_hand = Hand()
        dealer_hand = Hand()
        hand_actions = []

        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        print(f"\nYour hand: {player_hand} ({player_hand.value})")
        print(f"Dealer's showing: {dealer_hand.cards[0]}")

        winnings = 0
        actions_str = ""

        # check for blackjack
        if player_hand.value == 21 and len(player_hand.cards) == 2:
            if dealer_hand.value == 21:
                print(f"Both you and the dealer have Blackjack! It's a push.")
                winnings = 0
                actions_str = "blackjack_push"
            else:
                print(f"Blackjack! You win ${bet * 1.5:.2f}!")
                winnings = bet * 1.5
                actions_str = "blackjack"
        elif dealer_hand.value == 21 and len(dealer_hand.cards) == 2:
            print(f"Dealer has Blackjack. You lose ${bet:.2f}.")
            winnings = -bet
            actions_str = "dealer_blackjack"
        else:
            # handle doubling down
            if len(player_hand.cards) == 2:
                display_count(counter)
                action_check = input(
                    "About to start your turn. (D)ouble available on first move. Type 'd' to double now or any key to continue. ").lower()
                if action_check != 'd':
                    print("Continuing without doubling down.")
                elif balance_manager.balance >= bet * 2:  # balance allows doubling down
                    bet *= 2
                    player_hand.add_card(deck.deal())
                    print(f"Bet doubled to ${bet:.2f}")
                    hand_actions.append("double")
                else:
                    print("Insufficient balance to double down.")

            winnings, actions_str = play_hand(deck, player_hand, dealer_hand, bet, counter, initial_actions=hand_actions)

        balance_manager.update(winnings)

        # add hand to db
        db.log_hand(session_id, str(player_hand), str(dealer_hand), actions_str, winnings)

    print(f"\nThanks for playing! Your final balance is ${balance_manager.balance:.2f}.")
    
    # end game in db
    db.end_session(session_id, balance_manager.balance, deck.total_dealt)
    



if __name__ == "__main__":
    game()
