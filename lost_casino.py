import random
from npc_names import npc_names

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
        self.dealer = dealer  # Dealer
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

class Roulette:
    def __init__(self, players=None, wheel=None, dealer=None, table=None):
        self.players = players if players else []  # Area for the players
        self.wheel = wheel if wheel else self.create_wheel()  # Method to set up the roulette wheel
        self.dealer = dealer  # Dealer
        self.table = table if table else {}  # Dictionary to place bets

    def create_wheel(self):
        # Logic to create an American roulette wheel
        pass

class NPCPlayer:
    def __init__(self, balance=1000):
        self.name, self.details = self.assign_random_name()  # Assign a random name and details
        self.hands = [[]]  # A list of hands, starting with one empty hand
        self.balance = balance  # Starting balance
        self.is_active = True  # Indicates if the player is active in a game
        self.current_game = None  # Track the game the NPC is currently playing

    def assign_random_name(self):
        """Assign a random name from the *Name* dictionary and return the name and details."""
        name = random.choice(list(npc_names.keys()))
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
        

class Player:
    def __init__(self, name, balance=1000):
        self.name = name
        self.hands = [[]]  # A list of hands, starting with one empty hand
        self.balance = balance  # Starting balance
        self.is_active = True  # Indicates if the player is active in a game
        self.current_game = None  # Track the game the player is currently playing

    def join_game(self, games):
        """Prompt the player to choose a game and join it."""
        print(f"Available games: {', '.join(games)}")
        game_name = input("Which game would you like to join? ").capitalize()

        if game_name in games:
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
            decision = input(f"{self.name}, do you want to 'hit', 'stand', or 'split' (if possible)? ").lower()
            if decision == "split" and self.can_split(hand_index):
                self.split_hand()
                return "split"
            return decision
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
        


