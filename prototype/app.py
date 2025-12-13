"""
SLOT MACHINE APP
"""

import random

ITEMS = ["🍓", "🍒", "🍋", "🍍", "🍀"]
attempt_count = 0
jackpot_count = 0
score = 0

while 1:
    taken = []

    for i in range(3):
        taken.append(random.choice(ITEMS))
    
    print(*taken, sep="|")

    if all(x == taken[0] for x in taken):
        i = taken[0]
        jackpot_count += 1
        print(f"[{i} JACKPOT! {i}]")
    
    retry = input("Retry (Y/n)? ").lower()

    if retry in ("y", "yes"):
        continue
    else:
        print("Evaluation:")
        print("Total attempt:", attempt_count)
        print("Total jackpot:", jackpot_count)
        print('='*20)
        print("Thanks for playing!")
        break