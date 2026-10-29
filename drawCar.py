from car import car


def draw_start(canvas, x, y):
    radius = 7
    canvas.delete("car")
    return canvas.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill=car.color,
        tags="car",
    )
def move_car(canvas, carID, x, y):
    radius = 7
    canvas.coords(
        carID,
        x - radius,
        y - radius,
        x + radius,
        y + radius,
    )

