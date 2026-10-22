#avto = input()
#S = float(input())
#V = float(input())
#import time
class specs:
    def __init__(self, vmax, weight, hp,br):
        self.currentV = 0 #zacetna hitrost
        self.Vmax = vmax / 3.6 # m/s
        self.weight = weight # kg
        self.hp = hp * 745.7 # moč motorja W
        self.br = br # bremze  g
        self.a = round(self.hp / (self.weight * self.Vmax), 2)

    def accelerate(self, t):
        self.currentV = min(self.Vmax,  self.currentV + self.a * t)
        print("currentV:", round(self.currentV * 3.6, 2))

    def decelerate(self, t):
        self.currentV = max(0,(self.currentV - 9.81 * self.br * t))
        print("currentV:", round(self.currentV * 3.6, 2))

car = specs(vmax=335,weight=768,hp=1000,br=6)
while car.currentV < car.Vmax:
    car.accelerate(t = 0.1)

while car.currentV > 0:
    car.decelerate(t = 0.1)
