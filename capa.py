from math import pi,sin

class Capa():
    """
    Generic class for any soil layer
        -Primitive Attributes
            -prof_init:  profundidad inicial de la capa [m]
            -prof_final: profundidad final de la capa [m]
            -gamma:      peso especifico [kn/m3]
            -gamma_sat:  peso especifico saturado [kn/m3]
            -phi:        angulo de friccion [degrees]
            -c:          cohesion de la capa [kn/m2]
        -Derivated Attributes
            -ko=: coef presion horizontal
    """

    def __init__(self,_prof_init,_prof_final,_gamma,_gamma_sat,_phi,_c):
        self.phi=_phi*pi/180
        self.prof_init=_prof_init
        self.prof_final=_prof_final
        self.gamma=_gamma
        self.gamma_sat=_gamma_sat
        self.c=_c
        pass

    @property
    def ko(self):
        return round((1-sin(self.phi)),4)

    
    
    
        