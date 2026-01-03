import random
from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
    icon: str
    value: int
    weight: int = 1
    wild: bool = False
    scatter: bool = False
    doubler: bool = False
    bomb: bool = False

SYMBOLS = [
    Symbol("🍒", 1, weight=10),
    Symbol("🍋", 2, weight=10),
    Symbol("🍊", 2, weight=10),

    Symbol("🍓", 3, weight=5),
    Symbol("🍇", 3, weight=5),
    Symbol("♠️", 5, weight=5),
    Symbol("♣️", 5, weight=5),
    Symbol("♥️", 5, weight=5),
    Symbol("♦️", 5, weight=5),

    Symbol("🔔", 10, weight=2),
    Symbol("🍀", 10, weight=2),
    
    Symbol("💎", 50, weight=1),
    Symbol("⭐", 50, weight=1),

    # Specials
    Symbol("🃏", 0, weight=3, wild=True),
    Symbol("💵", 5, weight=4, scatter=True),
    Symbol("🎰", 8, weight=3, scatter=True),
    Symbol("2️⃣", 0, weight=2, doubler=True),
    Symbol("❌", 0, weight=2, doubler=True),
    Symbol("💣", 0, weight=1, bomb=True)
]

class SlotMachine3x3:
    SIZE = 3
    BOMB_PENALTY = 10

    def __init__(self):
        self.board = []
        self.total_score = 0

    def spin(self):
        symbols = SYMBOLS
        weights = [s.weight for s in symbols]
        self.board = [
            [random.choices(symbols, weights=weights, k=1)[0] for _ in range(self.SIZE)]
            for _ in range(self.SIZE)
        ]

    def display(self):
        max_icon_len = max(len(s.icon) for s in SYMBOLS)
        col_width = max_icon_len + 1

        for row in self.board:
            print(" ".join(cell.icon.center(col_width) for cell in row))
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
        """
        Rules implemented:
        - If any bomb (Symbol.bomb) is present anywhere on the board, all other payouts
          for this spin are cancelled and a penalty of BOMB_PENALTY points per bomb
          is applied (gain = -BOMB_PENALTY * bomb_count).
        - Wilds (Symbol.wild) substitute for any regular symbol when checking paylines.
        - Doubler symbols (Symbol.doubler) present in a winning line double that line's payout.
          Each doubler multiplies by 2 (so 2 doublers => x4, etc).
        - Diagonal lines receive an additional x2 multiplier.
        - Scatter symbols (Symbol.scatter) pay independently; each scatter on the board adds its value to the gain.
        """
        gain = 0

        # Check bombs first
        bombs = sum(1 for row in self.board for s in row if s.bomb)
        if bombs > 0:
            penalty = bombs * self.BOMB_PENALTY
            gain = -penalty
            self.total_score += gain
            return gain

        paylines = self.get_paylines()

        # Helper: list of regular symbols (used for substitution decisions)
        regular_symbols = [
            s for s in SYMBOLS if not (s.wild or s.scatter or s.doubler or s.bomb)
        ]

        for line in paylines:
            # Identify non-special symbols in the line (regular ones)
            non_specials = [s for s in line if not (s.wild or s.scatter or s.doubler or s.bomb)]

            if not non_specials:
                # Line contains only wilds/doublers/scatters:
                # Treat as a win using the highest-value regular symbol as the substituted target.
                if not regular_symbols:
                    continue
                matched = max(regular_symbols, key=lambda s: s.value)
            else:
                # All non-specials must be the same icon to be a winning line (wilds can fill gaps)
                unique_icons = {s.icon for s in non_specials}
                if len(unique_icons) > 1:
                    # two different regular symbols -> cannot form a matching line (wilds can't reconcile different symbols)
                    continue
                matched_icon = non_specials[0].icon
                matched = next((s for s in SYMBOLS if s.icon == matched_icon), None)
                if matched is None:
                    continue

            # Count doublers in the line
            doubler_count = sum(1 for s in line if s.doubler)
            doubler_multiplier = 2 ** doubler_count

            # Diagonal extra multiplier
            diag_multiplier = 2 if self.is_diagonal(line) else 1

            line_gain = matched.value * doubler_multiplier * diag_multiplier
            gain += line_gain

        # Scatter payouts: pay independently for occurrences anywhere on the board
        scatter_total = sum(s.value for row in self.board for s in row if s.scatter)
        gain += scatter_total

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
    print(f"Gain: {'' if gain < 0 else '+'}{gain}")
    print(f"Total Score: {game.total_score}")

if __name__ == "__main__":
    main()
