"""
Libreria para el desarrollo de problemas asociados a capacidad de carga
en cimentaciones por el metodo de terzagui
"""
from math import cos, exp, pi, tan, radians
from suelo import Suelo

def kpy(suelo,prof):
    """
    Devuelve el coeficiente Kpy para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
    """
    capa=suelo.ptcapa(prof)
    if type(capa)==list:
        capa=suelo.capas[capa[1]]
        pass
    else:
        capa=suelo.capas[capa]
    coef=3*(tan(radians(45)+(0.5*(capa.phi + radians(33)))))**2
    return coef

#FACTORES DE CAPACIDAD DE SOPORTE
def nq(suelo: Suelo=None,prof: float=0.0):
    """
    Devuelve el coeficiente Nq para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    a=exp((0.75*pi - 0.5*capa.phi)*tan(capa.phi))
    coef=(a**2)/(2*(cos(0.25*pi+0.5*capa.phi)**2))
    return coef
    
def nc(suelo,prof):
    """
    Devuelve el coeficiente Nc para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    coef=(nq(suelo,prof)-1)*(tan(capa.phi)**-1)
    return coef

def ny(suelo,prof):
    """
    Devuelve el coeficiente Ny para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    coef=(0.5*tan(capa.phi))*((kpy(suelo,prof)/(cos(capa.phi)**2))-1)
    return coef


#FACTORES DE FORMA
def sc (cimiento: str="rectangular"):
    """
    Devuelve el coeficiente Sc para un tipo de cimiento dado
        - cimiento:
            - rectangular = rectangular/cuadrado (1.3)
            - redondo = redondo (1.3)
            - continuo = continuo (1.0)
    """
    if cimiento=="rectangular":
        return 1.3
    elif cimiento=="redondo":
        return 1.3
    elif cimiento=="continuo":
        return 1
    else:
        print('error')

def sy (cimiento: str="rectangular"):
    """
    Devuelve el coeficiente Sy para un tipo de cimiento dado
        - cimiento:
            - rectangular = rectangular/cuadrado (0.8)
            - redondo = redondo (0.6)
            - continuo = continuo (1.0)
    """
    if cimiento=="rectangular":
        return 0.8
    elif cimiento=="redondo":
        return 0.6
    elif cimiento=="continuo":
        return 1
    else:
        return print('error')

def sobreq(suelo: Suelo=None,prof: float=0):
    """
    Devuelve el factor de sobre carga para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
    """
    q=suelo.ptsigmav(prof)
    return q

def gammaeq(suelo: Suelo=None,prof: float=0,b: float=0):
    """
    Devuelve el gamma equivalente 
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - b = ancho del cimiento a utilizar
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]

    if suelo.n_fret<=prof: #caso 1
        coef=capa.gamma_sat - suelo.gamma_h20
        pass
    elif suelo.n_fret>prof and (suelo.n_fret-prof)<=b: #caso 32
        d=suelo.n_fret - prof
        coef=capa.gamma_sat+(d/b)*(capa.gamma - capa.gamma_sat)
        pass
    else:
        coef=capa.gamma
        pass
    return coef

def qult(suelo,prof,cimiento,b):
    capa=suelo.ptcapa(prof,True)
    ci=suelo.capas[capa].c
    nci=nc(suelo,prof)
    nqi=nq(suelo,prof)
    nyi=ny(suelo,prof)
    sci=sc(cimiento)
    syi=sy(cimiento)
    qi=sobreq(suelo,prof)
    geq=gammaeq(suelo,prof,b)

    return (ci*nci*sci + qi*nqi + 0.5*geq*b*nyi*syi)


def qadm(suelo,prof,cimiento,b,fs):
    return qult(suelo,prof,cimiento,b)/fs

