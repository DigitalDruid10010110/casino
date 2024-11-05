class Lobby:
    def __init__(self):
        self.game("Blackjack", "Roulette")
        self.current_game = None
        self.player_balance = 1000 #starting balance
        