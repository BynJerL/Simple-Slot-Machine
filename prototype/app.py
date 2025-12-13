"""
SLOT MACHINE APP
"""

import random

ITEMS = [("🍓", +1), 
         ("🍒", +2), 
         ("🍋", +5), 
         ("🍍", +10), 
         ("🍀", +25)]
attempt_count = 0
jackpot_count = 0
score = 0

while 1:
    attempt_count += 1
    taken = []

    for i in range(3):
        taken.append(random.choice(ITEMS))
    
    print(" | ".join(item for item,_ in taken))

    if all(x == taken[0] for x in taken):
        i = taken[0][0]
        jackpot_count += 1
        print(f"[{i} JACKPOT!!! {i}]")
        gain = 30 * taken[0][1]
    else:
        gain = sum([value for (item, value) in taken])
    
    score += gain
    print(f"Score +{gain}")

    retry = input("Retry (Y/n)? ").lower()

    if retry in ("y", "yes"):
        continue
    else:
        print("Evaluation:")
        print("Total attempt:", attempt_count)
        print("Total jackpot:", jackpot_count)
        print("Total score:", score)
        print('='*20)
        print("Thanks for playing!")
        break