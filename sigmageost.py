def PolyArea(x,y): #Funcion que obtiene el area de un poligono por coordenadas
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
    