from rlcard.games.burraco.game import BurracoGame

def test_discard_and_pickup():
    game = BurracoGame()
    game.init_game()

    player = game.current_player
    _, _ = game.step('draw_pile')
    
    game.players[game.current_player].hand = ['5H', '6D', '7C']
    hand_before = game.players[player].hand.copy()
    # Discard a card from hand
    discard_card = hand_before[0]
    _, next_player = game.step(('discard', discard_card))
    
    assert discard_card not in game.players[player].hand
    assert discard_card in game.dealer.discard_pile
    assert next_player != player

    # Next player picks up discard pile
    player = next_player
    discard_pile_before = game.dealer.discard_pile.copy()
    _, _ = game.step('pickup_discard')
    for card in discard_pile_before:
        assert card in game.players[player].hand
    assert len(game.dealer.discard_pile) == 0

    print("Discard and pickup tests passed!")

def test_discard_edge_cases():
    game = BurracoGame()
    game.init_game()
    player = game.current_player
    # Must draw before discard - test skipping draw
    try:
        game.step(('discard', '7C'))
    except ValueError as e:
        assert str(e) == "Must draw a card before discarding."
    else:
        assert False, "Expected ValueError for discarding before draw"

    # Draw first
    _, _ = game.step('draw_pile')
    player = game.current_player
    state, player = game.get_state(player)
    
    # Discard card not in hand
    game.players[game.current_player].hand = ['5H', '6D', '7C']
    fake_card = '9S'  # definitely not in hand
    try:
        game.step(('discard', fake_card))
    except ValueError as e:
        error_msg = str(e)
        print(error_msg)
        assert f"Player {game.current_player} cannot discard card: {fake_card}, not in hand." in error_msg
    else:
        assert False, "Expected ValueError for discarding card not in hand"

    # Normal discard to clear flag
    discard_card = game.players[game.current_player].hand[0]
    _, next_player = game.step(('discard', discard_card))

    # Next player tries to pick up empty discard pile (simulate)
    game.dealer.discard_pile.clear()
    try:
        game.step('pickup_discard')
    except ValueError as e:
        assert "discard pile is empty" in str(e).lower()
    else:
        assert False, "Expected ValueError for picking up empty discard pile"

    print("Discard edge case tests passed!")

if __name__ == "__main__":
    test_discard_and_pickup()
    test_discard_edge_cases()
