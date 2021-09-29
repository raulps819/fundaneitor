#OUTER LIBRARIES
from math import pi
from abc import ABC,abstractmethod

#INNER LIBRARIES

#CROSS SECTION OBJECTS
class CrossSection(ABC):
    """
    Base class for any type of CrossSection of an Element.

    - Primitive Attributes:
        - Depends on the CrossSection subclass
    - Derivated Attributes:
        - area : Area associated to the CrossSection
        - inertia_z : Moment of Inertia around Z axis.
    """
    def __init__(self) -> "CrossSection":
        pass

    @property
    def area(self):
        pass

    @property
    def inertia_z(self):
        pass

class SquareSection(CrossSection):
    """
    Base class for elements with squaresection of an Element.

    - Primitive Attributes:
        - Depends on the CrossSection subclass
    - Derivated Attributes:
        - area : Area associated to the CrossSection
        - inertia_z : Moment of Inertia around Z axis.
    """
    def __init__(self, b : float = 0.2,
                       h : float = 0.2) -> "CrossSection":
        self.base = b;
        self.heigth = h;
    
    @property
    def area(self):
        return self.base*self.heigth     
    @property
    def inertia_z(self):
        return self.base*(self.heigth^3)/12

cuadrado1 = SquareSection()


class CircleSecition(CrossSection):
    r=None      #circle ratio

    def __init__ (self, r: float = 0.2):
        self.r=r

    @property
    def area(self):
        return (pi*self.r*self.r)
    
    @property
    def perimetro(self):
        return (2*pi*self.r)

    @property
    def inertia_x(self):
        return (0.25*pi*(self.r**4))

    @property
    def inertia_y(self):
        return (0.25*pi*(self.r**4))
        
    @property
    def inertia_z(self):
        return (0.25*pi*(self.r**4))
