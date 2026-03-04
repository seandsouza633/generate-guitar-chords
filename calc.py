from main import NOTES

natural_notes = [
    1,  # C
    3,  # D
    5,  # E
    6,  # F
    8,  # G
    10, # A
    12, # B
]

with open("da-notes.txt", "w") as f:
    distances = []
    distances.extend([
        (natural_notes[i], natural_notes[j], (natural_notes[j] - natural_notes[i]) % 12)
        for i in range(7) for j in range(i+1, 7)
        ])
    distances.extend([
        (natural_notes[j], natural_notes[i], (natural_notes[i] - natural_notes[j]) % 12)
        for i in range(7) for j in range(i+1, 7)
        ])
    distances = sorted(distances, key=lambda d: d[2])
    f.writelines([
        f"{NOTES[d[0]]} -> {NOTES[d[1]]} = {d[2]} frets\n"
        for d in distances
        ])