#testing area
# Instantiate the Lobby
lobby = Lobby()
print("Lobby initialized with games:", lobby.games)

# Create a player and an NPC
player = Player("Shaun")
npc = NPCPlayer()

# Print the player's and NPC's details
print(f"Player Name: {player.name}, Balance: ${player.balance}")
print(f"NPC Name: {npc.get_full_name()}, Balance: ${npc.balance}")

# Test joining a game
player.join_game(lobby.games)
npc.join_game("Blackjack")

# Create a Blackjack game
blackjack_game = Blackjack(players=[player, npc])

# Test placing bets
print("\nTesting Bets:")
player_bet_success = blackjack_game.place_bet(player, 15)  # Attempt a valid bet
npc_bet_success = blackjack_game.place_bet(npc, 5)  # Attempt an invalid bet (less than min bet)

# Test drawing and discarding cards
print("\nTesting Card Drawing and Discarding:")
card1 = blackjack_game.draw_card()
card2 = blackjack_game.draw_card()
print(f"Player drew: {card1} and {card2}")

player.receive_card(card1)
player.receive_card(card2)

# Display player's hand value
print(f"{player.name}'s hand value: {player.calculate_hand_value()}")

# NPC receives a card and makes a decision
npc.receive_card(blackjack_game.draw_card())
npc_decision = npc.make_decision()
print(f"{npc.name} decided to {npc_decision}.")

# Test splitting hands (if applicable)
print("\nTesting Hand Splitting:")
player.receive_card(card1)  # Add another card to potentially create a pair
if player.can_split():
    player.split_hand()
else:
    print(f"{player.name} cannot split their hand.")

# Test reshuffling the deck when empty
print("\nTesting Deck Reshuffle:")
# Simulate emptying the deck
blackjack_game.full_deck = []
blackjack_game.reshuffle_deck()  # This should reshuffle from the trash deck

# Test leaving the game
print("\nTesting Leaving Game:")
player.leave_game()
npc.leave_game()