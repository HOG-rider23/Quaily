import tkinter as tk
from tkinter import ttk
from pathlib import Path

from CSVconverter import load_track
from drawCar import draw_start, move_car

racePoints = []
raceIndex = 0
carID = None


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

def draw_track(event=None):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    if canvas_width <= 1 or canvas_height <= 1:
        return

    points = load_track(tracks[selected_track.get()], canvas_width, canvas_height)
    coordinates = [coordinate for point in points for coordinate in point]
    canvas.delete("track")
    canvas.create_line(*coordinates, fill="black", width=3, tags="track")
    #dekleracija za avto
    global racePoints, raceIndex, carID
    racePoints = points
    raceIndex = 0
    carID = draw_start(canvas, *racePoints[0])


def draw_race(event=None):
    global raceIndex
    if racePoints and carID is not None:
        raceIndex = (raceIndex + 1) % len(racePoints)
        move_car(canvas, carID, *racePoints[raceIndex])
    window.after(50, draw_race)

canvas.bind("<Configure>", draw_track)
track_selector.bind("<<ComboboxSelected>>", draw_track)
window.after(50, draw_race)
window.mainloop() #okno/window ostane odprt