from rlcard.games.burraco.game import BurracoGame

game = BurracoGame()
state, player_id = game.init_game()
print(f"Player {player_id}'s hand: {state['hand']}")

# Player draws
_, _ = game.step('draw_pile')
print(f"Player {player_id} drew a card. New hand: {game.players[player_id].hand}")

# Player discards first card in hand
discard_card = game.players[player_id].hand[0]
_, next_player = game.step(('discard', discard_card))
print(f"Player {player_id} discarded {discard_card}. New hand: {game.players[player_id].hand}")

# Print discard pile
print(f"Discard pile: {game.dealer.discard_pile}")
print(f"Next player is {next_player}")

# Next player chooses to pick up the discard pile
state, current_player = game.step('pickup_discard')
print(f"Player {current_player} picked up the discard pile. New hand: {game.players[current_player].hand}")

# Then discards a card
discard_card = game.players[current_player].hand[0]
state, next_player = game.step(('discard', discard_card))
print(f"Player {current_player} discarded {discard_card}. New hand: {game.players[current_player].hand}")
print(f"Next player is {next_player}")
print(f"Discard pile now: {game.dealer.discard_pile}")
