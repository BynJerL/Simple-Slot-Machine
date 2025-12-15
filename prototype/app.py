"""
SLOT MACHINE APP
"""

import random
from dataclasses import dataclass
from collections import Counter

@dataclass(frozen=True)
class Symbol:
    icon: str
    value: int
    weight: int

ITEMS = [
    Symbol("🍓", +1, 350),
    Symbol("🍒", +2, 250),
    Symbol("🌽", +4, 200),
    Symbol("🍋", +8, 150),
    Symbol("💣", -10, 30),
    Symbol("🍀", +25, 20)
]

TWO_OF_KIND_MULTIPLIER = 2
JACKPOT_MULTIPLIER = 5
BOMB_PENALTY = -3

class GameError(Exception):
    pass

class Game:
    def __init__ (self, mode = "classic"):
        self.attempt_count          = 0
        self.two_of_a_kind_count    = 0
        self.jackpot_count          = 0
        self.disaster_count         = 0
        self.minor_disaster_count   = 0
        self.total_score            = 0
        self.single_bomb_count      = 0
        self.spin_result            = []
        self.current_gain           = 0
        self.mode                   = mode.lower()
        self.is_running             = True
    
    @property
    def total_item (self) -> int:
        match self.mode:
            case "classic":
                return 3
            case _:
                raise GameError(f"Mode \"{self.mode}\" is not available.")

    def clean_last_spin_result (self):
        self.spin_result = []

    def spin (self):
        self.attempt_count += 1
        self.spin_result = self.get_spin()
    
    def get_spin (self) -> list[Symbol]:
        spin_result = []
        for item in range(self.total_item):
            spin_result.append(random.choices(ITEMS, weights=[item.weight for item in ITEMS])[0])
        return spin_result

    def get_symbol_counts (self):
        return Counter(item.icon for item in self.spin_result)

    def show_spin_result (self):
        print(" | ".join(item.icon for item in self.spin_result))
    
    def show_evaluation (self):
        print("Evaluation:")
        print("Total attempt:", self.attempt_count)
        print("Total jackpot:", self.jackpot_count)
        print("Total two-of-a-kind:", self.two_of_a_kind_count)
        bomb_count_total = self.disaster_count * 3 + self.minor_disaster_count * 2 + self.single_bomb_count
        print("Total bomb gained:", bomb_count_total)
        print("Total score:", self.total_score)
        print('='*20)
        print("Thanks for playing!")

    def is_jackpot (self):
        return all(x.icon == self.spin_result[0].icon for x in self.spin_result)

    def is_bomb_on_spin_result (self):
        return any(item.icon == "💣" for item in self.spin_result)

    def scoring (self):
        counts = self.get_symbol_counts()
        symbol_map = {item.icon: item for item in self.spin_result}

        if len(counts) == 1:
            symbol = symbol_map[next(iter(counts))]

            if symbol.icon == "💣":
                self.disaster_count += 1
                gain = JACKPOT_MULTIPLIER * symbol.value
                print(f"[{symbol.icon} DISASTER!!! {symbol.icon}]")
            else:
                self.jackpot_count += 1
                gain = JACKPOT_MULTIPLIER * symbol.value
                print(f"[{symbol.icon} JACKPOT!!! {symbol.icon}]")

        elif 2 in counts.values():
            icon = next(icon for icon, c in counts.items() if c == 2)
            symbol = symbol_map[icon]

            if icon == "💣":
                self.minor_disaster_count += 1
                gain = BOMB_PENALTY
                print("💣 Two bombs! Minor disaster!")
            elif "💣" in counts:
                self.single_bomb_count += 1
                gain = 0
                print("💣 Bomb detected!")
            else:
                self.two_of_a_kind_count += 1
                gain = symbol.value * TWO_OF_KIND_MULTIPLIER
                print(f"✨ Two of a kind: {icon}")
        
        elif "💣" in counts:
            self.single_bomb_count += 1
            gain = BOMB_PENALTY
            print("💣 Bomb detected!")
        
        else:
            gain = 0
            print("❌ No match")

        self.current_gain = gain
        self.total_score += gain

        print(f"Score {gain:+}")

    def end_game (self):
        self.is_running = False

def main ():
    # Setup
    slot_machine = Game()

    # Loop
    while slot_machine.is_running:
        slot_machine.spin()
        slot_machine.show_spin_result()
        slot_machine.scoring()

        retry = input("Retry (Y/n)? ").lower()

        if retry in ("y", "yes"):
            continue
        else:
            slot_machine.show_evaluation()
            slot_machine.end_game()

if __name__ == "__main__":
    main()