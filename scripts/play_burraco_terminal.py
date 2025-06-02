from rlcard.games.burraco.game import BurracoGame

game = BurracoGame()
state, player_id = game.init_game()
print(f"Player {player_id}'s hand: {state['hand']}")

while True:
    print(f"\nPlayer {game.current_player}'s turn, phase: {game.phase}")
    print(f"Your hand: {game.players[game.current_player].hand}")
    print(f"Discard pile top: {game.dealer.discard_pile[-1] if game.dealer.discard_pile else 'Empty'}")

    action_input = input("Enter action (draw_pile, pickup_discard, meld, add_to_meld, discard): ").strip()

    if action_input == 'draw_pile' or action_input == 'pickup_discard':
        action = action_input
    elif action_input == 'meld':
        cards = input("Enter meld cards separated by space (e.g. 7C 7D 7H): ").split()
        action = ('meld', cards)
    elif action_input == 'add_to_meld':
        meld_idx = int(input("Enter meld index to add to: "))
        cards = input("Enter cards to add separated by space: ").split()
        action = ('add_to_meld', meld_idx, cards)
    elif action_input == 'discard':
        card = input("Enter card to discard: ").strip()
        action = ('discard', card)
    else:
        print("Invalid action, try again.")
        continue

    try:
        state, next_player = game.step(action)
    except Exception as e:
        print(f"Error: {e}")
        continue
