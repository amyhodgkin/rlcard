import random

class Dealer:
    def __init__(self):
        self.full_deck = [f"{rank}{suit}" for rank in "23456789TJQKA" for suit in "CDHS"] * 2  # Double deck for Burraco
        self.full_deck += ['JK'] * 4  # Add 4 jokers for double deck
        self.draw_pile = []
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.full_deck)
        self.draw_pile = self.full_deck.copy()


    def deal_cards(self, players):
        # Deal 11 cards to each player  
        # - improvement split and deal like in real game
        for player in players:
            player.hand = [self.draw_pile.pop() for _ in range(11)]
        # Start the discard pile with one card from the draw pile
        self.discard_pile.append(self.draw_pile.pop())

        self.potzo_cards = [
            [self.draw_pile.pop() for _ in range(11)],
            [self.draw_pile.pop() for _ in range(11)]
        ]

        return [player.hand for player in players]
