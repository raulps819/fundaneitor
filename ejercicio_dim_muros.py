from math import radians
from rankine import *
from capa import *
from suelo import *
from muros import *
from os import system

system('cls')


capa1=Capa(0,6,18,0,30,0,10)
suelo1=Suelo([capa1],6.8,0,9.81)

capa2=Capa(5.2,6.7,19,0,20,40)
suelo2=Suelo([capa2],6.8,0,9.81)

muro1=Muro(6,0.7,0.7,0.7,0.7,2.6,0.5)

alpha=suelo1.capas[0].alpha
H=round(muro1.lpuntera * tan(alpha),3)

kai=ka(suelo1,0)
print(kai)

d=H/3

ea=activo(suelo1,6.7)
print('ea: ',ea)


