from math import degrees, radians
from capa import Capa
from suelo import Suelo
import qterzagui
import qhansen

capa1=Capa(0,4,17.5,19,23.5,10)
capa2=Capa(4,6,21,22,5,35)
capas=[capa1,capa2]
suelo = Suelo(capas,4)


prof=6
V=300
B=3.5
L=4
H=0
n=10
betha=radians(15)
n=radians(n)
faja=False

betha=15
n=10

rta=qhansen.qult(suelo,prof,V,B,L,H,n,betha,faja)


print('Qu = ',rta)
print('Qadm = ',rta/2)

"""
nqi=qhansen.nq(suelo,prof)
nci=qhansen.nc(suelo,prof)
nyi=qhansen.ny(suelo,prof)

dci=qhansen.dc(suelo, prof,B)
dqi=qhansen.dq(suelo,prof,B)
dyi=qhansen.dy()

qi=qterzagui.sobreq(suelo,prof)
yeq=qterzagui.gammaeq(suelo,prof,B)

sci=qhansen.sc(suelo, prof,B,L,faja)
sqi=qhansen.sq(suelo,prof,B,L)
syi=qhansen.sy(B,L)

ici=qhansen.ic(suelo,prof,V,B,L,H)
iqi=qhansen.iq(suelo,prof,V,B,L,H)
iyi=qhansen.iy(suelo,prof,V,B,L,H,n)

gci=qhansen.gc(suelo, prof, degrees(betha))
gqi=qhansen.gq(betha)
gyi=gqi

bci=qhansen.bc(suelo,prof,degrees(n))
bqi=qhansen.bq(suelo,prof,n)
byi=qhansen.by(suelo,prof,n)
"""