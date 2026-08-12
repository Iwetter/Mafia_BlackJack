import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        self.make_deck()

    def make_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["A", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "J", "Q", "K"]

        self.cards = []

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))

        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) == 0:
            self.make_deck()

        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_total(self):
        total = 0
        aces = 0

        for card in self.cards:
            total += card.get_value()
            if card.rank == "A":
                aces += 1

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def show(self):
        hand_text = ""

        for card in self.cards:
            hand_text += str(card) + ", "

        return hand_text[:-2]