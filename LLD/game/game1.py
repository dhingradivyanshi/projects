import random
from collections import deque

class Jump:
    def __init__(self, start: int, end: int, jump_type: str):
        self.start = start
        self.end = end
        self.type = jump_type  # 'snake' or 'ladder'


class Board:
    def __init__(self, size: int, jumps: list[Jump]):
        self.size = size
        self.jumps = {jump.start: jump for jump in jumps}

    def get_jump(self, position):
        return self.jumps.get(position)


class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 0

    def __repr__(self):
        return f"Player({self.name}, Pos: {self.position})"


class Dice:
    def __init__(self, faces=6):
        self.faces = faces

    def roll(self):
        return random.randint(1, self.faces)


class JumpStrategy:
    def apply_jump(self, board: Board, position: int) -> int:
        jump = board.get_jump(position)
        if jump:
            print(f"Hit a {jump.type.upper()}! Moving from {jump.start} to {jump.end}")
            return jump.end
        return position


class GameRuleEngine:
    def __init__(self, jump_strategy: JumpStrategy):
        self.jump_strategy = jump_strategy

    def move_player(self, board: Board, current_pos: int, roll: int) -> int:
        new_pos = current_pos + roll
        if new_pos > board.size:
            return current_pos  # overshoot
        return self.jump_strategy.apply_jump(board, new_pos)


class GameEngine:
    def __init__(self, board: Board, players: list[Player], dice: Dice, rule_engine: GameRuleEngine):
        self.board = board
        self.players = deque(players)
        self.dice = dice
        self.rules = rule_engine

    def play(self):
        while True:
            current_player = self.players.popleft()
            roll = self.dice.roll()
            print(f"{current_player.name} rolls a {roll}")
            new_pos = self.rules.move_player(self.board, current_player.position, roll)
            current_player.position = new_pos
            print(f"  -> {current_player.name} moves to {new_pos}\n")

            if new_pos == self.board.size:
                print(f"{current_player.name} wins the game!")
                break
            self.players.append(current_player)


# Example Setup and Run
if __name__ == "__main__":
    snakes_and_ladders = [
        Jump(3, 22, "ladder"),
        Jump(5, 8, "ladder"),
        Jump(11, 26, "ladder"),
        Jump(20, 29, "ladder"),
        Jump(27, 1, "snake"),
        Jump(21, 9, "snake"),
        Jump(17, 4, "snake"),
    ]

    board = Board(size=30, jumps=snakes_and_ladders)
    players = [Player("Alice"), Player("Bob")]
    dice = Dice()
    jump_strategy = JumpStrategy()
    rule_engine = GameRuleEngine(jump_strategy)
    game = GameEngine(board, players, dice, rule_engine)

    game.play()