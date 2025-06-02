from rlcard.games.burraco.game import BurracoGame

def test_is_valid_meld():
    game = BurracoGame()

    # Valid set with no jokers
    assert game.is_valid_meld(['7C', '7D', '7H']) == True

    # Valid set with 1 joker
    assert game.is_valid_meld(['7C', '7D', 'JK']) == True

    # Invalid set with 2 jokers
    assert game.is_valid_meld(['7C', 'JK', 'JK']) == False

    # Valid run with no jokers
    assert game.is_valid_meld(['5H', '6H', '7H']) == True

    # Valid run with 1 joker filling gap
    assert game.is_valid_meld(['5H', '7H', 'JK']) == True

    # Invalid run with 2 jokers (more than 1 gap)
    assert game.is_valid_meld(['5H', '9H', 'JK', 'JK']) == False

    # Invalid run with wrong suits
    assert game.is_valid_meld(['5H', '6D', '7H']) == False

    print("All meld tests passed!")

if __name__ == "__main__":
    test_is_valid_meld()
