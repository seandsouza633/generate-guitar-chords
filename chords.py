from main import NOTES, GUITAR_STRINGS, note_normal
from scales import SCALES, generate_scale
from colorama import Fore
import random
import itertools
import statistics
import math

CHORDS = {
    "maj": [(1, 0), (3, 0), (5, 0)],
    "min": [(1, 0), (3, -1), (5, 0)],
    "dim": [(1, 0), (3, -1), (5, -1)],
    "aug": [(1, 0), (3, 1), (5, 0)],
    "maj7": [(1, 0), (3, 0), (5, 0), (7, 0)],
    "min7": [(1, 0), (3, -1), (5, 0), (7, -1)],
    "dom7": [(1, 0), (3, 0), (5, 0), (7, -1)],
    "sus2": [(1, 0), (2, 0), (5, 0)],
    "sus4": [(1, 0), (4, 0), (5, 0)],
}

MAJOR_CHORDS = {k: v for k, v in CHORDS.items() if k in ["maj", "maj7"]}

REGULAR_CHORDS = {k: v for k, v in CHORDS.items() if k not in ["sus2", "sus4"]}

ATTS = 6  # how many chord shapes to generate per chord


def generate_chord(base: int, scale: list[int], chord_positions) -> list[int]:
    ret = []
    for pos in chord_positions:
        note = scale[(base + pos[0] - 1) % len(scale)] + pos[1]
        if note > 12:
            note -= 12
        ret.append(note)
    return ret


ALL_STRING_COMBOS = [(i, i + n) for n in range(6, 2, -1) for i in range(7 - n)]


def insert_over_x_array(start: int, arr: list):
    ret = [None for _ in range(6)]
    ret[start:start] = arr
    ret = ret[:6]
    # print(printable_tab(ret))
    return ret


def printable_tab(tab) -> str:
    return " ".join([" x" if t is None else f"{t:2}" for t in tab])


def generate_guitar_tabs(chord, limit=10) -> list[tuple]:
    all_string_positions = []
    for string in GUITAR_STRINGS:
        all_string_positions.append(
            [fret for fret in range(0, 12) if note_normal(string + fret) in chord]
        )
    all_fingerings = []
    for start, end in ALL_STRING_COMBOS:
        fingerings = [
            insert_over_x_array(start, list(p))
            for p in itertools.product(*all_string_positions[start:end])
        ]
        all_fingerings.extend(fingerings)

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
                if sum(
                    map(
                        lambda x: (
                            x == statistics.mode(filter(lambda p: p is not None, f))
                        ),
                        f,
                    )
                )
                >= 3  # condition for barre chord
                else (
                    sum(map(lambda x: x is not None and x > 0, f)) < 5
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
                + random.random() * 0.2
            )
        ),
        reverse=True,
    )

    print(Fore.BLACK + f"len {len(all_fingerings)}")
    if len(all_fingerings) < limit:
        print(Fore.RED + "Unable to generate desired number of tabs")
    return all_fingerings[:limit]


def main(debug=False):
    root = input(Fore.BLUE + "Desired root: " + Fore.WHITE).lower()
    try:
        root = next(k for k in NOTES.keys() if NOTES[k].lower() == root)
    except StopIteration:
        print(Fore.RED + "No key found.")
        return
    scale_name = random.choice(list(SCALES.keys()))
    # scale_name = "major"
    scale: list[int] = generate_scale(root, SCALES[scale_name])
    print(Fore.BLUE + f"Scale: {scale_name}")
    if debug:
        print(Fore.BLACK + str([NOTES[n] for n in scale]))
    amt = 4
    # amt = 1
    for n in range(amt):
        target_chords = MAJOR_CHORDS if n == amt - 1 and amt > 1 else REGULAR_CHORDS
        chord_name, chord_positions = random.choice(list(target_chords.items()))
        # chord_name, chord_positions = "maj", target_chords["maj"]
        if debug:
            print(Fore.BLACK + f"{chord_name} {chord_positions}")
        base = random.randrange(len(scale))
        # base = 0
        chord = generate_chord(base, scale, chord_positions)
        if debug:
            print(Fore.BLACK + f"{NOTES[root]}{chord_name:4} {chord}")
        print(
            Fore.BLUE
            + f"{NOTES[root]}{chord_name} -> {' '.join([NOTES[note_normal(n)] for n in chord])}"
        )
        tabs = generate_guitar_tabs(chord, limit=ATTS)
        # print(f"Tabs count {len(tabs)}")
        print(Fore.WHITE + " E  A  D  G  B  E")
        for tab in tabs:
            print(Fore.BLACK + printable_tab(tab))


if __name__ == "__main__":
    main()
