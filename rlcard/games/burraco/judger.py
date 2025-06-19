import collections
from rlcard.games.burraco.utils import get_card_str # Assuming you have a card representation

# Let's assume you have a card representation where:
# 'S' = Spades, 'H' = Hearts, 'D' = Diamonds, 'C' = Clubs
# 'B-Joker', 'R-Joker' for Jokers
# Card strings look like 'S2', 'HA', 'DK', etc.

class BurracoJudge:
    '''
    Judge for the Italian Burraco card game.
    '''

    def get_payoffs(self, game):
        '''
        Calculates the score for each team at the end of a round.

        Args:
            game (BurracoGame): The game object with the final state.
            
        Returns:
            (list): A list of scores for each player. For a 2v2 game,
                    players on the same team will have the same score.
                    e.g., [team_A_score, team_B_score, team_A_score, team_B_score]
        '''
        
        # Assuming teams are players [0, 2] and [1, 3]
        team_scores = {0: 0, 1: 0} # Team 0 (p0, p2), Team 1 (p1, p3)

        # 1. Determine which team closed
        closing_team_id = game.round.winner_id % 2
        team_scores[closing_team_id] += 100 # Chiusura bonus

        for team_id in [0, 1]:
            team_score = 0
            
            # These are the players on the current team we are scoring
            player_ids = [team_id, team_id + 2]
            
            # Get all melds for the team
            team_melds = []
            for pid in player_ids:
                # You need to have player.melds available in your game state
                team_melds.extend(game.players[pid].melds)

            # 2. Calculate points from melded cards and Burrachi
            meld_points = self._calculate_melds_points(team_melds)
            team_score += meld_points

            # 3. Calculate negative points from cards in hand
            hand_points_penalty = 0
            for pid in player_ids:
                for card in game.players[pid].hand:
                    hand_points_penalty += self._get_card_point_value(card)
            team_score -= hand_points_penalty

            # 4. Check for Pozzetto penalty
            # You need a flag like player.has_taken_pozzetto
            pozzetto_taken_by_team = (game.players[player_ids[0]].has_taken_pozzetto or 
                                      game.players[player_ids[1]].has_taken_pozzetto)
            if not pozzetto_taken_by_team:
                team_score -= 100

            team_scores[team_id] += team_score

        # Prepare the final payoffs array as required by RLCard
        payoffs = [0] * game.num_players
        payoffs[0] = team_scores[0]
        payoffs[1] = team_scores[1]
        payoffs[2] = team_scores[0]
        payoffs[3] = team_scores[1]
        
        return payoffs

    def _get_card_point_value(self, card_str):
        ''' Returns the point value of a single card. '''
        # Assuming card_str format like 'S3', 'HA', 'C-Joker'
        if 'Joker' in card_str:
            return 30
            
        rank = card_str[1:] # e.g., 'A', 'K', '2', '8'
        if rank == 'A':
            return 15
        if rank == '2': # Pinella
            return 20
        if rank in ['K', 'Q', 'J', 'T', '9', '8']: # T for 10
            return 10
        if rank in ['7', '6', '5', '4', '3']:
            return 5
        return 0 # Should not happen

    def _calculate_melds_points(self, melds):
        '''
        Calculates the total points from all melds for a team,
        including Burraco bonuses.
        '''
        total_points = 0
        for meld in melds:
            # First, add the value of every card in the meld
            for card in meld:
                total_points += self._get_card_point_value(card)
            
            # Second, check if the meld is a Burraco (7+ cards) and add bonus
            if len(meld) >= 7:
                is_wildcard_present = any('Joker' in c or c[1] == '2' for c in meld)
                
                if not is_wildcard_present:
                    # Clean Burraco (Pulito)
                    total_points += 200
                else:
                    # It's either Dirty or Semi-Clean. This logic can be tricky.
                    # A simple way to check for Semi-Clean is to see if there is
                    # a continuous run of 7+ natural cards within the meld.
                    if self._is_semipulito(meld):
                         total_points += 150
                    else:
                        # Dirty Burraco (Sporco)
                        total_points += 100
        return total_points

    def _is_semipulito(self, meld):
        '''
        Checks if a burraco with a wildcard is semi-clean.
        This requires a sequence of at least 7 natural cards.
        This is a complex check and depends on your card representation.
        
        A simple heuristic for sequence melds:
        1. Temporarily remove wildcards.
        2. Sort the remaining natural cards by rank.
        3. Check if there's a continuous run of 7 or more cards.
        
        This is a placeholder for your more complex logic.
        '''
        # This is a simplified example for sequence melds. You'll need to adapt it.
        natural_cards = [c for c in meld if not ('Joker' in c or c[1] == '2')]
        
        # We only care if there is a sequence of 7 natural cards
        if len(natural_cards) < 7:
            return False

        # TODO: Implement the logic to check for a continuous sequence of 7+ cards
        # This is non-trivial. For a set meld (e.g., seven Kings), it's always "clean" 
        # if it has no wildcards, or "dirty" if it does. The semi-clean concept
        # primarily applies to sequences.

        # For now, we'll use a simplified rule: if it has a wildcard but 7+ natural
        # cards, we'll call it semi-clean. A more robust implementation is needed.
        if len(natural_cards) >= 7:
            return True # Simplified assumption
            
        return False