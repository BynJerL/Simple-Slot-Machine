"""
SLOT MACHINE APP
"""

import random
from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
    icon: str
    value: int
    weight: int

ITEMS = [
    Symbol("🍓", +1, 35),
    Symbol("🍒", +2, 25),
    Symbol("🌽", +4, 15),
    Symbol("🍋", +8, 10),
    Symbol("💣", -10, 10),
    Symbol("🍀", +25, 5)
]

JACKPOT_MULTIPLIER = 10

class GameError(Exception):
    pass

class Game:
    def __init__ (self, mode = "classic"):
        self.attempt_count  = 0
        self.jackpot_count  = 0
        self.total_score    = 0
        self.spin_result    = []
        self.current_gain   = 0
        self.mode           = mode.lower()
        self.is_running     = True
    
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

    def show_spin_result (self):
        print(" | ".join(item.icon for item in self.spin_result))
    
    def show_evaluation (self):
        print("Evaluation:")
        print("Total attempt:", self.attempt_count)
        print("Total jackpot:", self.jackpot_count)
        print("Total score:", self.total_score)
        print('='*20)
        print("Thanks for playing!")

    def is_jackpot (self):
        return all(x.icon == self.spin_result[0].icon for x in self.spin_result)

    def scoring (self):
        if self.is_jackpot():
            icon = self.spin_result[0].icon
            self.jackpot_count += 1
            print(f"[{icon} JACKPOT!!! {icon}]")
            gain = JACKPOT_MULTIPLIER * self.spin_result[0].value
        else:
            gain = sum([item.value for item in self.spin_result])

        self.current_gain = gain
        self.total_score += gain

        if gain >= 0:
            print(f"Score +{gain}")
        else:
            print(f"Score {gain}")

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