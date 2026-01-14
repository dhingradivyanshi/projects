import random
from abc import ABC, abstractmethod
from collections import deque
from queue import Queue
Queue()
class Dice(ABC):
    @abstractmethod
    def roll(self) -> int:
        pass


class StandardDice(Dice):
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class GameEndStrategy(ABC):
    @abstractmethod
    def should_end(self, winners, players):
        pass


class FirstWinnerStrategy(GameEndStrategy):
    def should_end(self, winners, players):
        return len(winners) >= 1


class EliminateUntilTwoStrategy(GameEndStrategy):
    def should_end(self, winners, players):
        return len(players) - len(winners) <= 2


class TurnManager(ABC):
    @abstractmethod
    def next_player(self):
        pass

    @abstractmethod
    def has_more_turns(self):
        pass


class RoundRobinTurnManager(TurnManager):
    def __init__(self, players):
        self._queue = deque(players)

    def next_player(self):
        player = self._queue.popleft()
        self._queue.append(player)
        return player

    def has_more_turns(self):
        return True


class Board:
    def __init__(self, size, snakes=None, ladders=None):
        self.size = size
        self.snakes = snakes or {}
        self.ladders = ladders or {}

    def get_final_position(self, position):
        while position in self.snakes or position in self.ladders:
            if position in self.snakes:
                position = self.snakes[position]
            elif position in self.ladders:
                position = self.ladders[position]
        return position


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0

    def move(self, steps):
        self.position += steps

    def __repr__(self):
        return f"{self.name} at {self.position}"


class SnakeAndLadderGame:
    def __init__(self, players, board, dice, end_strategy, turn_manager):
        self.players = players
        self.board = board
        self.dice = dice
        self.end_strategy = end_strategy
        self.turn_manager = turn_manager
        self.winners = []

    def play(self):
        while not self.end_strategy.should_end(self.winners, self.players):
            player = self.turn_manager.next_player()

            if player in self.winners:
                continue

            roll = self.dice.roll()
            player.move(roll)
            player.position = self.board.get_final_position(player.position)

            print(f"{player.name} rolled a {roll} and moved to {player.position}")

            if player.position >= self.board.size:
                print(f"{player.name} has won!")
                self.winners.append(player)


# Example Usage
if __name__ == "__main__":
    snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
    ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    board = Board(size=100, snakes=snakes, ladders=ladders)
    players = [Player("Alice"), Player("Bob"), Player("Charlie")]
    dice = StandardDice()
    end_strategy = FirstWinnerStrategy()  # Change to EliminateUntilTwoStrategy() if needed
    turn_manager = RoundRobinTurnManager(players)

    game = SnakeAndLadderGame(players, board, dice, end_strategy, turn_manager)
    game.play()
