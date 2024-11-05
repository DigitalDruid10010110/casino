import random

class Lobby:
    def __init__(self, games=None, current_game=None, player_balance=1000):
        self.games = games if games else ["Blackjack", "Roulette"]  # Use provided games or default
        self.current_game = current_game
        self.player_balance = player_balance  # Starting balance

class Blackjack:
    def __init__(self, players=None, full_deck=None, trash_deck=None, dealer=None, bet=0):
        self.players = players if players else []  # Area for the players
        self.full_deck = full_deck if full_deck else self.create_deck()  # Initial full deck (shuffled)
        self.trash_deck = trash_deck if trash_deck else []  # Discarded cards
        self.dealer = dealer  # Dealer
        self.bet = bet  # Player's bet amount

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
    def __init__(self, name, hand=None, balance=1000, is_active=True, current_game=None):
        self.name = name
        self.hand = hand if hand else []  # Cards in the player's hand (for card games)
        self.balance = balance  # Starting balance
        self.is_active = is_active  # Indicates if the player is active in a game
        self.current_game = current_game  # Track the game the NPC is currently playing

    def join_game(self, game_name):
        """Assign the NPC to a game."""
        self.current_game = game_name
        print(f"{self.name} has joined {self.current_game}.")

    def leave_game(self):
        """Remove the NPC from the current game."""
        print(f"{self.name} has left {self.current_game}.")
        self.current_game = None

    def receive_card(self, card):
        """Add a card to the player's hand (for card games)."""
        self.hand.append(card)

    def clear_hand(self):
        """Clear the player's hand (for starting a new round in a card game)."""
        self.hand = []

    def make_decision(self):
        """Decide what action to take. (Example for Blackjack)"""
        if self.current_game == "Blackjack":
            hand_value = self.calculate_hand_value()
            return "hit" if hand_value < 17 else "stand"
        # Additional decision-making logic can be added for other games
        return "stand"

    def calculate_hand_value(self):
        """Calculate the total value of the hand (specific to Blackjack)."""
        value = 0
        ace_count = 0
        for card in self.hand:
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