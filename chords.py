from notes import (
    NOTES,
    STANDARD_TUNING,
    note_normal,
    convert_from_note_str,
    convert_tuning,
)
from scales import SCALES, generate_scale
from colorama import Fore
import random
import itertools
import statistics
# import math

CHORDS = {
    "maj": [0, 4, 7],
    "min": [0, 3, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
    "maj7": [0, 4, 7, 11],
    "min7": [0, 3, 7, 10],
    "dim7": [0, 3, 6, 9],
    "dom7": [0, 4, 7, 10],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
}

MAJOR_CHORDS = {k: v for k, v in CHORDS.items() if "maj" in k}

REGULAR_CHORDS = {k: v for k, v in CHORDS.items() if "sus" not in k}


def generate_chord(base: int, chord_notes) -> list[int]:
    return [note_normal(base + delta) for delta in chord_notes]


ALL_STRING_COMBOS = [(i, i + n) for n in range(6, 2, -1) for i in range(7 - n)]


def insert_over_x_array(start: int, arr: list):
    ret = [None for _ in range(6)]
    ret[start:start] = arr
    ret = ret[:6]
    # print(printable_tab(ret))
    return ret


def quantify(cond, iterable):
    return sum(map(cond, iterable))


def printable_tab(tab) -> str:
    return " ".join([" x" if t is None else f"{t:2}" for t in tab])


def generate_guitar_tabs(
    chord: list[int], tuning=STANDARD_TUNING, limit=10, debug=False
) -> list[tuple]:
    all_string_positions = []
    for string in tuning:
        all_string_positions.append(
            [fret for fret in range(0, 18) if note_normal(string + fret) in chord]
        )
    all_fingerings = []
    for start, end in ALL_STRING_COMBOS:
        fingerings = [
            insert_over_x_array(start, list(p))
            for p in itertools.product(*all_string_positions[start:end])
        ]
        all_fingerings.extend(fingerings)

    all_fingerings = filter(  # filtering out tabs where not every note is in the chord
        lambda f: all(
            note
            in [
                note_normal(tuning[i] + fret)
                for i, fret in enumerate(f)
                if fret is not None
            ]
            for note in chord
        ),
        all_fingerings,
    )

    MAX_REACH = 2  # how many frets across the guitar which you can reach
    all_fingerings = filter(  # filtering out tabs where you would have to reach too far
        lambda f: (
            len(
                list(
                    itertools.combinations(
                        filter(lambda i: i is not None and i > 0, f), 2
                    )
                )
            )
            > 0
            and max(
                [
                    abs(c[0] - c[1])
                    for c in list(
                        itertools.combinations(
                            filter(lambda i: i is not None and i > 0, f), 2
                        )
                    )
                ]
            )
            <= MAX_REACH
        ),
        all_fingerings,
    )

    all_fingerings = (
        filter(  # filtering out tabs that are impossible to play / don't make sense
            lambda f: (
                (
                    all(
                        n is None
                        or n < statistics.mode(filter(lambda p: p is not None, f))
                        for n in f
                    )
                )  # removing barre chords with notes behind the barre
                if quantify(
                    lambda x: x == statistics.mode(filter(lambda p: p is not None, f)),
                    f,
                )
                >= 3  # condition for barre chord
                else (
                    quantify(lambda x: x is not None and x > 0, f) < 5
                )  # removing non-barre chords with 5 or more notes to hold down
            ),
            all_fingerings,
        )
    )

    all_fingerings = sorted(  # "easiest-to-play" tabs (aka closest together) rank highest
        all_fingerings,
        key=(
            lambda t: (
                # these weights for the different parts of the eval are arbitrarily chosen
                sum(1 for i in t if i == 0) * 0.5
                - statistics.stdev(filter(lambda i: i is not None and i > 0, t))
                + len(list(filter(lambda i: i is not None, t))) * 0.3
                # + random.random() * 0.2
            )
        ),
        reverse=True,
    )

    # print(Fore.BLACK + f"len {len(all_fingerings)}")
    if debug and len(all_fingerings) < limit:
        print(Fore.RED + "Unable to generate desired number of tabs")
    return all_fingerings[:limit]


def group_alike_tabs(tab_groups: list[list[tuple]], debug=False):

    def non_zero(tab: list):
        return filter(lambda n: n is not None and n > 0, tab)

    if debug:
        for tab_group in tab_groups:
            print(Fore.BLACK + str(tab_group))

    ret = []
    for tab in tab_groups[0]:
        group = [tab]
        for i in range(1, len(tab_groups)):
            group_center: float = statistics.mean(
                [statistics.mean(non_zero(tab)) for tab in group]
            )
            ordered_candidates = sorted(
                tab_groups[i],
                key=(
                    lambda t: (
                        abs(statistics.mean(non_zero(t)) - group_center)
                        + random.normalvariate(0, 1)
                    )
                ),
            )
            group.append(ordered_candidates[0])
        ret.append(group)
    if debug:
        for tab_group in ret:
            print(Fore.BLACK + str(tab_group))
    return ret


def main(debug=False):
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
    scale: list[int] = generate_scale(root, SCALES[scale_str])
    if debug:
        print(Fore.BLACK + str([NOTES[n] for n in scale]))
    tuning_str = input(
        Fore.BLUE
        + "Desired tuning: "
        + Fore.BLACK
        + "(leave blank for standard) "
        + Fore.WHITE
    )
    tuning = convert_tuning(tuning_str) if tuning_str != "" else STANDARD_TUNING
    amt = input(Fore.BLUE + "Number of chords: " + Fore.BLACK + "(leave blank for 4) " + Fore.WHITE)
    amt = int(amt) if amt != "" else 4
    atts = input(Fore.BLUE + "Number of tabs per chord: " + Fore.BLACK + "(leave blank for 3) " + Fore.WHITE)
    atts = int(atts) if atts != "" else 3
    assert amt >= 1
    for n in range(amt):
        target_chords = REGULAR_CHORDS
        chord_name, chord_notes = random.choice(list(target_chords.items()))
        base = random.randrange(len(scale))
        chord = generate_chord(base, chord_notes)
        print(
            Fore.BLUE
            + f"{NOTES[chord[0]]} {chord_name} -> {' '.join([NOTES[note_normal(n)] for n in chord])}"
        )
        tabs = generate_guitar_tabs(chord, tuning=tuning, limit=atts)
        print(Fore.WHITE + "".join([f"{NOTES[note]:^3}" for note in tuning]))
        for tab in tabs:
            print(Fore.BLACK + printable_tab(tab))


if __name__ == "__main__":
    main()
