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

NUMERAL_TO_NUM = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
}

COMMON_PROGRESSIONS = []


def generate_progression(progression_str: str, scale: list) -> list[tuple]:
    assert all(
        num.upper() in NUMERAL_TO_NUM.keys() for num in progression_str.split(" ")
    )
    # print(Fore.BLACK + str(scale))
    ret = []
    for numeral in progression_str.split(" "):
        num = NUMERAL_TO_NUM[numeral.upper()]
        if numeral == numeral.upper():
            chord_notes = CHORDS["maj"]
            # print(f"{num} maj")
        else:
            chord_notes = CHORDS["min"]
            # print(f"{num} min")
        # print(chord_notes)
        # print(f"Root: {NOTES[scale[num - 1]]}")
        ret.append((numeral, generate_chord(scale[num - 1], scale, chord_notes)))
    return ret


def main():
    root = input(Fore.BLUE + "Desired root: " + Fore.WHITE).lower()
    try:
        root = next(k for k in NOTES.keys() if NOTES[k].lower() == root)
    except StopIteration:
        print(Fore.RED + "No key found.")
        return
    scale_str = input(Fore.BLUE + "Key major or minor: " + Fore.WHITE).lower()
    assert scale_str.lower() in ["major", "minor"]
    scale = generate_scale(root, SCALES[scale_str])
    progression_str = input(Fore.BLUE + "Input progression: " + Fore.WHITE)
    progression = generate_progression(progression_str, scale)
    tab_group_count = input(Fore.BLUE + "Desired count of tabs: " + Fore.WHITE)
    tab_group_count = int(tab_group_count) if tab_group_count != "" else 1
    tab_groups = group_alike_tabs(
        [generate_guitar_tabs(chord, limit=999) for chord_numeral, chord in progression],
        True
    )[:tab_group_count]
    for i, tab_group in enumerate(tab_groups):
        print(Fore.GREEN + f"Tab group {i + 1}")
        print(Fore.WHITE + " E  A  D  G  B  E")
        for j, position in enumerate(progression):
            chord_numeral, chord = position
            print(
                Fore.CYAN
                + chord_numeral
                + Fore.BLUE
                + f" -> {' '.join([NOTES[note_normal(n)] for n in chord])}"
            )
            print(Fore.BLACK + printable_tab(tab_group[j]))


if __name__ == "__main__":
    main()
