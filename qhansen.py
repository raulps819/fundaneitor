"""
Libreria para el desarrollo de problemas asociados a capacidad de carga
en cimentaciones por el metodo de hansen
"""
from math import degrees, exp, pi, radians, sin, sqrt, tan, atan
from qterzagui import gammaeq, sobreq
from rankine import kp
from suelo import Suelo

def khansen(prof,B):
    
    if (prof/B) <= 1:
        return (prof/B)
    else:
        return atan(prof/B) 

def nq(suelo,prof):
    """
    Devuelve el coeficiente Nq para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    return (exp(pi*tan(capa.phi))*(tan(radians(45)+0.5*capa.phi))**2)

def nc(suelo,prof):
    """
    Devuelve el coeficiente Nc para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    return ((nq(suelo,prof)-1)*(tan(capa.phi)**-1))

def ny(suelo,prof):
    """
    Devuelve el coeficiente Ny para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    return (1.5*(nq(suelo,prof)-1)*tan(capa.phi))


def sc(suelo,prof,B,L,faja: bool=False):
    """
    Devuelve el coeficiente Sc para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
        - B = base del cimiento
        - L = longitud del cimiento
    """
    if suelo.capas[suelo.ptcapa(prof,True)].phi == 0:
        return (0.2*(B/L))

    elif suelo.capas[suelo.ptcapa(prof,True)].phi != 0 and faja:
        return 1
    else:
        return (1+((nq(suelo,prof))/(nc(suelo,prof)))*(B/L))
        

def sq(suelo,prof,B,L):
    """
    Devuelve el coeficiente Sq para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - B = base del cimiento
        - L = longitud del cimiento
    """
    return (1+(B/L)*tan(suelo.capas[suelo.ptcapa(prof,True)].phi))

def sy(B,L):
    """
    Devuelve el coeficiente Sq para una profundidad dada
        - B = base del cimiento
        - L = longitud del cimiento
    """
    return (1-0.4*(B/L))

def dc(suelo,prof,B):
    """
    Devuelve el coeficiente dc para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - B = base del cimiento
    """    
    k=khansen(prof,B)
    if suelo.capas[suelo.ptcapa(prof,True)].phi == 0:
        return (0.4*k)
    else:
        return (1+0.4*k)


def dq(suelo,prof,B):
    """
    Devuelve el coeficiente dq para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - B = base del cimiento
    """    
    phi=suelo.capas[suelo.ptcapa(prof,True)].phi
    k=khansen(prof,B)
    return (1+2*k*tan(phi)*(1-sin(phi))**2)

def dy():
    """Devuelve el coeficiente dy"""
    return 1

def iq(suelo,prof,V,B,L,H):
    """
    Devuelve el coeficiente iq para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - V = fuerza aplicada perpendicular a la base del cimiento
        - B = base del cimiento
        - L = longitud el cimiento
        - H = fuerza aplicada paralela a la base del cimiento
    """
    phi=suelo.capas[suelo.ptcapa(prof,True)].phi
    ca=0.6*suelo.capas[suelo.ptcapa(prof,True)].c
    af=B*L
    return (1-((0.5*H)/(V + af*ca*tan(phi)**-1)))**5


def ic (suelo,prof,V,B,L,H):
    """
    Devuelve el coeficiente ic para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - V = fuerza aplicada perpendicular a la base del cimiento
        - B = base del cimiento
        - L = longitud el cimiento
        - H = fuerza aplicada paralela a la base del cimiento
    """
    phi=suelo.capas[suelo.ptcapa(prof,True)].phi
    ca=0.6*suelo.capas[suelo.ptcapa(prof,True)].c
    af=B*L
    if phi>0:
        return (iq(suelo,prof,V,B,L,H) 
        - ((1-iq(suelo,prof,V,B,L,H))/(nq(suelo,prof)-1)))
    elif phi==0:
        return (0.5-0.5*sqrt(1-(H/(af*ca))))
    else:
        return 'error'


def iy (suelo,prof,V,B,L,H,n):
    """
    Devuelve el coeficiente iy para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - V = fuerza aplicada perpendicular a la base del cimiento
        - B = base del cimiento
        - L = longitud el cimiento
        - H = fuerza aplicada paralela a la base del cimiento
        - n = angulo de inclinacion del cimiento
    """
    phi=suelo.capas[suelo.ptcapa(prof,True)].phi
    ca=0.6*suelo.capas[suelo.ptcapa(prof,True)].c
    af=B*L
    if n>0:
        return (1-(((0.7-n/450)*H)/(V + af*ca*tan(phi)**-1)))**5
    else:
        return (1-((0.7*H)/(V + af*ca*tan(phi)**-1)))**5

def gc(suelo, prof, betha):
    """
    Devuelve el coeficiente gc para una cimentacion
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - betha = angulo de inclinacion del terreno en el sentido de las manecillas del reloj
    """
    if suelo.capas[suelo.ptcapa(prof,True)].phi == 0:
        return (betha/147)
    elif suelo.capas[suelo.ptcapa(prof,True)].phi > 0:
        return (1-(betha/147))

def gq(betha):
    """
    Devuelve el coeficiente gq para una cimentacion
        - betha = angulo de inclinacion del terreno en el sentido de las manecillas del reloj
    """
    return (1-0.5*tan(betha))**5

def bc(suelo,prof,n):
    """
    Devuelve el coeficiente bc para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - n = angulo de inclinacion del cimiento
    """
    if n==0:
        return 1
    else:
        phi=suelo.capas[suelo.ptcapa(prof,True)].phi
        if phi==0:
            return (n/147)
        else:
            return (1-(n/147))

def bq(suelo,prof,n):
    """
    Devuelve el coeficiente bq para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - n = angulo de inclinacion del cimiento
    """
    if n==0:
        return 1
    else:
        phi=suelo.capas[suelo.ptcapa(prof,True)].phi
        return (exp(-2*n*tan(phi)))

def by(suelo,prof,n):
    """
    Devuelve el coeficiente by para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - n = angulo de inclinacion del cimiento
    """
    if n==0:
        return 1
    else:
        phi=suelo.capas[suelo.ptcapa(prof,True)].phi
        return (exp(-2.7*n*tan(phi)))


def qult(suelo,prof,V,B,L,H,n,betha,faja: bool=False):
    """
    Devuelve la carga ultima para un suelo:
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - V = fuerza aplicada perpendicular a la base del cimiento
        - B = base del cimiento
        - L = longitud el cimiento
        - H = fuerza aplicada paralela a la base del cimiento
        - n = angulo (degrees) de inclinacion del cimiento
        - betha = angulo (degrees) de inclinacion del terreno en el sentido de las manecillas del reloj
        - faja = booleano si el cimiento es en faja
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    ci=capa.c
    betha=radians(betha)
    n=radians(n)


    nqi=nq(suelo,prof)
    nci=nc(suelo,prof)
    nyi=ny(suelo,prof)

    dci=dc(suelo, prof,B)
    dqi=dq(suelo,prof,B)
    dyi=dy()

    qi=sobreq(suelo,prof)
    qi=94.38
    yeq=gammaeq(suelo,prof,B)
    
    sci=sc(suelo, prof,B,L,faja)
    sqi=sq(suelo,prof,B,L)
    syi=sy(B,L)

    ici=ic(suelo,prof,V,B,L,H)
    iqi=iq(suelo,prof,V,B,L,H)
    iyi=iy(suelo,prof,V,B,L,H,n)

    gci=gc(suelo, prof, degrees(betha))
    gqi=gq(betha)
    gyi=gqi

    bci=bc(suelo,prof,degrees(n))
    bqi=bq(suelo,prof,n)
    byi=by(suelo,prof,n)


    qulti=ci*nci*sci*dci*ici*gci*bci+qi*nqi*sqi*dqi*iqi*gqi*bqi+0.5*yeq*B*nyi*syi*dyi*iyi*gyi*byi
    return qulti

def qadm(suelo,prof,V,B,L,H,n,betha,fs: float=2.0,faja: bool=False,):
    """
   Devuelve la carga admisible para un suelo:
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - V = fuerza aplicada perpendicular a la base del cimiento
        - B = base del cimiento
        - L = longitud el cimiento
        - H = fuerza aplicada paralela a la base del cimiento
        - n = angulo de inclinacion del cimiento
        - betha = ngulo de inclinacion del terreno en el sentido de las manecillas del reloj
        - faja = booleano si el cimiento es en faja
        - fs = factor de seguridad
    """  
    return (qult(suelo,prof,V,B,L,H,n,betha,faja)/fs)