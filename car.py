#avto = input()
#S = float(input())
#V = float(input())
import time
class specs:
    def __init__(self, Vmax, weight, hp,br):
        self.currentV = 0
        self.Vmax = Vmax
        self.weight = weight
        self.hp = hp
        self.br = br
        self.a = round((self.hp * 745.7) / (self.weight * (self.Vmax / 3.6)), 2)

    def acelearate(self, t):
        self.currentV += self.a * t
        print("currentV:", round(self.currentV,2))
        if self.currentV > self.Vmax:
            self.currentV = self.Vmax
        elif self.currentV < 0:
            self.currentV = 0

car = specs(Vmax=335,weight=768,hp=1000,br=6)
for i in range(10):
    car.acelearate(t = 0.1)

#print(a , "m/s²", t , "s", d, "m")
#abr = br * 9.81
#tbr = round((335/3.6)/ abr)
#dbr = round((335/3.6)**2 / (2 * abr))
#print(abr , "m/s²", tbr , "s", dbr, "m")