#avto = input()
#S = float(input())
#V = float(input())
weight = 768
hp = 1000
Vzac = 0
Vmax = 335
br = 6
a =  round((hp * 745.7)/(weight * (Vmax/ 3.6)), 2)
t = round(Vmax/(a * 3.6),2)
d = round(Vzac * t +1/2 * a * (t**2))
print(a , "m/s²", t , "s", d, "m")
abr = br * 9.81
tbr = round((335/3.6)/ abr)
dbr = round((335/3.6)**2 / (2 * abr))
print(abr , "m/s²", tbr , "s", dbr, "m")