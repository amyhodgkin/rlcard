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
        self.has_discarded = False
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
            if isinstance(action, tuple) and action[0] == 'meld':
                if self.has_discarded:
                    raise ValueError("Cannot meld after discarding.")
                meld_cards = action[1]
                # Validate meld legality
                if not self.is_valid_meld(meld_cards):
                    raise ValueError(f"Invalid meld: {meld_cards}")

                # Remove meld cards from player's hand
                player_hand = self.players[self.current_player].hand
                for card in meld_cards:
                    if card in player_hand:
                        player_hand.remove(card)
                    else:
                        raise ValueError(f"Player {self.current_player} does not have card {card} to meld.")

                # Add meld to player's melds
                self.players[self.current_player].melds.append(meld_cards)
                print(f"Player {self.current_player} melded: {meld_cards}")

            elif isinstance(action, tuple) and action[0] == 'add_to_meld':
                if self.has_discarded:
                    raise ValueError("Cannot add to meld after discarding.")
                meld_index = action[1]
                cards_to_add = action[2] if len(action) > 2 else []
                # Validate meld legality
                full_meld = self.players[self.current_player].melds[meld_index] + cards_to_add
                if not self.is_valid_meld(full_meld):
                    raise ValueError(f"Invalid meld after adding cards: {full_meld}")

                # Remove meld cards from player's hand
                player_hand = self.players[self.current_player].hand
                for card in cards_to_add:
                    if card in player_hand:
                        player_hand.remove(card)
                    else:
                        raise ValueError(f"Player {self.current_player} does not have card {card} to add to meld.")

                # Add meld to player's melds
                self.players[self.current_player].melds[meld_index].extend(cards_to_add)
                print(f"Player {self.current_player} added {cards_to_add} to meld {meld_index}")

            elif isinstance(action, tuple) and action[0] == 'discard':
                if self.has_discarded:
                    raise ValueError("Already discarded this turn.")
                
                card = action[1]
                if card in self.players[self.current_player].hand:
                    self.players[self.current_player].hand.remove(card)
                else:
                    raise ValueError(f"Player {self.current_player} cannot discard card: {card}, not in hand.")
                self.dealer.discard_pile.append(card)
                print(f"Player {self.current_player} discarded card: {card}")
                # advance to the next player after discarding
                self.has_discarded = True
            else:
                raise ValueError("Invalid action during discard phase. Must be a discard action.")

        #Log action
        self.history.append(action)

        if self.check_potzo(self.current_player):
            print(f"Player {self.current_player} can go to Potzo!")
            self.go_to_potzo(self.current_player)
            self.history.append(('potzo', self.current_player))

        if self.has_discarded:
            self.current_player = (self.current_player + 1) % len(self.players)
            self.phase = 'draw'
            self.has_discarded = False
        
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

    def is_wildcard(self, card):
        return card.startswith('2') or card == 'JK'
    
    def is_valid_meld(self, cards): 
        """
        Currently supports groups (e.g. ['7C', '7D', '7H']) and runs (e.g. ['5H', '6H', '7H']).
        Add wildcard logic later.
        """
        if len(cards) < 3:
            return False

        # Extract ranks and suits
        ranks = [card[0] for card in cards if card != 'JK']
        suits = [card[1] for card in cards if card != 'JK']

        jokers = [card for card in cards if card == 'JK']
        if len(jokers) > 1:
            return False
        
        # Check set: all ranks same
        if len(set(ranks)) == 1:
            return True

        # Check run: same suit, ranks consecutive
        if len(set(suits)) == 1:
            rank_order = "23456789TJQKA"
            indices = sorted(rank_order.index(r) for r in ranks)
            gaps = 0
            for i in range(len(indices) - 1):
                gap = indices[i + 1] - indices[i] - 1
                if gap < 0:
                    return False  # duplicate or out-of-order
                gaps += gap
            
            return gaps <= 1

        return False
    
    def check_potzo(self, player_id):
        """
        Check if player can go to Potzo
        Returns True if hand is empty and player hasn't gone to Potzo yet.
        """
        return not self.players[player_id].gone_to_potzo and len(self.players[player_id].hand) == 0
    
    def go_to_potzo(self, player_id):
        """
        Move player to Potzo
        """
        if not self.check_potzo(player_id):
            raise ValueError(f"Player {player_id} cannot go to Potzo, not eligible or already gone.")
        
        # asign potzo cards - first available list in potzo_cards
        potzo_cards = self.dealer.potzo_cards.pop(0)
        self.players[player_id].hand.extend(potzo_cards)
        self.players[player_id].gone_to_potzo = True

        print(f"Player {player_id} has gone to Potzo!")
    
    def is_over(self):
        # TODO: Determine if game is over
        return False

    def get_payoffs(self):
        # TODO: Return final scores for all players
        return [0, 0]
