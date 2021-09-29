"""
Libreria para el desarrollo de problemas asociados a capacidad de carga
en cimentaciones por el metodo de meyerhof
"""
from math import degrees, exp, pi, radians, sqrt, tan
from qterzagui import gammaeq, sobreq
from rankine import kp
from suelo import Suelo

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
    return ((nq(suelo,prof)-1)*(1.4*tan(capa.phi)))

def sc(suelo,prof,B,L):
    """
    Devuelve el coeficiente Sc para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
        - B = base del cimiento
        - L = longitud del cimiento
    """
    i=suelo.ptcapa(prof,True)
    kpi=kp(suelo,i)
    return (1+0.2*kpi*(B/L))

def sq(suelo,prof,B,L):
    """
    Devuelve el coeficiente Sq para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - B = base del cimiento
        - L = longitud del cimiento
    """
    i=suelo.ptcapa(prof,True)
    capa=suelo.capas[i]
    kpi=kp(suelo,i)
    if capa.phi<10:
        return 1
    else:
        return (1+0.1*kpi*(B/L))

def dc(suelo,prof,B):
    """
    Devuelve el coeficiente dc para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - B = base del cimiento
    """    
    i=suelo.ptcapa(prof,True)
    kpi=kp(suelo,i)
    return (1+0.2*sqrt(kpi)*(prof/B))

def dq(suelo,prof,B):
    """
    Devuelve el coeficiente dq para una profundidad dada
        - suelo = suelo de cimentacion. Objeto de tipo suelo
        - prof = profundidad base de cimentacion
        - B = base del cimiento
    """    
    i=suelo.ptcapa(prof,True)
    capa=suelo.capas[i]
    kpi=kp(suelo,i)
    if capa.phi<10:
        return 1
    else:
        return (1+0.1*sqrt(kpi)*(prof/B))

def ic (tetha):
    """
    Devuelve el coeficiente ic para una profundidad dada
        - tetha = angulo (degrees) de inclinacion de la carga 
        respecto al eje vertical
    """    
    return ((1-(tetha/90))**2)

def iy (suelo, prof, tetha):
    """
    Devuelve el coeficiente iy para una profundidad dada
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion

        - tetha = angulo (degrees) de inclinacion de la carga 
        respecto al eje vertical
    """
    capa=suelo.capas[suelo.ptcapa(prof,True)]
    if capa.phi==0:
        return 0
    else:
        return (1-(tetha/degrees(capa.phi)))

def qult(suelo,prof,B,L,tetha: float=0.0):
    """
    Devuelve la carga ultima para un suelo:
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
        - B = base del cimiento
        - L = longitud del cimiento
        - tetha = angulo (degrees) de inclinacion de la carga 
        respecto al eje vertical
    """
    capa=suelo.ptcapa(prof,True)
    ci=capa.c
    nci=nc(suelo,prof)
    nqi=nq(suelo,prof)
    nyi=ny(suelo,prof)
    dci=dc(suelo, prof,B)
    dqi=dq(suelo,prof,B)
    dyi=dqi
    qi=sobreq(suelo,prof)
    yeq=gammaeq(suelo,prof,B)
    
    if tetha==0.0:
        sci=sc(suelo, prof,B,L)
        sqi=sq(suelo,prof,B,L)
        syi=sqi
        qulti=ci*nci*sci*dci+qi*nqi*sqi*dqi+0.5*yeq*B*nyi*syi*dyi
        return qulti
    else:
        ici=ic(tetha)
        iqi=ici
        iyi=iy(suelo,prof,tetha)
        qulti=ci*nci*dci*ici+qi*nqi*dqi*iqi+0.5*yeq*B*nyi*dyi*iyi
        return qulti

def qadm(suelo,prof,B,L,tetha: float=0.0,fs: float=2.0):
    """
    Devuelve la carga ultima para un suelo:
        - suelo = suelo de cimentacion
        - prof = profundidad de base de cimentacion
        - B = base del cimiento
        - L = longitud del cimiento
        - tetha = angulo (degrees) de inclinacion de la carga 
        respecto al eje vertical
        - fs = factor de seguridad
    """  
    return (qult(suelo,prof,B,L,tetha)/fs)