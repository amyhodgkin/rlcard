from rlcard.games.burraco.game import BurracoGame
from random import shuffle
def test_sort():
    game = BurracoGame()

    cards = ['5C', '6C', '7C', '3D', '9H', 'AH', '5S', 'TS']
    cards_sorted = cards.copy()
    shuffle(cards)

    cards_resorted = BurracoGame.sort_cards(cards)
    assert cards_resorted == cards_sorted, f"Expected {cards_sorted}, but got {cards_resorted}"

    cards = ['2C','5C', '6C', '7C', '3D', '9H', 'AH', '5S', 'TS', 'JK']
    cards_sorted = cards.copy()
    shuffle(cards)

    cards_resorted = BurracoGame.sort_cards(cards)
    assert cards_resorted == cards_sorted, f"Expected {cards_sorted}, but got {cards_resorted}"
    
if __name__ == "__main__":
    test_sort()
    print("test_sort passed.")