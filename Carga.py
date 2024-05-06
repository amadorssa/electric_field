
class Carga:
    
    def __init__(self, x, y, signo = 1):
        self.x = x
        self.y = y
        self.signo = signo
        self.valorCarga=1e-9 * signo
        self.id = None

    def Valor(self):
        return self.valorCarga

    def X(self):
        return self.x
    
    def Y(self):
        return self.y
    
    def Signo(self):
        return self.signo
    
    def obtenerId(self):
        return self.id
    
    def asignarId(self, id):
        self.id = id

    def asignarX(self, x):
        self.x = x
    
    def asignarY(self, y):
        self.y = y