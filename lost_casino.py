import random
import time
import builtins

def print_ascii(*args, end='\n', flush=True, **kwargs):
    text = " ".join(str(arg) for arg in args)
    original_print(text, end=end, flush=flush)
def print_inst(*args, end='\n', flush=True, **kwargs):
    text = " ".join(str(arg) for arg in args)
    original_print(text, end=end, flush=flush)

# Save the original print function
original_print = builtins.print

# Global settings for slow printing
settings = {
    "text_speed": 0.025,  # Default delay per character
    "enable_slow_text": True  # Toggle slow text globally
}

# Function to retrieve settings dynamically
def get_text_speed():
    return settings["text_speed"]

def is_slow_text_enabled():
    return settings["enable_slow_text"]

# Define slow_print to use the original print internally
def slow_print(*args, end='\n', flush=True, **kwargs):
    # Combine arguments into a single string for printing
    text = " ".join(str(arg) for arg in args)
    delay = get_text_speed()  # Get delay from the dynamic function

    # Print each character slowly if enabled; otherwise, print normally
    if is_slow_text_enabled():  # Check the setting dynamically
        for char in text:
            original_print(char, end='', flush=True, **kwargs)
            time.sleep(delay)
        original_print(end=end, flush=flush)  # Print the end character after the loop
    else:
        original_print(text, end=end, flush=flush)

# Override the built-in print to use slow_print instead
builtins.print = slow_print


npc_names = {
    "Jack": {"last_name": "Shephard", "title": "The Leader", "trait": "Courageous"},
    "Kate": {"last_name": "Austen", "title": "The Fugitive", "trait": "Resourceful"},
    "Sawyer": {"last_name": "Ford", "title": "The Con Man", "trait": "Charming"},
    "Locke": {"last_name": "Locke", "title": "The Hunter", "trait": "Mysterious"},
    "Hurley": {"last_name": "Reyes", "title": "The Lucky", "trait": "Good-natured"},
    "Sayid": {"last_name": "Jarrah", "title": "The Warrior", "trait": "Intelligent"},
    "Sun": {"last_name": "Kwon", "title": "The Loyal", "trait": "Caring"},
    "Jin": {"last_name": "Kwon", "title": "The Protector", "trait": "Dedicated"},
    "Desmond": {"last_name": "Hume", "title": "The Constant", "trait": "Determined"},
    "Ben": {"last_name": "Linus", "title": "The Manipulator", "trait": "Cunning"},
    "Claire": {"last_name": "Littleton", "title": "The Mother", "trait": "Compassionate"},
    "Charlie": {"last_name": "Pace", "title": "The Musician", "trait": "Brave"},
    "Michael": {"last_name": "Dawson", "title": "The Father", "trait": "Protective"},
    "Walt": {"last_name": "Lloyd", "title": "The Gifted", "trait": "Mysterious"},
    "Richard": {"last_name": "Alpert", "title": "The Ageless", "trait": "Wise"}
}

class Lobby:
    def __init__(self, games=None, current_game=None, player_balance=1000):
        self.games = games if games else ["Blackjack", "Roulette"]  # Use provided games or default
        self.current_game = current_game
        self.player_balance = player_balance  # Starting balance

class Blackjack:
    def __init__(self, players=None, full_deck=None, trash_deck=None, dealer=None, min_bet=10):
        self.players = players if players else []  # Area for the players
        self.full_deck = full_deck if full_deck else self.create_deck()  # Initial full deck (shuffled)
        self.trash_deck = trash_deck if trash_deck else []  # Discarded cards
        self.dealer_hand = []  # Dealer's hand
        self.min_bet = min_bet  # Minimum bet amount

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        single_deck = [(value, suit) for suit in suits for value in values]

        triple_deck = single_deck * 3
        random.shuffle(triple_deck)  # Shuffle the deck
        return triple_deck

    def draw_card(self):
        # Check if the deck is empty and needs to be reshuffled
        if not self.full_deck:
            self.reshuffle_deck()

        # Draw a card from the top of the deck
        card = self.full_deck.pop(0)
        return card

    def discard_card(self, card):
        # Add the discarded card to the trash deck
        self.trash_deck.append(card)

    def reshuffle_deck(self):
        # Move all cards from the trash deck back into the full deck and shuffle
        self.full_deck = self.trash_deck
        self.trash_deck = []  # Clear the trash deck
        random.shuffle(self.full_deck)
        print("Deck reshuffled!")

    def place_bet(self, player, amount):
        """Place a bet if the amount is greater than or equal to the minimum bet and the player has enough balance."""
        if amount < self.min_bet:
            print(f"The minimum bet is ${self.min_bet}. Please increase your bet amount.")
            return False
        elif amount > player.balance:
            print(f"{player.name} does not have enough balance to place this bet.")
            return False
        else:
            player.balance -= amount
            print(f"{player.name} placed a bet of ${amount}. Remaining balance: ${player.balance}")
            return True

    def dealer_blackjack_check(self):
        """Check if the dealer has a Blackjack."""
        if self.calculate_hand_value(self.dealer_hand) == 21:
            print("Dealer has a Blackjack! All players without 21 lose.")
            return True
        return False

    def calculate_hand_value(self, hand):
        """Calculate the total value of a hand (specific to Blackjack)."""
        value = 0
        ace_count = 0
        for card in hand:
            if card[0] in ['Jack', 'Queen', 'King']:
                value += 10
            elif card[0] == 'Ace':
                ace_count += 1
                value += 11
            else:
                value += int(card[0])

        while value > 21 and ace_count > 0:
            value -= 10
            ace_count -= 1

        return value

class NPCPlayer:
    def __init__(self, balance=1000):
        self.name, self.details = self.assign_random_name()
        self.hands = [[]]  # A list of hands, starting with one empty hand
        self.balance = balance
        self.is_active = True
        self.current_game = None

    def assign_random_name(self):
        """Assign a random unique name from npc_names."""
        while True:
            name = random.choice(list(npc_names.keys()))
            if name not in used_names:
                used_names.add(name)
                details = npc_names[name]
                return name, details

    def get_full_name(self):
        """Return the full name with title and trait."""
        return f"{self.details['title']} {self.name} {self.details['last_name']} - {self.details['trait']}"
    
    def join_game(self, game_name):
        """Assign the NPC to a game."""
        self.current_game = game_name
        print(f"{self.name} has joined {self.current_game}.")

    def leave_game(self):
        """Remove the NPC from the current game."""
        print(f"{self.name} has left {self.current_game}.")
        self.current_game = None

    def receive_card(self, card, hand_index=0):
        """Add a card to the specified hand (for card games)."""
        self.hands[hand_index].append(card)

    def clear_hands(self):
        """Clear all of the NPC's hands for starting a new round in a card game."""
        self.hands = [[]]

    def can_split(self, hand_index=0):
        """Check if the NPC's hand can be split (i.e., has two cards of the same value)."""
        hand = self.hands[hand_index]
        return len(hand) == 2 and hand[0][0] == hand[1][0]  # Check if both cards have the same value

    def split_hand(self):
        """Split the NPC's hand into two separate hands if they have a pair."""
        if self.can_split():
            card1, card2 = self.hands[0]  # Get the two cards
            self.hands = [[card1], [card2]]  # Split into two separate hands
            print(f"{self.name} has split their hand into two hands.")
        else:
            print(f"{self.name} cannot split their hand.")

    def make_decision(self, hand_index=0):
        """Decide whether to hit, stand, or split, with automatic splitting of Aces."""
        if self.current_game == "Blackjack":
            # Check if the hand can be split and contains two Aces
            if self.can_split(hand_index) and self.hands[hand_index][0][0] == "Ace":
                self.split_hand()
                return "split"

            hand_value = self.calculate_hand_value(hand_index)
            
            # Basic decision-making with randomness
            if hand_value < 17:
                return "hit"
            elif hand_value == 17:
                # Random chance to hit on 17 (e.g., 20% chance)
                return "hit" if random.random() < 0.2 else "stand"
            else:
                return "stand"
        return "stand"

    def calculate_hand_value(self, hand_index=0):
        """Calculate the total value of the specified hand (specific to Blackjack)."""
        hand = self.hands[hand_index]
        value = 0
        ace_count = 0
        for card in hand:
            if card[0] in ['Jack', 'Queen', 'King']:
                value += 10
            elif card[0] == 'Ace':
                ace_count += 1
                value += 11  # Initially count Aces as 11
            else:
                value += int(card[0])

        # Adjust for Aces if the value exceeds 21
        while value > 21 and ace_count > 0:
            value -= 10
            ace_count -= 1

        return value

    def place_bet(self, amount):
        """Place a bet if the NPC has enough balance."""
        if amount <= self.balance:
            self.balance -= amount
            print(f"{self.name} placed a bet of ${amount}. Remaining balance: ${self.balance}")
            return amount
        else:
            print(f"{self.name} does not have enough balance to place this bet.")
            return 0

used_names = set()  # To keep track of used names and ensure uniqueness
  

class Player:
    def __init__(self, name, balance=1000):
        self.name = name
        self.hands = [[]]  # A list of hands, starting with one empty hand
        self.balance = balance  # Starting balance
        self.is_active = True  # Indicates if the player is active in a game
        self.current_game = None  # Track the game the player is currently playing

    def join_game(self, game_name):
        """Assign the player to a game."""
        if game_name in ["Blackjack", "Roulette"]:
            self.current_game = game_name
            print(f"{self.name} has joined {self.current_game}.")
        else:
            print("Invalid game selection. Please try again.")

    def leave_game(self):
        """Remove the player from the current game."""
        if self.current_game:
            print(f"{self.name} has left {self.current_game}.")
            self.current_game = None
        else:
            print("You are not currently in a game.")

    def receive_card(self, card, hand_index=0):
        """Add a card to the specified hand (for card games)."""
        self.hands[hand_index].append(card)

    def clear_hands(self):
        """Clear all of the player's hands for starting a new round in a card game."""
        self.hands = [[]]

    def can_split(self, hand_index=0):
        """Check if the player's hand can be split (i.e., has two cards of the same value)."""
        hand = self.hands[hand_index]
        return len(hand) == 2 and hand[0][0] == hand[1][0]  # Check if both cards have the same value

    def split_hand(self, game, hand_index=0):
        """Split the player's hand into two separate hands if they have a pair."""
        if self.can_split(hand_index):
            card1, card2 = self.hands[hand_index]  # Get the two cards
            self.hands[hand_index] = [card1]  # Update the current hand with the first card
            self.hands.append([card2])  # Add a new hand with the second card
        
            # Deal a new card to each new hand
            self.hands[hand_index].append(game.deal_card())
            self.hands[-1].append(game.deal_card())
        
            # Announce the new totals for each hand
            print(f"{self.name} has split their hand into two hands.")
            for i, hand in enumerate(self.hands):
                print(f"Hand {i+1}: {hand} (Total: {game.calculate_hand_total(hand)})")
        
            # Recursively check for further splits
            for i in range(len(self.hands)):
                if self.can_split(i):
                    self.split_hand(game, i)
        else:
            print("You cannot split this hand.")

    def make_decision(self, hand_index=0):
        """Prompt the player to make a decision (specific to Blackjack)."""
        if self.current_game == "Blackjack":
            while True:  # Loop until a valid input is given
                decision = input(f"{self.name}, do you want to 'hit', 'stand', or 'split' (if possible)? ").lower()
                if decision in ["hit", "stand", "split"]:
                    if decision == "split" and not self.can_split(hand_index):
                        print("You cannot split this hand.")
                        continue
                    return decision
                print("Invalid choice. Please enter 'hit', 'stand', or 'split'.")
        return "stand"

    def calculate_hand_value(self, hand_index=0):
        """Calculate the total value of the specified hand (specific to Blackjack)."""
        hand = self.hands[hand_index]
        value = 0
        ace_count = 0
        for card in hand:
            if card[0] in ['Jack', 'Queen', 'King']:
                value += 10
            elif card[0] == 'Ace':
                ace_count += 1
                value += 11  # Initially count Aces as 11
            else:
                value += int(card[0])

        # Adjust for Aces if the value exceeds 21
        while value > 21 and ace_count > 0:
            value -= 10
            ace_count -= 1

        return value

    def place_bet(self, amount):
        """Place a bet if the player has enough balance."""
        if amount <= self.balance:
            self.balance -= amount
            print(f"{self.name} placed a bet of ${amount}. Remaining balance: ${self.balance}")
            return amount
        else:
            print(f"{self.name} does not have enough balance to place this bet.")
            return 0

def main_lobby():
    print("Welcome to the Lost Casino!")
    player_name = input("Please enter your name: ")
    player = Player(name=player_name)
    lobby = Lobby()
    npcs = [NPCPlayer() for _ in range(random.randint(2, 4))]

    # Main loop for the lobby
    while True:
        print("\nYou are in the lobby. Available games: ", ", ".join(lobby.games))
        choice = input("Would you like to 'join' a game, 'leave' the casino, or 'check' your balance? ").lower()

        if choice == "join":
            game_choice = input(f"Which game would you like to join? ({', '.join(lobby.games)}) ").capitalize()
            if game_choice == "Blackjack":
                player.join_game(game_choice)
                print("\nYou have joined Blackjack!")
                print("NPC Players joining the game:")
                for npc in npcs:
                    npc.join_game("Blackjack")
                    print(f"{npc.get_full_name()} has joined the game.")

                # Start the Blackjack game
                blackjack_game = Blackjack(players=[player] + npcs)
                play_blackjack(blackjack_game, player, npcs)
            elif game_choice == "Roulette":
                player.join_game(game_choice)
                print("\nYou have joined Roulette!")
                print("NPC Players joining the game:")
                for npc in npcs:
                    npc.join_game("Roulette")
                    print(f"{npc.get_full_name()} has joined the game.")

                # Start the Roulette game
                roulette_game = Roulette(players=[player] + npcs)
                play_roulette(roulette_game, player, npcs)
            else:
                print("Invalid game selection. Please try again.")
        elif choice == "leave":
            print("Thanks for visiting the Lost Casino! See you next time.")
            break
        elif choice == "check":
            print(f"Your current balance is: ${player.balance}")
        else:
            print("Invalid choice. Please try again.")

def play_blackjack(blackjack_game, player, npcs):
    print("\nStarting a game of Blackjack...")

    # Ask the player to place a bet
    while True:
        try:
            player_bet = int(input("How much would you like to bet? (Minimum bet is $10) "))
            if blackjack_game.place_bet(player, player_bet):
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # NPCs place their bets
    for npc in npcs:
        npc_bet = random.randint(10, 50)
        blackjack_game.place_bet(npc, npc_bet)

    # Deal initial cards to all players and the dealer
    for _ in range(2):
        player.receive_card(blackjack_game.draw_card())
        for npc in npcs:
            npc.receive_card(blackjack_game.draw_card())
        blackjack_game.dealer_hand.append(blackjack_game.draw_card())

    # Show initial hands
    print(f"\n{player.name}'s hand: {player.hands[0]} (Value: {player.calculate_hand_value()})")
    for npc in npcs:
        print(f"{npc.get_full_name()}'s hand: {npc.hands[0]} (Value: {npc.calculate_hand_value()})")
    print(f"Dealer's visible card: {blackjack_game.dealer_hand[0]}")

    # Check if the dealer has a Blackjack
    dealer_value = blackjack_game.calculate_hand_value(blackjack_game.dealer_hand)
    if dealer_value == 21:
        print("\nDealer has Blackjack! All players lose unless they also have Blackjack.")
        
        # Check if player has Blackjack
        if player.calculate_hand_value() == 21:
            print(f"{player.name} has a Blackjack as well! It's a tie, and the bet is returned.")
            player.balance += player_bet
        else:
            print(f"{player.name} loses the bet.")

        # Check if each NPC has Blackjack
        for npc in npcs:
            npc_value = npc.calculate_hand_value()
            if npc_value == 21:
                print(f"{npc.get_full_name()} also has a Blackjack and ties with the dealer.")
            else:
                print(f"{npc.get_full_name()} loses.")
        
        # Clear all hands and move cards to the trash deck after dealer blackjack
        clear_and_discard(player.hands[0])
        for npc in npcs:
            clear_and_discard(npc.hands[0])
        clear_and_discard(blackjack_game.dealer_hand)
        
        return  # End the game if dealer has blackjack

    # Player's turn if dealer doesn't have a Blackjack
    player_blackjack = False
    if player.calculate_hand_value() == 21:
        print(f"{player.name} has a Blackjack! Potential win if dealer does not match.")
        player_blackjack = True  # Flag that the player has Blackjack for later evaluation
    else:
        # Let player make decisions if they don't have Blackjack
        hand_index = 0
        while hand_index < len(player.hands):
            print(f"\nPlaying hand {hand_index + 1} for {player.name}")
            while True:
                decision = player.make_decision(hand_index)
                if decision == "hit":
                    card = blackjack_game.draw_card()
                    player.receive_card(card, hand_index)
                    print(f"{player.name} drew: {card}")
                    print(f"{player.name}'s new hand value: {player.calculate_hand_value(hand_index)}")
                    if player.calculate_hand_value(hand_index) > 21:
                        print(f"{player.name} busted with a value of {player.calculate_hand_value(hand_index)}!")
                        break
                elif decision == "stand":
                    print(f"{player.name} stands with a value of {player.calculate_hand_value(hand_index)}.")
                    break
                elif decision == "split" and player.can_split(hand_index):
                    if player.balance >= player_bet:
                        card_to_split = player.hands[hand_index].pop()
                        player.hands.append([card_to_split])
                        player.balance -= player_bet
                        print(f"{player.name} has split their hand and placed an additional bet of ${player_bet}.")
                        print(f"Remaining balance: ${player.balance}")
                    else:
                        print(f"{player.name} does not have enough balance to split.")
                        break
                else:
                    print("Invalid choice. Please enter 'hit', 'stand', or 'split'.")
            hand_index += 1

    # NPCs' turns
    for npc in npcs:
        print(f"\n{npc.get_full_name()}'s turn.")
        while npc.make_decision() == "hit":
            card = blackjack_game.draw_card()
            npc.receive_card(card)
            print(f"{npc.name} drew: {card}")
            if npc.calculate_hand_value() > 21:
                print(f"{npc.name} busted with a value of {npc.calculate_hand_value()}!")
                break
        print(f"{npc.name} stands with a value of {npc.calculate_hand_value()}.")

    # Dealer's turn
    print("\nDealer's turn.")
    dealer_value = blackjack_game.calculate_hand_value(blackjack_game.dealer_hand)
    print(f"Dealer's hand: {blackjack_game.dealer_hand} (Value: {dealer_value})")
    while dealer_value < 17:
        card = blackjack_game.draw_card()
        blackjack_game.dealer_hand.append(card)
        dealer_value = blackjack_game.calculate_hand_value(blackjack_game.dealer_hand)
        print(f"Dealer drew: {card} (New value: {dealer_value})")

    if dealer_value > 21:
        print("Dealer busted!")

    # Compare hands and determine the winner
    print("\nFinal results:")
    player_value = player.calculate_hand_value()
    if player_blackjack:
        # Handle the outcome if the player initially had Blackjack
        if dealer_value != 21:
            print(f"{player.name} wins with a Blackjack! Doubling the bet.")
            player.balance += player_bet * 2
        else:
            print("It's a tie with the dealer Blackjack. Bet returned.")
            player.balance += player_bet
    elif player_value <= 21:
        if dealer_value > 21 or player_value > dealer_value:
            print(f"{player.name} wins and doubles their bet!")
            player.balance += player_bet * 2
        elif player_value < dealer_value:
            print(f"{player.name} loses the bet.")
        else:
            print(f"It's a tie! {player.name} gets their bet back.")
            player.balance += player_bet

    for npc in npcs:
        npc_value = npc.calculate_hand_value()
        if npc_value <= 21:
            if dealer_value > 21 or npc_value > dealer_value:
                print(f"{npc.get_full_name()} wins!")
            elif npc_value < dealer_value:
                print(f"{npc.get_full_name()} loses.")
            else:
                print(f"{npc.get_full_name()} ties with the dealer.")

    # Clear all hands and move cards to the trash deck
    def clear_and_discard(hand):
        for card in hand:
            blackjack_game.discard_card(card)
        hand.clear()

    clear_and_discard(player.hands[0])
    for npc in npcs:
        clear_and_discard(npc.hands[0])
    clear_and_discard(blackjack_game.dealer_hand)

    # Check if player balance has hit zero
    if player.balance <= 0:
        print("Game over! You have no balance left.")
        if input("Would you like to start over? (yes/no): ").lower() == "yes":
            player.balance = 1000  # Reset balance
            play_blackjack(blackjack_game, player, npcs)
        else:
            print("Returning to the lobby.")
            return

    # Ask the player if they want to play again
    while True:
        play_again = input("\nWould you like to play another round of Blackjack or leave? (play/leave): ").lower()
        if play_again == "play":
            play_blackjack(blackjack_game, player, npcs)
            break
        elif play_again == "leave":
            print("Thanks for playing! Returning to the lobby.")
            break
        else:
            print("Invalid choice. Please enter 'play' or 'leave'.")


def display_roulette_table():
    """Prints the ASCII representation of the roulette table."""
    print_ascii(r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                               ROULETTE TABLE                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║   3  |  6  |  9  | 12  | 15  | 18  | 21  | 24  | 27  | 30  | 33  | 36  (RED) ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║   2  |  5  |  8  | 11  | 14  | 17  | 20  | 23  | 26  | 29  | 32  | 35 (BLACK)║
║  ─────────────────────────────────────────────────────────────────────────   ║
║   1  |  4  |  7  | 10  | 13  | 16  | 19  | 22  | 25  | 28  | 31  | 34  (RED) ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  LOW (1-18) | EVEN | RED | BLACK | ODD | HIGH (19-36) ║    0    ║    00      ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

corner_bets = {
    (1, 2, 4, 5), (2, 3, 5, 6), (4, 5, 7, 8), (5, 6, 8, 9),
    (10, 11, 13, 14), (11, 12, 14, 15), (13, 14, 16, 17), (14, 15, 17, 18),
    (19, 20, 22, 23), (20, 21, 23, 24), (22, 23, 25, 26), (23, 24, 26, 27),
    (28, 29, 31, 32), (29, 30, 32, 33), (31, 32, 34, 35), (32, 33, 35, 36)
}

# Valid street bets (each row of three numbers)
street_bets = {
    (1, 2, 3), (4, 5, 6), (7, 8, 9),
    (10, 11, 12), (13, 14, 15), (16, 17, 18),
    (19, 20, 21), (22, 23, 24), (25, 26, 27),
    (28, 29, 30), (31, 32, 33), (34, 35, 36)
}

# Valid split bets (each pair of adjacent numbers)
split_bets = {
    (1, 2), (2, 3), (4, 5), (5, 6), (7, 8), (8, 9),
    (10, 11), (11, 12), (13, 14), (14, 15), (16, 17), (17, 18),
    (19, 20), (20, 21), (22, 23), (23, 24), (25, 26), (26, 27),
    (28, 29), (29, 30), (31, 32), (32, 33), (34, 35), (35, 36),
    # Vertical splits
    (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9),
    (7, 10), (8, 11), (9, 12), (10, 13), (11, 14), (12, 15),
    (13, 16), (14, 17), (15, 18), (16, 19), (17, 20), (18, 21),
    (19, 22), (20, 23), (21, 24), (22, 25), (23, 26), (24, 27),
    (25, 28), (26, 29), (27, 30), (28, 31), (29, 32), (30, 33),
    (31, 34), (32, 35), (33, 36)
} 
color_mapping = {
    1: "red", 2: "black", 3: "red", 4: "black", 5: "red", 6: "black",
    7: "red", 8: "black", 9: "red", 10: "black", 11: "black", 12: "red",
    13: "black", 14: "red", 15: "black", 16: "red", 17: "black", 18: "red",
    19: "red", 20: "black", 21: "red", 22: "black", 23: "red", 24: "black",
    25: "red", 26: "black", 27: "red", 28: "black", 29: "black", 30: "red",
    31: "black", 32: "red", 33: "black", 34: "red", 35: "black", 36: "red",
    0: "green" , "00": "green"
}

class Roulette:
    def __init__(self, players=None, wheel=None, dealer=None):
        self.players = players if players else []  # Initialize with provided players or an empty list
        self.wheel = wheel if wheel else self.create_wheel()
        self.dealer = dealer
        self.payouts = {  # Payout multipliers for each bet type
            "single": 35,
            "split": 17,
            "street": 11,
            "corner": 8,
            "red": 1,
            "black": 1,
            "even": 1,
            "odd": 1,
            "high": 1,
            "low": 1
        }

    def get_random_bet_choice(self, bet_type):
        """Return a random bet choice based on the bet type for NPCs."""
        if bet_type == "single":
            return str(random.choice(range(37)))
        elif bet_type in ["red", "black", "even", "odd", "high", "low"]:
            return bet_type
        elif bet_type == "split":
            return random.choice(list(split_bets))  # Use global split_bets
        elif bet_type == "street":
            return random.choice(list(street_bets))  # Use global street_bets
        elif bet_type == "corner":
            return random.choice(list(corner_bets))  # Use global corner_bets
    
    def create_wheel(self):
        """Create a roulette wheel with numbers 0-36, including 00 for American Roulette."""
        return [str(i) for i in range(37)] + ["00"]  # American Roulette wheel

    def spin_wheel(self):
        """Spin the wheel and return the winning number along with its color."""
        winning_number = random.choice(self.wheel)
        color = self.get_color(winning_number)  # Use get_color instead of is_red/is_black
        print(f"The wheel spins... and lands on {winning_number} ({color})!")
        return winning_number, color

    def get_color(self, number):
        """Return the color of a roulette number."""
        red_numbers = {"1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32", "34", "36"}
        black_numbers = {"2", "4", "6", "8", "10", "11", "13", "15", "17", "20", "22", "24", "26", "28", "29", "31", "33", "35"}
    
        if str(number) in red_numbers:
            return "red"
        elif str(number) in black_numbers:
            return "black"
        return "green"
    
    def place_bet(self, player, bet_type, amount, bet_choice):
        """Place a bet for a player and deduct the bet amount if valid."""
        if amount > player.balance:
            print(f"{player.name} does not have enough balance to place this bet.")
            return None
        player.balance -= amount
        print(f"{player.name} placed a ${amount} bet on {bet_type} {bet_choice}. Remaining balance: ${player.balance}")
        return (bet_type, bet_choice, amount)

    def parse_bet_input(self, bet_input):
        """Parse bet input and return (bet_type, bet_choice) if valid."""
        bet_type = None
        bet_choice = None

        # Check for single number bet (e.g., '5' or '00')
        if bet_input.isdigit() and 0 <= int(bet_input) <= 36:
            bet_type = "single"
            bet_choice = int(bet_input)
        elif bet_input == "00":
            bet_type = "single"
            bet_choice = "00"

        # Check for color bets (red or black)
        elif bet_input in ["red", "black"]:
            bet_type = bet_input  # 'red' or 'black'
            bet_choice = bet_input

        # Check for even/odd, high/low bets
        elif bet_input in ["even", "odd", "high", "low"]:
            bet_type = bet_input  # 'even', 'odd', 'high', or 'low'
            bet_choice = bet_input

        # Check for split bets (e.g., 'split 1,2')
        elif bet_input.startswith("split"):
            try:
                numbers = tuple(map(int, bet_input.split()[1].split(',')))
                if numbers in split_bets:  # Assuming split_bets is defined elsewhere
                    bet_type = "split"
                    bet_choice = numbers
                else:
                    print("Invalid split bet. Please enter a valid pair.")
            except (ValueError, IndexError):
                print("Invalid split format. Use format 'split X,Y'.")

        # Check for street bets (e.g., 'street 1,2,3')
        elif bet_input.startswith("street"):
            try:
                numbers = tuple(map(int, bet_input.split()[1].split(',')))
                if numbers in street_bets:  # Assuming street_bets is defined elsewhere
                    bet_type = "street"
                    bet_choice = numbers
                else:
                    print("Invalid street bet. Please enter a valid row.")
            except (ValueError, IndexError):
                print("Invalid street format. Use format 'street X,Y,Z'.")

        # Check for corner bets (e.g., 'corner 1,2,4,5')
        elif bet_input.startswith("corner"):
            try:
                numbers = tuple(map(int, bet_input.split()[1].split(',')))
                if numbers in corner_bets:  # Assuming corner_bets is defined elsewhere
                    bet_type = "corner"
                    bet_choice = numbers
                else:
                    print("Invalid corner bet. Please enter a valid square.")
            except (ValueError, IndexError):
                print("Invalid corner format. Use format 'corner X,Y,Z,W'.")

        # If valid bet was parsed, return the result
        if bet_type and bet_choice:
            return bet_type, bet_choice
        else:
            print("Invalid bet input. Please enter a valid bet type.")
            return None

    def evaluate_bets(self, winning_number, winning_color, bets):
        """Evaluate all bets and payout winners."""
        for player, (bet_type, bet_choice, amount) in bets.items():
            if self.check_win(bet_type, bet_choice, winning_number, winning_color):
                payout = amount * self.payouts[bet_type]
                player.balance += payout
                print(f"{player.name} won ${payout} with a {bet_type} bet on {bet_choice}!")
            else:
                print(f"{player.name} lost ${amount} with a {bet_type} bet on {bet_choice}.")
            print(f"{player.name}'s new balance: ${player.balance}")

    def check_win(self, bet_type, bet_choice, winning_number, winning_color):
        """Check if the player's bet wins based on the winning number and color."""
        if bet_type == "single" and str(bet_choice) == winning_number:
            return True
        elif bet_type == "red" and winning_color == "red":
            return True
        elif bet_type == "black" and winning_color == "black":
            return True
        elif bet_type == "odd" and int(winning_number) % 2 != 0:
            return True
        elif bet_type == "even" and int(winning_number) % 2 == 0:
            return True
        elif bet_type == "high" and 19 <= int(winning_number) <= 36:
            return True
        elif bet_type == "low" and 1 <= int(winning_number) <= 18:
            return True
        elif bet_type == "split" and winning_number in bet_choice:
            if bet_choice in split_bets:
                return True
        elif bet_type == "street" and winning_number in bet_choice:
            if bet_choice in street_bets:
                return True
        elif bet_type == "corner" and winning_number in bet_choice:
            # Debugging output to verify corner bet evaluation
            print(f"Evaluating corner bet: {bet_choice}, Winning number: {winning_number}")
            if bet_choice in corner_bets:
                print("Corner bet is valid and includes the winning number.")
                return True
            else:
                print("Corner bet choice is not in corner_bets.")
        return False
    
def display_bet_instructions():
    """Displays the roulette table and provides examples of valid bets."""
    display_roulette_table()  # Assuming this function displays the ASCII art of the table
    print("\nEnter your bet type and choice together. Examples:")
    print("Single number: '5'")
    print("Red/Black, Odd/Even, High/Low: 'red', 'even', 'high'")
    print("Split (two numbers): 'split 1,2'")
    print("Street (three numbers in a row): 'street 1,2,3'")
    print("Corner (four numbers in a square): 'corner 1,2,4,5'")

def play_roulette(roulette_game, player, npcs):
    """Handles the main loop for player interaction in a game of Roulette."""
    print("\nStarting a game of Roulette...")

    # Step 1: Prompt for bet amount
    while True:
        try:
            bet_amount = int(input("How much would you like to bet? (Minimum bet is $10) "))
            if bet_amount < 10:
                print("The minimum bet is $10. Please increase your bet.")
                continue
            if bet_amount > player.balance:
                print(f"You don't have enough balance. Your balance is ${player.balance}.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the bet amount.")

    # Step 2: Display instructions for bet type and choice
    display_bet_instructions()  # Show table and betting examples
    bet_input = input("Enter your bet type and choice (e.g., 'split 10,11'): ").lower()
    player_bet = roulette_game.parse_bet_input(bet_input)

    # Step 3: Validate and place the bet
    if player_bet:
        bet_type, bet_choice = player_bet
        bets = {player: roulette_game.place_bet(player, bet_type, bet_amount, bet_choice)}
    else:
        print("Invalid bet. Please try again.")
        return

    # Collect random bets from NPCs
    for npc in npcs:
        npc_bet_amount = random.randint(10, 50)
        npc_bet_type = random.choice(["single", "red", "black", "even", "odd", "high", "low", "split", "street", "corner"])
        npc_bet_choice = roulette_game.get_random_bet_choice(npc_bet_type)
        bets[npc] = roulette_game.place_bet(npc, npc_bet_type, npc_bet_amount, npc_bet_choice)

    # Spin the wheel and determine the result
    winning_number, winning_color = roulette_game.spin_wheel()

    # Evaluate all bets and display results
    roulette_game.evaluate_bets(winning_number, winning_color, bets)

    # Check if player has balance left or offer to start over
    if player.balance <= 0:
        print("Game over! You have no balance left.")
        if input("Would you like to start over? (yes/no): ").lower() == "yes":
            player.balance = 1000  # Reset balance
            play_roulette(roulette_game, player, npcs)
        else:
            print("Returning to the lobby.")
            return

    # Ask if the player wants to play again
    play_again = input("\nWould you like to play another round of Roulette or leave? (play/leave): ").lower()
    if play_again == "play":
        play_roulette(roulette_game, player, npcs)
    else:
        print("Thanks for playing! Returning to the lobby.")
# Settings menu function
def settings_menu():
    while True:
        print("\nSettings Menu:")
        print("1. Adjust Text Speed")
        print("2. Toggle Slow Text Effect")
        print("3. Return to Main Menu")

        choice = input("Choose an option: ")
        
        if choice == "1":
            try:
                new_speed = float(input("Enter new text speed (e.g., 0.05 for fast, 0.1 for slower): "))
                settings["text_speed"] = new_speed
                print(f"Text speed set to {new_speed} seconds per character.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "2":
            settings["enable_slow_text"] = not settings["enable_slow_text"]
            status = "enabled" if settings["enable_slow_text"] else "disabled"
            print(f"Slow text effect is now {status}.")

        elif choice == "3":
            print("Returning to the main menu.")
            break
        
        else:
            print("Invalid choice. Please choose a valid option.")

def roulette_instructions():
    print("\nROULETTE RULES AND STRATEGIES:")
    print("=" * 50)

    # Basic Rules
    print("\nRULES:")
    print("- In Roulette, you place bets on where a ball will land on a spinning wheel with numbered slots.")
    print("- The numbers on the wheel are 0 to 36. In American Roulette, there is also a 00 slot.")
    print("- The slots alternate between red and black, except for 0 and 00, which are green.")
    print("- You can place different types of bets, from single numbers to colors, odd/even, or groups of numbers.")

    # Types of Bets
    print("\nTYPES OF BETS:")
    print("- *Straight Bet:* Bet on a single number for a 35-to-1 payout.")
    print("- *Split Bet:* Bet on two adjacent numbers (e.g., 7 and 8) for a 17-to-1 payout.")
    print("- *Street Bet:* Bet on three consecutive numbers in a row (e.g., 1, 2, and 3) for an 11-to-1 payout.")
    print("- *Corner Bet:* Bet on four numbers that form a square (e.g., 10, 11, 13, and 14) for an 8-to-1 payout.")
    print("- *Red or Black:* Bet on whether the number will be red or black. Pays 1-to-1.")
    print("- *Odd or Even:* Bet on whether the number will be odd or even. Pays 1-to-1.")
    print("- *High or Low:* Bet on whether the number will be in the low (1-18) or high (19-36) range. Pays 1-to-1.")

    # Strategy Tips
    print("\nSTRATEGY TIPS:")
    print("- *Understand the House Edge:* American Roulette has a higher house edge (5.26%) due to the additional 00 slot, while European Roulette has a lower edge (2.7%).")
    print("- *Bet Conservatively:* Outside bets (red/black, odd/even, high/low) have lower payouts but higher odds of winning.")
    print("- *Avoid Betting Systems:* Systems like the Martingale (doubling your bet after every loss) can be risky and lead to large losses.")
    print("- *Place Combination Bets:* Consider placing a mix of inside (specific numbers) and outside bets for a balanced strategy.")
    print("- *Set a Budget:* Roulette is a game of chance; setting a budget and sticking to it can help you avoid large losses.")

    print("\nPress Enter to return to the main instructions.")
    input()

def blackjack_instructions():
    print("\nBLACKJACK RULES AND STRATEGIES:")
    print("=" * 50)

    # Basic Rules
    print("\nRULES:")
    print("- The goal of Blackjack is to beat the dealer by having a hand as close to 21 as possible, without going over.")
    print("- Number cards (2-10) are worth their face value.")
    print("- Face cards (Jack, Queen, King) are each worth 10 points.")
    print("- Aces are worth either 1 or 11 points, depending on which value keeps the hand closer to 21 without busting.")
    print("- Both the player and dealer start with two cards; one of the dealer’s cards remains hidden until the end of the round.")

    # Player Options
    print("\nPLAYER OPTIONS:")
    print("- 'Hit': Draw another card to increase your hand total.")
    print("- 'Stand': Keep your current hand and end your turn.")
    print("- 'Double Down': Double your bet after the first two cards and receive only one more card (advanced players)(not currently in the game).")
    print("- 'Split': If your first two cards are of the same value, you may split them into two separate hands, each with its own bet.")

    # Dealer Rules
    print("\nDEALER RULES:")
    print("- The dealer must hit until reaching a total of at least 17.")
    print("- The dealer will not draw if their hand totals 17 or more.")
    print("- If the dealer’s hand exceeds 21, they bust, and all remaining players win the round.")

    # Strategy Tips
    print("\nSTRATEGY TIPS:")
    print("- *Know When to Hit or Stand:* Generally, if your hand is below 12, hitting is safer. If you're close to 21, consider standing.")
    print("- *Watch the Dealer’s Card:* If the dealer's visible card is a 2-6 (low cards), they are more likely to bust, so standing on a lower total can work.")
    print("- *Use Splitting Wisely:* Split pairs of Aces or 8s to increase your chances of winning. Avoid splitting 10s or 5s.")
    print("- *Avoid Insurance Bets:* Insurance is generally a poor bet with high odds against the player.(not currently in the game)")
    print("- *Double Down on Strong Hands:* If your total is 10 or 11 and the dealer shows a low card, doubling down can increase your payout.(not currently in the game)")
    
    print("\nPress Enter to return to the main instructions.")
    input()
    
# Instructions placeholder function
def game_instructions():
    while True:
        print("\nGAMEPLAY INSTRUCTIONS:")
        print("=" * 50)
        print("Choose a game to learn more about:")
        print("1. Blackjack Rules and Strategies")
        print("2. Roulette Rules and Strategies")
        print("3. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            blackjack_instructions()
        elif choice == "2":
            roulette_instructions()
        elif choice == "3":
            print("Returning to the main menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def main_menu():
    while True:
        print_ascii(r"""
==================================================================================
******************************WELCOME TO THE**************************************
==================================================================================
██╗     ███████╗███████╗████████╗     ██████╗ █████╗ ███████╗██╗███╗   ██╗███████╗ 
██║     ██╔══██║██╔════╝╚══██╔══╝    ██╔════╝██╔══██╗██╔════╝██║████╗  ██║██╔══██║ 
██║     ██║  ██║███████╗   ██║       ██║     ███████║███████╗██║██╔██╗ ██║██║  ██║
██║     ██║  ██║╚════██║   ██║       ██║     ██╔══██║╚════██║██║██║╚██╗██║██║  ██║
███████╗███████║███████║   ██║       ╚██████╗██║  ██║███████║██║██║ ╚████║███████║
╚══════╝╚══════╝╚══════╝   ╚═╝        ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝

===================================================================================
        """)
        print("1. Start Game")
        print("2. Gameplay Instructions")
        print("3. Settings")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            main_lobby()  # Go directly to the main lobby
        elif choice == "2":
            game_instructions()  # Show instructions
        elif choice == "3":
            settings_menu()  # Open settings menu
        elif choice == "4":
            print("Thanks for visiting the Lost Casino! Goodbye.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

# Run the main menu if this script is executed directly
if __name__ == "__main__":
    main_menu()
