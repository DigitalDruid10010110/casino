class Lobby:
    def __init__(self):
        self.games = ["Blackjack", "Roulette"]  # List of games
        self.current_game = None
        self.player_balance = 1000  # Starting balance


class Blackjack:
    def __init__(self):
        self.players = []  # Area for the players
        self.deck = self.create_deck()  # Method to create a triple deck of cards
        self.dealer = None  # Dealer
        self.bet = 0  # Player's bet amount

    def create_deck(self):
        # Logic to create a triple deck of cards
        pass


class Roulette:
    def __init__(self):
        self.players = []  # Area for the players
        self.wheel = self.create_wheel()  # Method to set up the roulette wheel
        self.dealer = None  # Dealer
        self.table = {}  # Dictionary to place bets

    def create_wheel(self):
        # Logic to create an American roulette wheel
        pass





