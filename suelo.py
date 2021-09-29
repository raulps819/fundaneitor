from math import sqrt
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from capa import Capa

from os import system
from os import path
from os import getcwd
import pandas as pd

import time
from os import system

class Suelo():
    
    capas = []
    n_fret = 0.0
    pext=0.0
    gamma_h20= 0.0 #kpa dividir en 1000, Pa no dividir
    
    def __init__(self,Capas: list=[],n_fret: float=0,pext: float=0,gamma_h20: float=9.81):
        """
        Objeto generico de tipo suelo
            - Capas = Lista que contiene objetos de tipo capa correpondiente al suelo
            - n_fret = Nivel freatico del suelos (Unidades de longitud)
            - pext = Presion externa o sobrecarga+
            - gamma_h20 = Peso especifico del agua
        """
        self.capas=Capas
        self.n_fret=n_fret
        self.pext = pext
        self.gamma_h20=gamma_h20
        pass
 
    def ptcapa(self,prof_pt: float=None,floor: bool=False):
        """
        Devuelve el numero de capa en la que se encuentra un punto dentro del suelo,
        si el punto se encuentra entre dos capas devuelve una lista con ambos indices
           - prof_pt: profundidad del punto para el que se busca la capa
           - floor: Ingrese True si desea la capa mas baja en caso de que el punto este entre dos capas 
        """
        c=0
        if prof_pt == 0:
            return c
        else:
            for capa in self.capas:
                if capa.prof_final==prof_pt:
                    if c == (len(self.capas)-1):
                        return c
                    else:
                        if floor==False:
                            c=[c,c+1]
                        else:
                            c=c+1
                        return c
                elif capa.prof_init<prof_pt and capa.prof_final>prof_pt:
                    return c
                else:
                    pass
                c=c+1
            pass
        pass

    def ptpresionagua(self,prof_pt): #getter que halla la presion de poros en un punto
        """
        Devuelve la presion de poros en un punto
            - prof_pt = Profundidad del punto
        """
        p_agua=0.0
        if prof_pt<self.n_fret:
            p_agua=0.0
            pass
        else:
            p_agua=(prof_pt-self.n_fret)*self.gamma_h20
        return p_agua 

    def ptsigmav(self,prof_pt): #getter que halla el esfuerzo vertical en un punto 
        """
        Devuelve el esfuerzo vertical a una determinada profundidad
            - prof_pt = Profundidad del punto
        """
        sigmav=self.pext
        for capa in self.capas:
            capaini=capa.prof_init
            capafin=capa.prof_final
            if capa.prof_init >= prof_pt:
                break #se alcanzo una capa mas profunda a la del punto
            elif capa.prof_final <= prof_pt and capa.prof_final <= self.n_fret:
                #la capa esta encima y el nivel freatico esta debajo de la capa
                sigmav=sigmav + capa.gamma*(capa.prof_final - capa.prof_init)
                pass
            elif capa.prof_final <= prof_pt and capa.prof_init >= self.n_fret:
                #la capa esta encima y el nivel freatico en toda la capa
                sigmav=sigmav + capa.gamma_sat*(capa.prof_final-capa.prof_init)              
                pass
            elif capa.prof_final<prof_pt and capa.prof_init < self.n_fret and capa.prof_final>self.n_fret:
                #la capa esta encima, pero el nivel freatico esta al interior de esa capa
                sigmav=sigmav + capa.gamma*(self.n_fret-capa.prof_init)
                sigmav=sigmav + capa.gamma_sat*(capa.prof_final-self.n_fret)
                pass
            else: #el punto se encuentra en la capa actual 
                if capa.prof_init >= self.n_fret: #el nivel freatico esta por encima de la capa del punto
                    sigmav=sigmav + capa.gamma_sat*(prof_pt-capa.prof_init)   
                    pass
                elif capa.prof_final <= self.n_fret or prof_pt <= self.n_fret: #el nivel freatico esta debajo de la capa del punto o del punto
                    sigmav=sigmav + capa.gamma*(prof_pt-capa.prof_init)
                    pass
                elif capa.prof_final>self.n_fret and capa.prof_init<self.n_fret: 
                    ##el nivel freatico esta dentro de la capa del punto y ademas esta entre el inicio de la capa y el punto
                    sigmav=sigmav + capa.gamma*(self.n_fret-capa.prof_init)
                    sigmav=sigmav + capa.gamma_sat*(prof_pt-self.n_fret)
                    pass
                else:
                    print('error en sigma v del punto')
                pass
            pass
        pass
        return round(sigmav,3)

    def ptsigmave(self,prof_pt): #getter halla esfuerzo efectivo vertical en un punto
        """
        Devuelve el esfuerzo vertical efectivo a una determinada profundidad
            - prof_pt = Profundidad del punto
        """
        sigmave=self.ptsigmav(prof_pt)-self.ptpresionagua(prof_pt)
        sigmave=round(sigmave,3)
        return sigmave

    def ptsigmahe(self,prof_pt): #getter halla esfuerzo efectivo horizontal, si el punto esta entre dos capas devuelve ambas
        """
        Devuelve el esfuerzo horizontal efectivo a una determinada profundidad,
        si el punto es intermedio a dos capas devuelve una lista con el esfuerzo para cada una
            - prof_pt = Profundidad del punto
        """
        ptcapa=self.ptcapa(prof_pt)
        if type(ptcapa)==list:
            sigmahe=[]
            sigmahe.append(round(self.capas[(ptcapa[0])].ko * self.ptsigmave(prof_pt),3))
            sigmahe.append(round(self.capas[(ptcapa[1])].ko * self.ptsigmave(prof_pt),3))
            pass
        else:
            sigmahe=round((self.capas[ptcapa].ko * self.ptsigmave(prof_pt)),3)
            pass
        return sigmahe      

    def ptsigmah(self,prof_pt): #getter halla esfuerzo horizontal, si el punto esta entre dos capas devuelve ambas
        """
        Devuelve el esfuerzo horizontal total a una determinada profundidad,
        si el punto es intermedio a dos capas devuelve una lista con el esfuerzo para cada una
            - prof_pt = Profundidad del punto
        """
        sigmahe=self.ptsigmahe(prof_pt)
        if type(sigmahe)==list:
            sigmah=[]
            sigmah.append(round(sigmahe[0]+self.ptpresionagua(prof_pt),3))
            sigmah.append(round(sigmahe[1]+self.ptpresionagua(prof_pt),3))
            pass
        else:
            sigmah=round(sigmahe+self.ptpresionagua(prof_pt),3)
            pass
        return sigmah
