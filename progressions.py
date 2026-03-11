from notes import NOTES, note_normal
from scales import SCALES, generate_scale
from chords import (
    CHORDS,
    # ATTS,
    generate_chord,
    generate_guitar_tabs,
    printable_tab,
    group_alike_tabs,
)
from colorama import Fore
import random

NUMERAL_TO_NUM = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
}

MODES = {
    "major": ["maj", "min", "min", "maj", "maj", "min", "dim"],
    "minor": ["min", "dim", "maj", "min", "min", "maj", "maj"],
}

GREEK_MODES = {
    "ionian": ["maj", "min", "min", "maj", "maj", "min", "dim"],
    "dorian": ["min", "min", "maj", "maj", "min", "dim", "maj"],
    "phrygian": ["min", "maj", "maj", "min", "dim", "maj", "min"],
    "lydian": ["maj", "maj", "min", "dim", "maj", "min", "min"],
    "mixolydian": ["maj", "min", "dim", "maj", "min", "min", "maj"],
    "aeolian": ["min", "dim", "maj", "min", "min", "maj", "maj"],
    "locrian": ["dim", "maj", "min", "min", "maj", "maj", "min"],
}

DIVIDER = "-----"

def generate_progression(progression_str: str, base: int, scale_str: str) -> list[tuple]:
    assert all(
        num.upper() in NUMERAL_TO_NUM.keys() for num in progression_str.split(" ")
    )
    assert scale_str in ["major", "minor"]
    scale = generate_scale(base, SCALES[scale_str])
    # print(Fore.BLACK + str(scale))
    ret = []
    for numeral in progression_str.split(" "):
        num = NUMERAL_TO_NUM[numeral.upper()]
        # print(Fore.BLACK + str(num))
        chord_name = random.choice(
            list(filter(lambda c: MODES[scale_str][num - 1] in c, set(CHORDS.keys())))
        )
        # chord_name = MODES[scale_str][num - 1]
        chord_notes = CHORDS[chord_name]
        # print(chord_notes)
        # print(f"Root: {NOTES[scale[num - 1]]}")
        ret.append(
            (
                numeral,
                f"{NOTES[scale[num - 1]]}{chord_name}",
                generate_chord(scale[num - 1], chord_notes),
            )
        )
    return ret


def main():
    root = input(Fore.BLUE + "Desired root: " + Fore.WHITE).lower()
    try:
        root = next(k for k in NOTES.keys() if NOTES[k].lower() == root)
    except StopIteration:
        print(Fore.RED + "No key found.")
        return
    scale_str = input(Fore.BLUE + "Key major or minor: " + Fore.WHITE).lower()
    progression_str = input(Fore.BLUE + "Input progression: " + Fore.WHITE).rstrip()
    if progression_str == "":
        with open(f"progressions/{scale_str}_progressions.txt", "r") as f:
            progression_str = random.choice(f.readlines()).rstrip()
        print(Fore.BLACK + f"Randomly selected progression: {progression_str}")
    progression = generate_progression(progression_str, root, scale_str)
    tab_group_count = input(Fore.BLUE + "Desired count of tabs: " + Fore.WHITE)
    tab_group_count = int(tab_group_count) if tab_group_count != "" else 1
    tab_groups = group_alike_tabs(
        [
            generate_guitar_tabs(chord, limit=999)
            for chord_numeral, chord_name, chord in progression
        ]
    )[:tab_group_count]

    print(Fore.WHITE + DIVIDER)
    print(
        Fore.WHITE
        + f"Progression: {' '.join([chord_numeral for chord_numeral, chord_name, chord in progression])}"
    )
    for i, tab_group in enumerate(tab_groups):
        print(Fore.GREEN + f"Tab group {i + 1}")
        print(Fore.WHITE + " E  A  D  G  B  E")
        for j, position in enumerate(progression):
            chord_numeral, chord_name, chord = position
            print(
                Fore.CYAN
                + f"{chord_numeral} {chord_name}"
                + Fore.BLUE
                + f" -> {' '.join([NOTES[note_normal(n)] for n in chord])}"
            )
            print(Fore.BLACK + printable_tab(tab_group[j]))
    print(Fore.WHITE + DIVIDER)


if __name__ == "__main__":
    main()
