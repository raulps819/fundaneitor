from rankine import *
from capa import *
from suelo import *
import qterzagui

capa1=Capa(0,10,17.6,0,28,30,0)
suelo1=Suelo([capa1],10,0,9.81)

rta=qterzagui.qult(suelo1,1.75,"continuo",5)
print(rta)

