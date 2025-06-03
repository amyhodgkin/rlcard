from rlcard.games.burraco.game import BurracoGame

def test_end_game_with_burraco():
    game = BurracoGame()

    # Force setup
    game.current_player = 0
    player = game.players[0]
    player.gone_to_potzo = True  # Simulate already gone to potzo
    player.hand = ['5H']  # Just one card left to discard

    # Add a valid burraco (7+ cards)
    player.melds = [['3H', '4H', '5H', '6H', '7H', '8H', '9H']]  # 7-card straight

    # Set game state to discard phase
    game.phase = 'discard'

    # Discard last card to trigger win
    state, player_id, done = game.step(('discard', '5H'))

    assert done is True
    assert game.game_over is True
    assert player.hand == []
    print("test_end_game_with_burraco passed.")


def test_game_does_not_end_without_burraco():
    game = BurracoGame()
    game.current_player = 0
    player = game.players[0]

    player.gone_to_potzo = True
    player.hand = ['5H']
    player.melds = [['3H', '4H', '5H']]  # Not a burraco (only 3 cards)
    game.phase = 'discard'

    state, player_id, done = game.step(('discard', '5H'))

    assert done is False
    assert game.game_over is False
    assert player.hand == []
    print("Game does not end without a burraco.")


if __name__ == "__main__":
    test_end_game_with_burraco()
    test_game_does_not_end_without_burraco()