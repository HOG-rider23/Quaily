import csv
from pathlib import Path


def load_track(csv_path, canvas_width, canvas_height, margin=30):
    points = []

    with Path(csv_path).open(newline="") as file:
        for row in csv.reader(file):
            if not row or row[0].startswith("#"): # izpusti komentrarje
                continue
            points.append((float(row[0]), float(row[1]))) #prvi dve vrsti da v x in y
    points = [(-y, x) for x, y in points] # zamenja in za negera y z x points = points = [(2, 5), (4, 1)] => [(-5, 2), (-1, 4)]

    if len(points) < 2:
        raise ValueError("The track CSV must contain at least two coordinate rows.")

    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)
    track_width = max_x - min_x  # širina proge
    track_height = max_y - min_y # višna proge
    scale = min(
        (canvas_width - 2 * margin) / track_width if track_width else float("inf"),
        (canvas_height - 2 * margin) / track_height if track_height else float("inf"),
    )

    drawn_width = track_width * scale
    drawn_height = track_height * scale
    offset_x = (canvas_width - drawn_width) / 2
    offset_y = (canvas_height - drawn_height) / 2

    return [
        (
            offset_x + (x - min_x) * scale,
            canvas_height - offset_y - (y - min_y) * scale,
        )
        for x, y in points
    ]
