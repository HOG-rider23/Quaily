import tkinter as tk
from tkinter import ttk
from pathlib import Path
from math import atan2, degrees, hypot
import time

from CSVconverter import load_track
from drawCar import draw_start, move_car
from car import *

racePoints = []
carID = None
raceDistance = 0.0
segmentLengths = []
lapLength = 0.0
corners = []
completed_laps = 0
lap_timer_start = None
lap_time = None
PIXELS_PER_METER = 1.0
CORNER_ANGLE_THRESHOLD = 18
CORNER_WINDOW = 8
CORNER_MERGE_GAP = 5

window = tk.Tk()
window.title("Racetrack")
window.attributes("-fullscreen", False)
window.geometry("900x600")

canvas = tk.Canvas(window, bg="white")
canvas.pack(fill="both", expand=True) # canvas je dan v okno/window brez tega se ne nariše

tracks_dir = (
    Path(__file__).parent
    / "racetrack-database-master"
    / "racetrack-database-master"
    / "tracks"
)
tracks = {path.stem: path for path in tracks_dir.glob("*.csv")}

selected_track = tk.StringVar(value="Austin")
track_selector = ttk.Combobox(
    window,
    textvariable=selected_track,
    values=sorted(tracks),
    state="readonly",
)
track_selector.pack()

timer_label = ttk.Label(window, text="Lap timer: waiting for warm-up lap")
timer_label.pack()


def detect_corners(points, segment_lengths):
    point_count = len(points)
    turn_angles = []
    window = min(CORNER_WINDOW, max(1, point_count // 4))
    for i in range(point_count):
        before = points[(i - window) % point_count]
        current = points[i]
        after = points[(i + window) % point_count]
        incoming = (current[0] - before[0], current[1] - before[1])
        outgoing = (after[0] - current[0], after[1] - current[1])
        cross = incoming[0] * outgoing[1] - incoming[1] * outgoing[0]
        dot = incoming[0] * outgoing[0] + incoming[1] * outgoing[1]
        turn_angles.append(abs(degrees(atan2(cross, dot))))

    candidates = [
        i for i, angle in enumerate(turn_angles)
        if angle >= CORNER_ANGLE_THRESHOLD
    ]
    groups = []
    for index in candidates:
        if groups and index - groups[-1][-1] <= CORNER_MERGE_GAP + 1:
            groups[-1].append(index)
        else:
            groups.append([index])

    if (
        len(groups) > 1
        and groups[0][0] + point_count - groups[-1][-1] <= CORNER_MERGE_GAP + 1
    ):
        groups[0] = groups[-1] + groups[0]
        groups.pop()

    cumulative_distances = []
    distance = 0.0
    for segment_length in segment_lengths:
        cumulative_distances.append(distance)
        distance += segment_length

    detected = []
    for number, group in enumerate(groups, start=1):
        apex_index = max(group, key=lambda point_index: turn_angles[point_index])
        corner_start_index = (apex_index - window) % point_count
        corner_start_distance = cumulative_distances[corner_start_index]
        corner_span = min(point_count, len(group) + 2 * window)
        corner_length = sum(
            segment_lengths[(corner_start_index + offset) % point_count]
            for offset in range(corner_span)
        )
        detected.append(
            (
                corner_start_distance,
                corner_length,
                turn_angles[apex_index],
                number,
                points[apex_index],
            )
        )
    return detected


def draw_track(event=None):
    global racePoints, carID, raceDistance, segmentLengths, lapLength, corners
    global completed_laps, lap_timer_start, lap_time

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    if canvas_width <= 1 or canvas_height <= 1:
        return

    points = load_track(tracks[selected_track.get()], canvas_width, canvas_height)
    coordinates = [coordinate for point in points for coordinate in point]
    canvas.delete("track")
    canvas.delete("corner-label")
    canvas.create_line(*coordinates, fill="black", width=3, tags="track")
    racePoints = points
    segmentLengths = [
        hypot(
            points[(i + 1) % len(points)][0] - points[i][0],
            points[(i + 1) % len(points)][1] - points[i][1],
        )
        for i in range(len(points))
    ]
    lapLength = sum(segmentLengths)
    corners = detect_corners(racePoints, segmentLengths)
    for _, _, _, number, (x, y) in corners:
        canvas.create_text(
            x,
            y - 16,
            text=str(number),
            fill="blue",
            font=("Arial", 10, "bold"),
            tags="corner-label",
        )
    raceDistance = 0.0
    completed_laps = 0
    lap_timer_start = None
    lap_time = None
    timer_label.config(text="Lap timer: waiting for warm-up lap")
    car.currentV = 0
    carID = draw_start(canvas, *racePoints[0])


def draw_race(event=None):
    global raceDistance, completed_laps, lap_timer_start, lap_time
    dt = 0.05
    if len(racePoints) > 1 and carID is not None and lapLength > 0:
        upcoming_corner = None
        distance_to_corner = lapLength
        for corner in corners:
            corner_start, corner_length, turn_angle, _, _ = corner
            distance = (corner_start - raceDistance) % lapLength
            if distance < distance_to_corner:
                upcoming_corner = corner
                distance_to_corner = distance

        if upcoming_corner is not None:
            corner_start, corner_length, turn_angle, _, _ = upcoming_corner
            target_speed = car.Vmax * max(0.25, 1 - turn_angle / 90)
            braking_acceleration = 9.81 * car.br
            braking_distance = (
                max(0, car.currentV**2 - target_speed**2)
                / (2 * braking_acceleration)
                * PIXELS_PER_METER
            )
            distance_into_corner = (raceDistance - corner_start) % lapLength
            in_corner = distance_into_corner <= corner_length
            if car.currentV > target_speed and (
                in_corner or distance_to_corner <= braking_distance * 1.2
            ):
                car.decelerate(dt)
            elif not in_corner:
                car.accelerate(dt)
        else:
            car.accelerate(dt)

        distance_step = car.currentV * dt * PIXELS_PER_METER
        total_distance = raceDistance + distance_step
        line_crossings = int(total_distance // lapLength)
        for _ in range(line_crossings):
            completed_laps += 1
            if completed_laps == 1:
                lap_timer_start = time.perf_counter()
            elif completed_laps == 2 and lap_timer_start is not None:
                lap_time = time.perf_counter() - lap_timer_start
        raceDistance = total_distance % lapLength

        distance = raceDistance
        for i, segment_length in enumerate(segmentLengths):
            if segment_length > 0 and distance <= segment_length:
                start = racePoints[i]
                end = racePoints[(i + 1) % len(racePoints)]
                fraction = distance / segment_length
                x = start[0] + (end[0] - start[0]) * fraction
                y = start[1] + (end[1] - start[1]) * fraction
                move_car(canvas, carID, x, y)
                break
            distance -= segment_length
    if lap_timer_start is None:
        timer_label.config(text="Lap timer: waiting for warm-up lap")
    elif lap_time is None:
        elapsed = time.perf_counter() - lap_timer_start
        timer_label.config(
            text=f"Lap time: {int(elapsed // 60):02}:{elapsed % 60:05.2f}"
        )
    else:
        timer_label.config(
            text=f"Lap time: {int(lap_time // 60):02}:{lap_time % 60:05.2f}"
        )
    window.after(50, draw_race)

canvas.bind("<Configure>", draw_track)
track_selector.bind("<<ComboboxSelected>>", draw_track)
window.after(50, draw_race)
window.mainloop() #okno/window ostane odprt5