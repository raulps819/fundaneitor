"""
Libreria para el desarrollo de problemas asociados a presion lateral de tierras
con la teoria de rankine. Requiere el uso de objetos de tipo suelo
"""

from suelo import Suelo
from math import cos, tan,sqrt,pi

def ka(suelo: Suelo=None, capa: int=None):
    """
    Devuelve una lista con los valores de coeficiente de presion activa de rankine
    para cada capa de un objeto suelo. Si se especifica una capa especifica devuelve un
    unico valor
        - suelo = Objeto de tipo suelo
        - capa = indice de la capa para la cual se quiere el coeficiente de presion activa
    """
    if capa == None:
        ka=[]
        for capai in suelo.capas:
            alpha=capai.alpha
            phi=capai.phi
            kai=cos(alpha)*((cos(alpha) - sqrt(cos(alpha)**2-cos(phi)**2))/(cos(alpha) + sqrt(cos(alpha)**2-cos(phi)**2)))
            ka.append(round(kai,3))
            pass
    else:
        capai=suelo.capas[capa]
        #alpha=capai.alpha
        alpha=0
        phi=capai.phi
        ka=cos(alpha)*((cos(alpha) - sqrt(cos(alpha)**2-cos(phi)**2))/(cos(alpha) + sqrt(cos(alpha)**2-cos(phi)**2)))  
        pass
    return round(ka,3)


def ptactivo(suelo,prof):
    """
    Devuelve el esfuerzo activo por rankine a una profundidad determinada
        - suelo: Objeto de tipo suelo
        - prof_pt: Profundidad para la que se quier el esfuerzo activo por rankine
    """
    capai=suelo.ptcapa(prof)
    if type(capai)==list:
        sigmai=[]
        for ci in capai:
            sigmai.append(round(ka[suelo,ci]*suelo.ptsigmahe(prof)
            - 2 * suelo.capas[ci].c * sqrt(ka[suelo,ci]),3))
        pass
    else:
        ci=capai
        sigmai=(round(ka[ci]*suelo.ptsigmahe(prof)
            - 2 * suelo.capas[ci].c * sqrt(ka[ci]),3))
        pass
    return sigmai

def activo(suelo: Suelo=None,prof_pt: float=None):
    """
    Devuele el esfuerzo activo por rankine a cierta profundidad o para todas las profundidades
    espeficadas
        - suelo: Objeto de tipo suelo
        - prof_pt: Especifique un valor unico o una lista de profundidades para las cuales desea el esfuerzo activo por rankine
    """
    if type(prof_pt)==list:
        sigma=[]
        for prof in prof_pt:        
            sigma.append(ptactivo(suelo,prof))
        pass
    else:
        sigma=ptactivo(suelo,prof_pt)
        pass
    return sigma

def kp(suelo: Suelo=None, capa: int=None):
    """
    Devuelve una lista con los valores de coeficiente de presion activa de rankine
    para cada capa de un objeto suelo. Si se especifica una capa especifica devuelve un
    unico valor
        - suelo = Objeto de tipo suelo
        - capa = indice de la capa para la cual se quiere el coeficiente de presion activa
    """
    if capa == None:
        kp=[]
        i=0
        for capai in suelo.capas:
            kp.append(round((tan(0.25*pi+0.5*capai.phi)**2),3))
            pass
    else:
        capai=suelo.capas[capa]
        kp=(round((tan(0.25*pi+0.5*capai.phi)**2),3))
        pass
    return kp

def ptpasivo(suelo,prof):
    """
    Devuelve el esfuerzo activo por rankine a una profundidad determinada
        - suelo: Objeto de tipo suelo
        - prof_pt: Profundidad para la que se quier el esfuerzo activo por rankine
    """
    capai=suelo.ptcapa(prof)
    if type(capai)==list:
        sigmai=[]
        for ci in capai:
            sigmai.append(round(kp[suelo,ci]*suelo.ptsigmahe(prof)
            - 2 * suelo.capas[ci].c * sqrt(kp[suelo,ci]),3))
        pass
    else:
        ci=capai
        sigmai=round((ka[ci]*suelo.ptsigmahe(prof)
            - 2 * suelo.capas[ci].c * sqrt(ka[ci])),3)
        pass
    return sigmai

def pasivo(suelo: Suelo=None,prof_pt: float=None):
    """
    Devuele el esfuerzo activo por rankine a cierta profundidad o para todas las profundidades
    espeficadas
        - suelo: Objeto de tipo suelo
        - prof_pt: Especifique un valor unico o una lista de profundidades para las cuales desea el esfuerzo activo por rankine
    """
    if type(prof_pt)==list:
        sigma=[]
        for prof in prof_pt:        
            sigma.append(ptpasivo(suelo,prof))
        pass
    else:
        sigma=ptpasivo(suelo,prof_pt)
        pass
    return sigma
