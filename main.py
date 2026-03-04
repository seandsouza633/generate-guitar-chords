import random
import time
from enum import Enum
from colorama import Fore

NOTES = {
    1: "C",
    2: "Db",
    3: "D",
    4: "Eb",
    5: "E",
    6: "F",
    7: "Gb",
    8: "G",
    9: "Ab",
    10: "A",
    11: "Bb",
    12: "B"
}

GUITAR_STRINGS: list[int] = [
    5,  # E
    12, # B
    8,  # G
    3,  # D
    10, # A
    5   # E
] 

def note_normal(note: int) -> int: 
    return (note - 1) % 12 + 1

def __main__():
    n = int(input(Fore.BLUE + "How many problems would you like? "))
    c = 0
    start = time.time()
    for _ in range(n):
        # note = random.choice(list(set(GUITAR_STRINGS)))
        note: int = random.choice(list(NOTES.keys()))
        # offset = 1
        offset = random.randint(0, 16)
        answer = NOTES[(note + offset - 1) % 12 + 1]
        res = input(Fore.BLUE + f"{NOTES[note]} + {offset} = ")
        if res.lower() == answer.lower():
            c += 1
            print(Fore.GREEN + "Correct!")
        else:
            print(Fore.RED + f"Incorrect (Correct answer was {answer})")
    end = time.time()
    print(
        Fore.BLUE + "Correct answers: " +
        Fore.WHITE + f"{c} / {n} ({round(c/n*100)}%) {round(end - start, 2)}s"
        )
  
if __name__=="__main__":
    __main__()