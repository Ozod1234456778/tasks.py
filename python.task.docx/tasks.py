class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.goals = 0  # yoki chessda yutuqlar

    def __str__(self):
        return f"{self.name} - {self.points} pts"


class Referee:
    def __init__(self, name):
        self.name = name

    def decide_winner(self, player1, player2):
        import random
        winner = random.choice([player1, player2, None])
        return winner


class Match:
    def __init__(self, player1, player2, referee):
        self.player1 = player1
        self.player2 = player2
        self.referee = referee

    def play(self):
        winner = self.referee.decide_winner(self.player1, self.player2)
        if winner:
            winner.points += 3
            print(f"{winner.name} won the match!")
        else:
            self.player1.points += 1
            self.player2.points += 1
            print("Draw!")
 2. Strategy Pattern: RoundRobin, Knockout (turli turnir formatlari)

class TournamentStrategy:
    def play_matches(self, players, referee):
        raise NotImplementedError


class RoundRobin(TournamentStrategy):
    def play_matches(self, players, referee):
        matches = []
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                match = Match(players[i], players[j], referee)
                match.play()


class Knockout(TournamentStrategy):
    def play_matches(self, players, referee):
        import random
        round_num = 1
        while len(players) > 1:
            print(f"--- Round {round_num} ---")
            random.shuffle(players)
            next_round = []
            for i in range(0, len(players), 2):
                if i + 1 < len(players):
                    match = Match(players[i], players[i + 1], referee)
                    match.play()
                    if players[i].points > players[i + 1].points:
                        next_round.append(players[i])
                    else:
                        next_round.append(players[i + 1])
            players = next_round
            round_num += 1
 3. Tournament Class

class Tournament:
    def __init__(self, name, strategy):
        self.name = name
        self.players = []
        self.strategy = strategy
        self.referee = Referee("Default Ref")

    def add_player(self, player):
        self.players.append(player)

    def start(self):
        print(f"Starting Tournament: {self.name}")
        self.strategy.play_matches(self.players, self.referee)
        self.show_standings()

    def show_standings(self):
        sorted_players = sorted(self.players, key=lambda x: x.points, reverse=True)
        print("=== Final Standings ===")
        for player in sorted_players:
            print(player)
 4. Test qilish (Admin CLI oddiy holatda)

if __name__ == "__main__":
    # Create Players
    p1 = Player("Alice")
    p2 = Player("Bob")
    p3 = Player("Charlie")
    p4 = Player("Diana")

    # Choose Strategy
    strategy = RoundRobin()  # yoki Knockout()

    # Create Tournament
    tour = Tournament("Summer Cup", strategy)

    # Add Players
    for p in [p1, p2, p3, p4]:
        tour.add_player(p)

    # Start Tournament
    tour.start()
