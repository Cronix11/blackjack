import itertools
import random
import math
from time import sleep

VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
SUITS = ["♠", "♥", "♦", "♣"]
DEALER_STAND = 18  # Dealer stands on 18 or higher
BLACKJACK_MULTIPLIER = 2.5  # Blackjack pays 2.5x


class card:
    def __init__(self, value, suit):
        self.suit = suit
        self.val = value

    def __repr__(self):
        return f"{self.val}{self.suit}"

    def value(self):
        if self.val in ['J', 'Q', 'K']:
            return 10
        elif self.val == 'A':
            return 11
        else:
            return self.val

# The shoe is a collection of decks


class shoe:
    def __init__(self, no_of_decks):
        self.cards = []
        for _ in range(no_of_decks):
            for c in [card(value, suit) for value, suit in itertools.product(VALUES, SUITS)]:
                self.cards.append(c)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)


class player:
    def __init__(self, name: str, balance: int):
        self.bal = int(balance)
        self.name = name
        self.hand = []

    def bet(self, amount):
        if self.bal < amount or amount < 500:
            return False
        else:
            self.bal -= amount
            return True

    def deposit(self, amount):
        self.bal += amount

    def get_balance(self):
        return self.bal

    def get_hand(self):
        return self.hand

    def get_name(self):
        return self.name

    def clear_hand(self):
        self.hand = []

    def get_hand_value(self):
        value = sum([card.value() for card in self.hand])
        aces = sum(card.val == 'A' for card in self.hand)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def take(self, card):
        self.hand.append(card)


def play_game():
    # The 'deck' is a collection of some number of decks
    deck = shoe(8)

    player1 = player('You', 10000)
    dealer = player('Dealer', 100_000_000)

    print("Players balance:", player1.get_balance())

    while player1.get_balance() > 0:
        play_hand(dealer, player1, deck)
        player1.clear_hand()
        dealer.clear_hand()
        if player1.get_balance() > 1_000_000:
            print('You win')
            return
    print('You went bankrupt...')
    return


def print_hands(player1, player2):
    print(f"{player1.get_name()}: {player1.get_hand()} (Value {player1.get_hand_value()})")
    print(f"{player2.get_name()}: {player2.get_hand()} (Value {player2.get_hand_value()})")
    print()


def play_hand(dealer, player1, deck):
    bet_amount = -1
    while not player1.bet(bet_amount):
        bet_amount = int(input(
            f"Place your bet (Current balance {player1.get_balance()}):"))
    player1.take(deck.draw())
    player1.take(deck.draw())
    dealer.take(deck.draw())

    print(f"You have {player1.get_hand()}. (Value {player1.get_hand_value()})")
    if player1.get_hand_value() == 21:
        player1.deposit(math.round(bet_amount * BLACKJACK_MULTIPLIER))
        print('Blackjack!')
        return True
    print(f"Dealer has {dealer.get_hand()}. (Value {dealer.get_hand_value()})")
    while player1.get_hand_value() <= 21:
        hit = True if input(
            f"Hit or Stand? (h/s):") == 'h' else False
        if hit:
            player1.take(deck.draw())
            print_hands(player1, dealer)
            continue
        else:
            while dealer.get_hand_value() < DEALER_STAND:
                sleep(0.5)
                dealer.take(deck.draw())
                print_hands(player1, dealer)
            if dealer.get_hand_value() > 21:
                print('Dealer Busted')
                player1.deposit(bet_amount*2)
                return True
            if dealer.get_hand_value() > player1.get_hand_value():
                print('You lose.')
                return False
            if dealer.get_hand_value() == player1.get_hand_value():
                print('Push.')
                player1.deposit(bet_amount)
                return None
            else:
                print('You win!')
                player1.deposit(bet_amount * 2)
                return True
    print('Busted!')
    return False


if __name__ == '__main__':
    play_game()
