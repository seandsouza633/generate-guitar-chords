import random
import time
from colorama import Fore
import re

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
    12: "B",
}

NOTES_SHARP = {
    1: "C",
    2: "C#",
    3: "D",
    4: "D#",
    5: "E",
    6: "F",
    7: "F#",
    8: "G",
    9: "G#",
    10: "A",
    11: "A#",
    12: "B",
}

STANDARD_TUNING: list[int] = [
    5,  # E
    10,  # A
    3,  # D
    8,  # G
    12,  # B
    5,  # E
]


def note_normal(note: int) -> int:
    return (note - 1) % 12 + 1


def normalize_note_str(note_str: str) -> str:
    note_str = note_str[0].upper() + note_str[1:].lower()
    assert note_str in list(NOTES.values()) + list(NOTES_SHARP.values())
    return note_str


def convert_from_note_str(note_str: str) -> int:
    note_str = normalize_note_str(note_str)
    if "#" in note_str:
        note_str = flatten_accidental(note_str)
    try:
        return next(k for k in NOTES.keys() if NOTES[k] == note_str)
    except StopIteration:
        print(Fore.RED + "No key found.")


def flatten_accidental(note_str: str) -> str:
    if "#" in note_str:
        return NOTES[convert_from_note_str(note_str)]
    return normalize_note_str(note_str)  # natural note


def convert_tuning(tuning_str: str, debug=False) -> list[int]:
    assert re.match(r"^([A-G][b#]? *)+$", tuning_str)
    notes = re.findall(r'[A-G][b#]?', tuning_str)
    if debug:
        print(Fore.BLACK + str(notes))
    assert len(notes) == 6 and all(len(note)<=2 for note in notes)
    return [convert_from_note_str(note) for note in notes]


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
        Fore.BLUE
        + "Correct answers: "
        + Fore.WHITE
        + f"{c} / {n} ({round(c / n * 100)}%) {round(end - start, 2)}s"
    )


if __name__ == "__main__":
    __main__()
