import pandas as pd


class Grua:
    
    def __init__(self, tiempo_servicio, capacidad, serv_min):
        self.estado = "Cargando P1"
        self.cola_parada_uno = []
        self.cola_parada_dos = []
        self.tiempo_servicio = tiempo_servicio
        self.capacidad = capacidad
        self.serv_min = serv_min
        self.carga = 0
    
    def suficiente_carga(self, parada_uno):
        if parada_uno == True:
            return len(self.cola_parada_uno) >= self.serv_min
        else:
            return len(self.cola_parada_dos) >= self.serv_min

    def realizar_abandono(self, tiempo_actual, abandono):
        abandona = [x for x in self.cola_parada_uno if x.abandono == abandono]
        if len(abandona) > 0:
            self.cola_parada_uno.remove(abandona)
        else:
            abandona = [x for x in self.cola_parada_dos if x.abandono == abandono]
            self.cola_parada_dos.remove(abandona)
    
    def trasladar(self, tiempo_actual):
        if self.estado == "Cargando P1":
            if self.suficiente_carga(True):
                while self.carga < self.capacidad and len(self.cola_parada_uno) > 0:
                    auto_actual = self.cola_parada_uno.pop(0)
                    auto_actual.fin_espera = tiempo_actual
                    auto_actual.estado = "Viajando a P2"
                    auto_actual.fin_traslado = tiempo_actual + self.tiempo_servicio
                    auto_actual.abandono.activo = 0
                    self.carga += 1
                self.estado = "Viajando a P2"
                return ["P2", tiempo_actual + self.tiempo_servicio]
            else:
                return None
        elif self.estado == "Cargando P2":
            if self.suficiente_carga(False):
                while self.carga < self.capacidad and len(self.cola_parada_dos) > 0:
                    auto_actual = self.cola_parada_dos.pop(0)
                    auto_actual.fin_espera = tiempo_actual
                    auto_actual.estado = "Viajando a P1"
                    auto_actual.fin_traslado = tiempo_actual + self.tiempo_servicio
                    auto_actual.abandono.activo = 0
                    self.carga += 1
                self.estado = "Viajando a P1"
                return ["P1", tiempo_actual + self.tiempo_servicio]
        else:
            return None
    
class Auto:
    
    def __init__(self, index, num_parada, hora_llegada):
        self.index = index
        self.estado = "En P1" if num_parada == 1 else "En P2"
        self.abandono = None
        self.hora_llegada = hora_llegada
        self.fin_espera = "-"
        self.fin_traslado = "-"
        
    def get_vector(self, nro_iteracion):
        i = str(self.index)
        columnas = ["Auto "+ i, "Estado "+ i,
                    "Llegada "+ i, "Fin espera "+ i, 
                    "Fin traslado "+ i]
        vector = pd.DataFrame(columns=columnas, index=[nro_iteracion])
        vector.loc[nro_iteracion]["Auto "+ i] = i
        vector.loc[nro_iteracion]["Estado "+ i] = self.estado
        vector.loc[nro_iteracion]["Llegada "+ i] = self.hora_llegada
        vector.loc[nro_iteracion]["Fin espera "+ i] = self.fin_espera
        vector.loc[nro_iteracion]["Fin traslado "+ i] = self.fin_traslado
        return vector
        
        
class Evento:

    def __init__(self, nombre, hora):
        self.nombre = nombre
        self.hora = hora
        self.activo = 1
        
       


