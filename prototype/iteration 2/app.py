import random
from dataclasses import dataclass

POSSIBLE_MODES = {"1x3", "3x3", "1x5", "3x5"}
current_mode = "1x5"

@dataclass(frozen=True)
class Symbol:
    icon: str
    value: int

SYMBOLS = [
    Symbol("🍒", 1),
    Symbol("🍓", 2),
    Symbol("🍊", 3),
    Symbol("🍇", 4),
    Symbol("🍋", 5),
    Symbol("🔔", 6),
    Symbol("🍀", 7),
    Symbol("💎", 8)
]

def roll():
    match current_mode:
        case "1x3":
            for i in range(3):
                print(random.choice(SYMBOLS).icon, end="")
            print()

        case "3x3":
            for i in range(3):
                for j in range(3):
                    print(random.choice(SYMBOLS).icon, end="")
                print()

        case "1x5":
            for i in range(5):
                print(random.choice(SYMBOLS).icon, end="")
            print()

        case "3x5":
            for i in range(3):
                for j in range(5):
                    print(random.choice(SYMBOLS).icon, end="")
                print()

        case _:
            raise ValueError(f"Invalid game mode \'{current_mode}\'")

def main():
    roll()

if __name__ == "__main__":
    main()