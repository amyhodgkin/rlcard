from rlcard.games.burraco.game import BurracoGame

game = BurracoGame()
state, player_id = game.init_game()
print(f"Player {player_id}'s hand: {state['hand']}")

next_state, next_player = game.step('draw')
print(f"Next player is {next_player}")
