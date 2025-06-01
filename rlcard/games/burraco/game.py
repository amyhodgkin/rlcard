import random
from rlcard.games.burraco.dealer import Dealer
from rlcard.games.burraco.player import Player

class BurracoGame:
    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.players = [Player(0), Player(1)]
        self.dealer = Dealer()
        self.current_player = 0
        self.history = []

    def init_game(self):
        self.dealer.shuffle()
        self.hands = self.dealer.deal_cards(self.players)
        self.current_player = 0
        self.history = []
        return self.get_state(self.current_player), self.current_player

    def step(self, action):
        # TODO: Apply the action to the current game state
        self.history.append(action)
        self.current_player = (self.current_player + 1) % len(self.players)
        return self.get_state(self.current_player), self.current_player

    def get_state(self, player_id):
        # Return a dict describing the game state for a given player
        state = {
            'hand': self.players[player_id].hand,
            'current_player': self.current_player,
        }
        return state

    def get_legal_actions(self):
        # TODO: Return legal actions for the current player
        return ['draw', 'discard', 'meld']

    def is_over(self):
        # TODO: Determine if game is over
        return False

    def get_payoffs(self):
        # TODO: Return final scores for all players
        return [0, 0]
