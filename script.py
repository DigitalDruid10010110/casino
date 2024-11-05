import random



class Lobby:
    def __init__(self):
        self.games = ["Blackjack", "Roulette"]  # List of games
        self.current_game = None
        self.player_balance = 1000  # Starting balance


class Blackjack:
    def __init__(self):
        self.players = []  # Area for the players
        self.full_deck = self.create_deck()  # Initial full deck (shuffled)
        self.trash_deck = []  # Discarded cards
        self.dealer = None  # Dealer
        self.bet = 0  # Player's bet amount

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        single_deck = [(value, suit) for suit in suits for value in values]

        triple_deck = single_deck * 3

        # Shuffle the deck
        random.shuffle(triple_deck)
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
    def __init__(self):
        self.players = []  # Area for the players
        self.wheel = self.create_wheel()  # Method to set up the roulette wheel
        self.dealer = None  # Dealer
        self.table = {}  # Dictionary to place bets

    def create_wheel(self):
        # Logic to create an American roulette wheel
        pass





