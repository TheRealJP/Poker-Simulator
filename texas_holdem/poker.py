from random import shuffle
import sys


class Player(object):
    def __init__(self, username: str):
        self.username = username
        ''' The name of this player. '''

        self.hand = []
        ''' A list of cards (2) representing this player's hand.'''

        self.chips = 0

    def bid(self, amount):
        if amount < self.chips:
            print("You don't have enough chips to bid " + amount)
        else:
            self.chips -= amount
        return self.chips


class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        return 1

    def __str__(self):
        switch = {
            0: "spades",  # '♠',
            1: "hearts",  # '♡',
            2: "diamonds",  # '♢',
            3: "clubs"  # '♣'
        }
        card_value = {
            1: "A",
            11: "J",
            12: "Q",
            13: "K"
        }
        if self.value != 1 and self.value <= 10:
            value = str(self.value)
            suit = switch.get(self.suit, "Invalid suit")
            return "[" + value + " of " + suit + "]"
        else:
            value = str(card_value.get(self.value, "0"))
            suit = switch.get(self.suit, "Invalid suit")
            return "[" + value + " of " + suit + "]"


class Deck(object):
    def __init__(self):
        # Total cards in deck.
        self.cards_facedown = []
        # Array of cards currently in play.
        self.cards_active = []

        # Populate the deck with every combination of suit/values
        for suit in range(4):
            for value in range(1, 14):
                card = Card(suit, value)
                self.cards_facedown.append(card)

    def shuffle(self):
        ''' Shuffles the position of the cards in the deck. '''

        self.cards_facedown.extend(self.cards_active)
        self.cards_active = []
        shuffle(self.cards_facedown)

        # Return amount of cards remaining in deck
    def cards_left(self):
        return len(self.cards_facedown)


class Poker:
    def __init__(self):
        self.deck = Deck()
        self.players = []

    def start(self, players):
        # Ensure there is just enough people to play
        if len(players) < 2 or len(players) > 10:
            sys.exit("Insufficient players. Must be between 2 and 10 players")
        else:
            self.players = players

    def fold(self, player):
        ''' To fold is to discard a player's cards. In this instance, we'll
         just return them back into the deck.'''
        self.deck.cards_facedown.extend(player.hand)
        player.hand = []

    def distribute_cards(self):
        # check if there are enough cards for each player
        if (len(self.players) * 2) > self.deck.cards_left():
            print("Not enough cards in the deck.")
            return False
        else:
            # hand each player two cards from the deck
            for i in range(2):
                for player in self.players:
                    card = self.deck.cards_facedown.pop(i)
                    print(player.username +
                          " is being handed a card: " + str(card))
                    player.hand.append(card)

    def find_royal_flush(self, cards: []) -> bool:
        last_suit = cards[0].suit
        sum = 0
        for card in cards:
            if card.value < 10 and card.value != 1:
                return False
            if last_suit != card.suit:
                return False
            else:
                sum += card.value
        return sum == 47

    def find_straight_flush(self, cards: []) -> bool:
        last_suit = cards[0].suit

        sorted_cards = sorted(cards, key=lambda card: card.value)
        for i in range(len(sorted_cards)-1):
            if sorted_cards[i+1].value - 1 != sorted_cards[i].value:
                return False
            elif sorted_cards[i].suit != last_suit:
                return False
        return True

    def find_four_of_a_kind(self, cards) -> bool:
        pair = 0
        matches = 0
        sample_size = int((len(cards)/2)-1)
        for i in range(sample_size):
            if cards[i].value == cards[i].value:
                pair = cards[i].value
                break
        for card in cards:
            if card.value == pair:
                matches += 1
        return matches == 4

    # def findFullHouse(self):

    # def findFlush(self):

    # def findStraight(self):

    # def findThreeOfAKind(self):

    # def findTwoPairs(self):

    # def findPair(self):

    # def findHighCard(self, cards):
