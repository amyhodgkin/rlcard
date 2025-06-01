import random
from rlcard.games.burraco.dealer import Dealer
from rlcard.games.burraco.player import Player

class BurracoGame:
    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.players = [Player(0), Player(1)]
        self.dealer = Dealer()
        self.current_player = 0
        self.phase = 'draw'
        self.history = []

    def init_game(self):
        self.dealer.shuffle()
        self.hands = self.dealer.deal_cards(self.players)
        self.current_player = 0
        self.history = []
        return self.get_state(self.current_player), self.current_player

    def step(self, action):
        # TODO: Apply the action to the current game state
        if self.phase == 'draw':
            if action == 'draw_pile':
                card = self.dealer.draw_pile.pop()
                self.players[self.current_player].hand.append(card)
                print(f"Player {self.current_player} drew card from deck")
                self.phase = 'discard'
            elif action == 'pickup_discard':
                if self.dealer.discard_pile:
                    self.players[self.current_player].hand.extend(self.dealer.discard_pile)
                    self.dealer.discard_pile.clear()
                    print(f"Player {self.current_player} picked up the discard pile. ")
                    self.phase = 'discard'
                else:
                    raise ValueError("Discard pile is empty, cannot pick up.")
            elif isinstance(action, tuple) and action[0] == 'discard':
                raise ValueError("Must draw a card before discarding.")
        elif self.phase == 'discard':
            if isinstance(action, tuple) and action[0] == 'discard':
                card = action[1]
                if card in self.players[self.current_player].hand:
                    self.players[self.current_player].hand.remove(card)
                else:
                    raise ValueError(f"Player {self.current_player} cannot discard card: {card}, not in hand.")
                self.dealer.discard_pile.append(card)
                print(f"Player {self.current_player} discarded card: {card}")
                # advance to the next player after discarding
                self.current_player = (self.current_player + 1) % len(self.players)
                self.phase = 'draw'
            else:
                raise ValueError("Invalid action during discard phase. Must be a discard action.")

        self.history.append(action)
        
        
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
        return ['draw']#, 'discard', 'meld']

    def is_over(self):
        # TODO: Determine if game is over
        return False

    def get_payoffs(self):
        # TODO: Return final scores for all players
        return [0, 0]
