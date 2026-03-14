from notes import (
    NOTES,
    note_normal,
    STANDARD_TUNING,
    convert_tuning,
    convert_from_note_str,
)
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
import re

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


def fetch_chord(numeral: str) -> tuple[str, list[int]]:
    is_major = numeral[0].isupper()

    # Determine chord type from suffix
    if "maj7" in numeral:
        chord_name = "maj7" if is_major else "minmaj7"
    elif "ø7" in numeral:
        chord_name = "m7b5"
    elif "°7" in numeral:
        chord_name = "dim7"
    elif "°" in numeral:
        chord_name = "dim"
    elif "+" in numeral:
        chord_name = "aug"
    elif "7" in numeral:
        chord_name = "dom7" if is_major else "min7"
    elif "sus2" in numeral:
        chord_name = "sus2"
    elif "sus4" in numeral:
        chord_name = "sus4"
    elif "add9" in numeral:
        chord_name = "maj_add9" if is_major else "min_add9"
    elif "add6" in numeral:
        chord_name = "maj_add6" if is_major else "min_add6"
    else:
        chord_name = "maj" if is_major else "min"

    chord_notes = list(CHORDS[chord_name])

    # Apply root accidental from prefix only
    prefix_match = re.match(r"^([b#]*)", numeral)
    prefix = prefix_match.group(1) if prefix_match else ""

    if "bb" in prefix:
        chord_notes[0] -= 2
        chord_name = "bb" + chord_name
    elif "b" in prefix:
        chord_notes[0] -= 1
        chord_name = "b" + chord_name
    elif "##" in prefix:
        chord_notes[0] += 2
        chord_name = "##" + chord_name
    elif "#" in prefix:
        chord_notes[0] += 1
        chord_name = "#" + chord_name

    return chord_name, chord_notes


def generate_progression(
    progression_str: str, base: int, scale_str: str
) -> list[tuple]:
    assert scale_str in ["major", "minor"]
    scale = generate_scale(base, SCALES[scale_str])
    # print(Fore.BLACK + str(scale))
    ret = []
    for numeral in progression_str.split(" "):
        roman_match = re.match(r'^[b#]*([IViv]+)', numeral)
        if not roman_match:
            raise ValueError(f"Could not extract Roman numeral from: {numeral}")

        roman_part = roman_match.group(1).upper()
        if roman_part not in NUMERAL_TO_NUM:
            raise ValueError(f"Unrecognized Roman numeral: {roman_part}")

        num = NUMERAL_TO_NUM[roman_part]
        chord_name, chord_notes = fetch_chord(numeral)
        ret.append(
            (
                numeral,
                f"{NOTES[scale[num - 1]]} {chord_name}",
                generate_chord(scale[num - 1], chord_notes),
            )
        )
    return ret


def main():
    root = input(
        Fore.BLUE
        + "Desired root: "
        + Fore.BLACK
        + "(leave blank for random) "
        + Fore.WHITE
    )
    if root == "":
        root = random.randint(1, 12)
        print(Fore.BLACK + f"Randomly selected root note: {NOTES[root]}")
    else:
        root = convert_from_note_str(root)
    scale_str = input(
        Fore.BLUE
        + "Key major or minor: "
        + Fore.BLACK
        + "(leave blank for random) "
        + Fore.WHITE
    ).lower()
    if scale_str == "":
        scale_str = random.choice(["major", "minor"])
        print(Fore.BLACK + f"Randomly selected scale: {scale_str}")
    progression_str = input(
        Fore.BLUE
        + "Input progression (these are case sensitive): "
        + Fore.BLACK
        + "(leave blank for random) "
        + Fore.WHITE
    ).strip()
    if progression_str == "":
        with open(f"progressions/{scale_str}_progressions.txt", "r") as f:
            progression_str = random.choice(f.readlines()).strip()
        print(Fore.BLACK + f"Randomly selected progression: {progression_str}")
    progression = generate_progression(progression_str, root, scale_str)
    tab_group_count = input(
        Fore.BLUE
        + "Desired count of tabs: "
        + Fore.BLACK
        + "(leave blank for 3) "
        + Fore.WHITE
    )
    tab_group_count = min(50, int(tab_group_count)) if tab_group_count != "" else 3
    tuning_str = input(
        Fore.BLUE
        + "Desired tuning: "
        + Fore.BLACK
        + "(leave blank for standard) "
        + Fore.WHITE
    )
    tuning = convert_tuning(tuning_str) if tuning_str != "" else STANDARD_TUNING
    tab_groups = group_alike_tabs(
        [
            generate_guitar_tabs(chord, tuning=tuning, max_fret=11, limit=999)
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
        print(Fore.WHITE + "".join([f"{NOTES[note]:^3}" for note in tuning]))
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
