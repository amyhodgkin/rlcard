import random

class Dealer:
    def __init__(self):
        self.deck = [f"{rank}{suit}" for rank in "23456789TJQKA" for suit in "CDHS"] * 2  # Double deck for Burraco

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_cards(self, players):
        for player in players:
            player.hand = [self.deck.pop() for _ in range(11)]
        return [player.hand for player in players]
