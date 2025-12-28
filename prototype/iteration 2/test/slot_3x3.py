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

roll_result = []
win_point = 0

for i in range(3):
    roll_result_row = []
    for j in range(3):
        rolled_symbol = random.choice(SYMBOLS)
        roll_result_row.append(rolled_symbol)
    roll_result.append(roll_result_row)

for row in roll_result:
    for cell in row:
        print(cell.icon, end="")
    print()

for row in roll_result:
    if row[0].icon == row[1].icon == row[2].icon:
        win_point += 1

for i in range(len(roll_result)):
    if roll_result[0][i] == roll_result[1][i] == roll_result[2][i]:
        win_point += 1

if roll_result[0][0] == roll_result[1][1] == roll_result[2][2]:
    win_point += 1

if roll_result[0][2] == roll_result[1][1] == roll_result[2][0]:
    win_point += 1

print(win_point)