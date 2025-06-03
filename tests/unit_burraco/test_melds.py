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

    assert game.is_valid_meld(['5H', '6H', '7H', '8H']) == True  # Valid run with 4 cards

    assert game.is_valid_meld(['5H', '6H', '7H', '8H', 'JK']) == True  # Valid run with 4 cards and a joker

    # Valid meld with two wildcards (2 in place))
    assert game.is_valid_meld(['2H', '3H', '4H', '6H', 'JK'])
    game.is_valid_meld(['2H', '3H', '4H', '6H', 'JK', 'JK'])  # Valid meld with two wildcards
    # Invalid meld with two wildcards
    assert not game.is_valid_meld(['2C', '3H', 'JK', '5H'])

    assert game.is_valid_meld(['2H', '3H', '4H', '2C', '6H'])

    assert game.is_valid_meld(['2H', '3H', '4H', '5H', '6H'])  # Valid meld with no wildcards

    assert game.is_valid_meld(['2H', '3H', '4H', '5H', '6H', '2C'])  # Valid meld with no wildcards

    assert game.is_valid_meld(['2H', '2H', '4H', '5H', '6H'])  # Valid meld with one wildcard
    
    assert game.is_valid_meld(['2H', 'JK', '4H', '5H', '6H'])  # Valid meld with one wildcard

    assert not game.is_valid_meld(['2D', '2C', '4H', '5H', '6H', '7H'])  # Invalid meld with too many cards

    # Two 2s, both wild – invalid
    assert not game.is_valid_meld(['3H', '5H', '2C', '2D'])

    # 2H as natural card
    assert game.is_valid_meld(['2H', '3H', '4H'])

    # 2C as wildcard
    assert game.is_valid_meld(['3H', '4H', '6H', '2C'])

    # Joker and 2C – invalid (too many wilds)
    assert not game.is_valid_meld(['3H', '4H', '6H', '2C', 'JK'])

if __name__ == "__main__":

    test_is_valid_meld()
