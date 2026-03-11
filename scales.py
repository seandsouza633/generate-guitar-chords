from notes import NOTES
from colorama import Fore

SCALES = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2],
}

GREEK_SCALES = {
    "ionian": [2, 2, 1, 2, 2, 2, 1],
    "dorian": [2, 1, 2, 2, 2, 1, 2],
    "phrygian": [1, 2, 2, 2, 1, 2, 2],
    "lydian": [2, 2, 2, 1, 2, 2, 1],
    "mixolydian": [2, 2, 1, 2, 2, 1, 2],
    "aeolian": [2, 1, 2, 2, 1, 2, 2],
    "locrian": [1, 2, 2, 1, 2, 2, 2],
}


def generate_scale(base: int, intervals: list[int]):
    ret = []
    note = base
    for i in range(len(intervals)):
        ret.append(note)
        note += intervals[i]
        if note > 12:
            note -= 12
    return ret


def main():
    root = input(Fore.BLUE + "Desired key: " + Fore.WHITE).lower()
    try:
        note = next(k for k in NOTES.keys() if NOTES[k].lower() == root)
    except StopIteration:
        print(Fore.RED + "No key found.")
        return
    root = NOTES[note]
    for scale, intervals in GREEK_SCALES.items():
        ret = [NOTES[n] for n in generate_scale(note, intervals)]
        print(Fore.BLUE + f"{root} {scale:11} {' '.join(ret)}")


if __name__ == "__main__":
    main()
