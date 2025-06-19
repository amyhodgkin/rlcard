import random
from rlcard.games.burraco.dealer import Dealer
from rlcard.games.burraco.player import Player

class BurracoGame:
    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.dealer = Dealer()
        self.current_player = 0
        self.phase = 'draw'
        self.has_discarded = False
        self.game_over = False
        self.history = []

    def init_game(self):
        self.dealer.shuffle()
        self.dealer.deal_cards(self.players) 
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
                # Check remaining cards in hand
                if not self.check_can_meld(meld_cards):
                    raise ValueError("Cannot meld, not enough valid cards left in hand ")
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
                # Validate meld only leads to end game if valid
                # Check remaining cards in hand
                if not self.check_can_meld(cards_to_add):
                    raise ValueError("Cannot meld, not enough valid cards left in hand ")
                
                # Validate meld legality
                full_meld = self.players[self.current_player].melds[meld_index] + cards_to_add
                if not self.is_valid_meld(full_meld):
                    raise ValueError(f"Invalid meld after adding cards: {full_meld}")

                # Remove meld cards from player's hand
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
            # check if game ends
            if self.check_end_game():
                self.game_over = True
                print(f"Player {self.current_player} has won the game!")
                return self.get_state(self.current_player), self.current_player, True
            self.current_player = (self.current_player + 1) % len(self.players)
            self.phase = 'draw'
            self.has_discarded = False
        
        return self.get_state(self.current_player), self.current_player, False

    def get_state(self, player_id):
        # Return a dict describing the game state for a given player
        state = {
            'hand': self.players[player_id].hand,
            'current_player': self.current_player,
            'game_over': self.game_over,
        }
        return state

    def get_legal_actions(self):
        # TODO: Return legal actions for the current player
        return ['draw', 'discard', 'meld']

    def is_valid_meld(self, cards):
        
        if len(cards) < 3:
            return False

        if self._is_valid_set(cards):
            return True

        if self._is_valid_run(cards):
            return True

        return False 
    
    def _is_valid_set(self, cards):

        jokers = [c for c in cards if c == 'JK']
        twos = [c for c in cards if c[0] == '2']
        normal_cards = [c for c in cards if c not in jokers + twos]
        
        if not normal_cards:
            return False

        # Check set: all ranks same (ignoring jokers/twos acting as wildcards) - cant have meld of only jokers or twos
        ranks = [c[0] for c in normal_cards]
        if len(set(ranks)) == 1:
            # If all ranks are the same and only one wildcard, it's valid
            if len(jokers) + len(twos) <= 1:
                return True
            
        return False
    
    def _is_valid_run(self, cards):
        rank_order = "A23456789TJQKA"  # Note: Ace low and high
        
        jokers = [c for c in cards if c == 'JK']
        twos = [c for c in cards if c[0] == '2']
        normal_cards = [c for c in cards if c not in jokers + twos]

        if not normal_cards:
            return False
        
        n_wildcards = len(jokers) + len(twos)
        # Check run assuming 2s are natural cards (if they fit)
        ranks = [c[0] for c in normal_cards]
        suits = [c[1] for c in normal_cards]
        two_suits = [c[1] for c in twos]
        
        if len(set(suits)) != 1:
            return False 
        
        if suits[0] in two_suits:
            # add one two to the ranks and remove it from twos
            n_wildcards_v1 = n_wildcards - 1

            if n_wildcards_v1 <= 1:
            # Check if the ranks form a valid run
                ranks_v1 = ranks + ['2']  # Add one two to the ranks
                indices = sorted(rank_order.index(r) for r in ranks_v1)
                if len(indices) == len(set(indices)): # Check for duplicates
                    gaps = (indices[-1] - indices[0] + 1) - len(indices)
                    if gaps <= n_wildcards_v1:
                        return True # Success! The meld is valid in this configuration.
        
        if n_wildcards <= 1:
            indices = sorted(rank_order.index(r) for r in ranks)
            if len(indices) == len(set(indices)): # Check for duplicates
                gaps = (indices[-1] - indices[0] + 1) - len(indices)
                if gaps <= n_wildcards:
                    return True # Success! The meld is valid in this configuration.
    
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

    def check_can_meld(self,cards_to_meld):
        """
        Check if the current player can remove meld cards from their hand.
        Returns True if player if allowed to remove meld cards from their hand.
        If player has gone to Potzo, they can only remove meld cards if they have at least 2 cards left in hand, or are ready for end game
        """
        player = self.players[self.current_player]
        hand = player.hand.copy()
        print(hand)
        hand_without_meld = hand.copy()
        # Make sure all cards to be melded are actually in hand
        for card in cards_to_meld:
            if card not in hand:
                return False
            hand_without_meld.remove(card)
        print(hand_without_meld)
        if not player.gone_to_potzo:
            return True # no restrictions on melding if player has not gone to Potzo
        if len(hand_without_meld) >= 2:
            return True # always okay to meld if player has at least 2 cards left in hand
        if len(hand_without_meld) == 0:  # already gone to Potzo
            return False # must be able to discard at least one card to end game
        if len(hand_without_meld) == 1:
            if hand_without_meld[0] == 'JK' or hand_without_meld[0][0] == '2':  # can not end on joker
                return False
            if any(len(meld) >= 7 for meld in player.melds): # can only end game if player has a meld of at least 7 cards
                return True
            return False
        return False

    
    def check_end_game(self):
        player_id = self.current_player
        player = self.players[player_id]
        if not player.gone_to_potzo:
            return False

        has_burraco = any(len(meld) >= 7 for meld in player.melds)
        if not has_burraco:
            return False

        if len(player.hand) == 0:
            return True

        return False
        
    def sort_cards(cards):
        rank_order = "23456789TJQKA"
        suit_order = "CDHS"  # Clubs < Diamonds < Hearts < Spades

        def card_key(card):
            if card == 'JK':
                return (99, 'Z')
            rank, suit = card[0], card[1]
            return (suit_order.index(suit),rank_order.index(rank), )

        return sorted(cards, key=card_key)
    
    def get_payoffs(self):
        # TODO: Return final scores for all players
        return [0, 0]
