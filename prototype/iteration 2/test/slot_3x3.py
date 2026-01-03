import random
from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
    icon: str
    value: int

SYMBOLS = [
    Symbol("🍒", 1),
    Symbol("🍓", 2),
    Symbol("🍇", 3),
    Symbol("🍋", 5),
    Symbol("🔔", 6),
    Symbol("🍀", 7),
    Symbol("💎", 8)
]

class SlotMachine3x3:
    SIZE = 3

    def __init__(self):
        self.board = []
        self.total_score = 0

    def spin(self):
        self.board = [
            [random.choice(SYMBOLS) for _ in range(self.SIZE)]
            for _ in range(self.SIZE)
        ]

    def display(self):
        for row in self.board:
            print(" ".join(cell.icon for cell in row))
        print()

    def get_paylines(self):
        lines = []

        # Rows
        for r in range(self.SIZE):
            lines.append([self.board[r][c] for c in range(self.SIZE)])

        # Columns (Unused)
        # for c in range(self.SIZE):
        #     lines.append([self.board[r][c] for r in range(self.SIZE)])

        # Diagonals
        lines.append([self.board[i][i] for i in range(self.SIZE)])
        lines.append([self.board[i][self.SIZE - 1 - i] for i in range(self.SIZE)])

        return lines

    def evaluate(self):
        gain = 0
        paylines = self.get_paylines()

        for line in paylines:
            if all(symbol == line[0] for symbol in line):
                multiplier = 2 if self.is_diagonal(line) else 1
                line_gain = line[0].value * multiplier
                gain += line_gain

        self.total_score += gain
        return gain

    def is_diagonal(self, line):
        diag1 = [self.board[i][i] for i in range(self.SIZE)]
        diag2 = [self.board[i][self.SIZE - 1 - i] for i in range(self.SIZE)]
        return line == diag1 or line == diag2


def main():
    game = SlotMachine3x3()

    game.spin()
    game.display()
    gain = game.evaluate()
    print(f"Gain: +{gain}")
    print(f"Total Score: {game.total_score}")

if __name__ == "__main__":
    main()
