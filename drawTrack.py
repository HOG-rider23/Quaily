import tkinter as tk
from pathlib import Path

from CSVconverter import load_track

window = tk.Tk()
window.title("Racetrack")
window.attributes("-fullscreen", False)
window.geometry("1200x800")

width, height = 1200, 800


canvas = tk.Canvas(window, width=width, height=height, bg="white")
canvas.pack(fill="both", expand=True) # canvas je dan v okno/window brez tega se ne nariše

csv_path = (
    Path(__file__).parent/ "racetrack-database-master"/ "racetrack-database-master"/ "tracks"/ "Monza.csv"
)
points = load_track(csv_path, width, height) # poiše v velikosti našega video da je pravilno nastavljeno
coordinates = [coordinate for point in points for coordinate in point] # postavi vrednosti v array [(x1, y1), (x2, y2)]  →  [x1, y1, x2, y2]
canvas.create_line(*coordinates, fill="black", width=3) # postavi v pare (x,y)
window.mainloop() #okno/window ostane odprt