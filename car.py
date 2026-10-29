import random
class specs:
    def __init__(self, vmax, weight, hp,br,color):
        self.currentV = 0 #zacetna hitrost
        self.raceNumber = random.randint(0, 99)
        self.Vmax = vmax / 3.6 # m/s
        self.weight = weight # kg
        self.hp = hp * 745.7 # moč motorja W
        self.br = br # bremze  g
        self.a = round(self.hp / (self.weight * self.Vmax), 2)
        self.color = color


    def accelerate(self, t):
        self.currentV = min(self.Vmax,  self.currentV + self.a * t) #min pusti da je 335 največja hitrost
        print("currentV:", round(self.currentV * 3.6, 2))

    def decelerate(self, t):
        self.currentV = max(0,(self.currentV - 9.81 * self.br * t)) #max pusti da je 0 najmanjša hitrost
        print("currentV:", round(self.currentV * 3.6, 2))



car = specs(vmax=335,weight=768,hp=1000,br=6,color="red")

