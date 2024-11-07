import random
import time
import builtins

# Save the original print function
original_print = builtins.print

# Defines the slow_print version of print
def slow_print(*args, delay=0.05, **kwargs):
    text = " ".join(str(arg) for arg in args)
    for char in text:
        original_print(char, end='', flush=True, **kwargs)
        time.sleep(delay)
    original_print()  # Move to the next line

# Replace the built-in print with slow_print
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

class Roulette:
    def __init__(self, players=None, wheel=None, dealer=None):
        self.players = players if players else []  # Area for the players
        self.wheel = wheel if wheel else self.create_wheel()  # Create the roulette wheel
        self.dealer = dealer  # Dealer (not really needed for Roulette but kept for consistency)

    def create_wheel(self):
        """Create a roulette wheel with numbers 0-36, including 00 for American Roulette."""
        return [str(i) for i in range(37)] + ["00"]  # American Roulette wheel

    def spin_wheel(self):
        """Spin the wheel and return the winning number along with its color."""
        winning_number = random.choice(self.wheel)
        color = "red" if self.is_red(winning_number) else "black" if self.is_black(winning_number) else "green"
        print(f"The wheel spins... and lands on {winning_number} ({color})!")
        return winning_number

    def is_red(self, number):
        """Check if a number is red. Red numbers on an American Roulette wheel."""
        red_numbers = {"1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32", "34", "36"}
        return number in red_numbers

    def is_black(self, number):
        """Check if a number is black. Black numbers on an American Roulette wheel."""
        black_numbers = {"2", "4", "6", "8", "10", "11", "13", "15", "17", "20", "22", "24", "26", "28", "29", "31", "33", "35"}
        return number in black_numbers

    def place_bet(self, player, bet_type, amount):
        """Place a bet for a player if they have enough balance."""
        if amount > player.balance:
            print(f"{player.name} does not have enough balance to place this bet.")
            return None
        player.balance -= amount
        print(f"{player.name} placed a ${amount} bet on {bet_type}. Remaining balance: ${player.balance}")
        return (bet_type, amount)

    def evaluate_bets(self, winning_number, bets):
        """Evaluate all bets and payout winners."""
        for player, (bet_type, amount) in bets.items():
            if bet_type == winning_number:  # Bet on a specific number
                payout = amount * 35  # Payout for a straight bet
                player.balance += payout
                print(f"{player.name} wins ${payout} on a straight bet!")
            elif bet_type == "even" and winning_number.isdigit() and int(winning_number) % 2 == 0:
                payout = amount * 2
                player.balance += payout
                print(f"{player.name} wins ${payout} on an even bet!")
            elif bet_type == "odd" and winning_number.isdigit() and int(winning_number) % 2 != 0:
                payout = amount * 2
                player.balance += payout
                print(f"{player.name} wins ${payout} on an odd bet!")
            elif bet_type == "red" and self.is_red(winning_number):
                payout = amount * 2
                player.balance += payout
                print(f"{player.name} wins ${payout} on a red bet!")
            elif bet_type == "black" and self.is_black(winning_number):
                payout = amount * 2
                player.balance += payout
                print(f"{player.name} wins ${payout} on a black bet!")
            else:
                print(f"{player.name} loses their ${amount} bet.")

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

    def split_hand(self):
        """Split the player's hand into two separate hands if they have a pair."""
        if self.can_split():
            card1, card2 = self.hands[0]  # Get the two cards
            self.hands = [[card1], [card2]]  # Split into two separate hands
            print(f"{self.name} has split their hand into two hands.")
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
       
def play_roulette(roulette_game, player, npcs):
    print("\nStarting a game of Roulette...")

    # Collect bets from the player
    bets = {}
    while True:
        try:
            bet_amount = int(input("How much would you like to bet? (Minimum bet is $10) "))
            
            # Check for minimum bet
            if bet_amount < 10:
                print("The minimum bet is $10. Please increase your bet.")
                continue  # Retry if the bet is below minimum
            
            # Check if the player has enough balance
            if bet_amount > player.balance:
                print(f"You don't have enough balance to place this bet. Your balance is ${player.balance}.")
                continue  # Retry if the bet is above available balance
            
            # If both conditions are met, the bet is valid
            break

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Ask for the bet type
    while True:
        bet_type = input("What would you like to bet on? (number 0-36, 00, 'even', 'odd', 'red', or 'black'): ").lower()
        if bet_type in roulette_game.wheel or bet_type in ["even", "odd", "red", "black"]:
            # Add player’s bet to the bets dictionary
            bets[player] = roulette_game.place_bet(player, bet_type, bet_amount)
            break
        else:
            print("Invalid bet type. Please choose a number 0-36, 00, 'even', 'odd', 'red', or 'black'.")

    # Collect bets from NPCs
    for npc in npcs:
        npc_bet_amount = random.randint(10, 50)  # NPCs bet randomly between $10 and $50
        npc_bet_type = random.choice(roulette_game.wheel + ["even", "odd", "red", "black"])  # NPCs choose a random bet
        bets[npc] = roulette_game.place_bet(npc, npc_bet_type, npc_bet_amount)
        print(f"{npc.get_full_name()} placed a ${npc_bet_amount} bet on {npc_bet_type}. Remaining balance: ${npc.balance}")

    # Spin the wheel and determine the winning number
    winning_number = roulette_game.spin_wheel()

    # Evaluate all bets and payout winners
    roulette_game.evaluate_bets(winning_number, bets)

    # Check if player balance is zero and offer to start over
    if player.balance <= 0:
        print("Game over! You have no balance left.")
        if input("Would you like to start over? (yes/no): ").lower() == "yes":
            player.balance = 1000  # Reset balance
            play_roulette(roulette_game, player, npcs)
        else:
            print("Returning to the lobby.")
            return

    # Ask the player if they want to play again or leave
    while True:
        play_again = input("\nWould you like to play another round of Roulette or leave? (play/leave): ").lower()
        if play_again == "play":
            play_roulette(roulette_game, player, npcs)
            break
        elif play_again == "leave":
            print("Thanks for playing! Returning to the lobby.")
            break
        else:
            print("Invalid choice. Please enter 'play' or 'leave'.")

if __name__ == "__main__":
    main_lobby()