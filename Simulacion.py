from Clases import *
import random
import pandas as pd
import math


class Simulacion:

    def __init__(self, costo_auto, costo_abandono, costo_grua, tiempo, mostrar_desde, 
            iteraciones, tiempo_grua, capacidad_grua, min_serv_grua):
        self.cola_eventos = []
        self.grua = Grua(tiempo_grua, capacidad_grua, min_serv_grua)
        self.costo_auto = costo_auto
        self.costo_abandono = costo_abandono
        self.costo_grua = costo_grua
        self.tiempo = tiempo
        self.tiempo_actual = 0.0
        self.index_columnas = 0
        self.mostrar_desde = mostrar_desde
        self.iteraciones = iteraciones
        self.tiempo_grua = tiempo_grua
        self.capacidad_grua = capacidad_grua
        self.min_serv_grua = min_serv_grua
        self.cont_abandonos = 0
        self.cont_atendidos = 0
        self.acum_ganancias = 0.0
        self.acum_permanencia = 0.0
        self.objetos_temporales = []
        self.columnas = ["Estado","Reloj","RND P1","Tiempo lleg. P1","Prox. lleg. P1","RND P2","Tiempo lleg. P2","Prox. lleg. P2", "i de llegada",
                    "Destino traslado","Fin traslado","Estado grua","Cola P1","Cola P2","Acum. Ganancias",
                    "Cont. Perdidos","Cont. Atendidos","Acum. Permanencia"]
        
    def simular(self):
        tabla = pd.DataFrame()
        contador_filas = 0
        contador_objetos = 0

        fila_actual = []
        fin_mostrar = False
        ultima_fila = False
        self.agregar_evento(Evento("Inicio del dia", 0))

        while len([x for x in self.cola_eventos if x.nombre != "Abandono"])>0:
            prox_evento = self.cola_eventos.pop(0)
            self.tiempo_actual = prox_evento.hora
            ultima_fila = False

            if prox_evento.nombre == "Llegada auto P1":
                contador_objetos += 1
                nuevo_auto = Auto(contador_objetos, 1, self.tiempo_actual)
                self.grua.cola_parada_uno.append(nuevo_auto)
                nuevo_abandono = Evento("Abandono",self.tiempo_actual+10)
                self.agregar_evento(nuevo_abandono)
                nuevo_auto.abandono = nuevo_abandono
                self.agregar_obj_temp(nuevo_auto)
                evento_resp = self.grua.trasladar(self.tiempo_actual)
                rnd_llegada, tiempo_llegada = self.get_llegada_cliente(True)
                prox_llegada = tiempo_llegada+self.tiempo_actual
                if prox_llegada <= self.tiempo:
                    self.agregar_evento(Evento("Llegada auto P1",prox_llegada))
                if evento_resp is not None:
                    self.agregar_evento(evento_resp)
                    fila_actual = self.mostrar_llegada_traslado_p1(rnd_llegada,tiempo_llegada,evento_resp,nuevo_auto.index)
                elif not fin_mostrar and self.tiempo_actual >= self.mostrar_desde:
                    fila_actual = self.mostrar_llegada_p1(rnd_llegada, tiempo_llegada,nuevo_auto.index)
            elif prox_evento.nombre == "Llegada auto P2":
                contador_objetos += 1
                nuevo_auto = Auto(contador_objetos, 0, self.tiempo_actual)
                self.grua.cola_parada_dos.append(nuevo_auto)
                nuevo_abandono = Evento("Abandono", self.tiempo_actual + 10)
                self.agregar_evento(nuevo_abandono)
                nuevo_auto.abandono = nuevo_abandono
                self.agregar_obj_temp(nuevo_auto)
                evento_resp = self.grua.trasladar(self.tiempo_actual)
                rnd_llegada, tiempo_llegada = self.get_llegada_cliente(False)
                prox_llegada = tiempo_llegada + self.tiempo_actual
                if prox_llegada <= self.tiempo:
                    self.agregar_evento(Evento("Llegada auto P2", prox_llegada))
                if evento_resp is not None:
                    self.agregar_evento(evento_resp)
                    fila_actual = self.mostrar_llegada_traslado_p2(rnd_llegada,tiempo_llegada,evento_resp,nuevo_auto.index)
                elif not fin_mostrar and self.tiempo_actual >= self.mostrar_desde:
                    fila_actual = self.mostrar_llegada_p2(rnd_llegada, tiempo_llegada,nuevo_auto.index)
            elif prox_evento.nombre == "Arribo a P1":
                self.grua.estado = "Esperando en P1"
                cargados = [n for n in self.objetos_temporales if n.estado == "Viajando a P1"]
                for auto in cargados:
                    auto.estado = "Destino"
                    self.cont_atendidos += 1
                    self.grua.carga -= 1
                    self.acum_ganancias += self.costo_auto
                    self.acum_permanencia += auto.fin_traslado-auto.hora_llegada
                self.acum_ganancias -= self.costo_grua
                evento_resp = self.grua.trasladar(self.tiempo_actual)
                if evento_resp is not None:
                    self.agregar_evento(evento_resp)
                    fila_actual = self.mostrar_recibe_traslado_p1(evento_resp)
                else:
                    fila_actual = self.mostrar_recibe_p1()
            elif prox_evento.nombre == "Arribo a P2":
                self.grua.estado = "Esperando en P2"
                cargados = [n for n in self.objetos_temporales if n.estado == "Viajando a P2"]
                for auto in cargados:
                    auto.estado = "Destino"
                    self.cont_atendidos += 1
                    self.grua.carga -= 1
                    self.acum_ganancias += self.costo_auto
                    self.acum_permanencia += auto.fin_traslado - auto.hora_llegada
                self.acum_ganancias -= self.costo_grua
                evento_resp = self.grua.trasladar(self.tiempo_actual)
                if evento_resp is not None:
                    self.agregar_evento(evento_resp)
                    fila_actual = self.mostrar_recibe_traslado_p2(evento_resp)
                else:
                    fila_actual = self.mostrar_recibe_p2()
            elif prox_evento.nombre == "Abandono":
                if 1 == prox_evento.activo:
                    self.grua.realizar_abandono(self.tiempo_actual, prox_evento)
                    self.cont_abandonos += 1
                    self.acum_ganancias -= self.costo_abandono
                    if not fin_mostrar and self.tiempo_actual >= self.mostrar_desde:
                        fila_actual = self.mostrar_abandono()
            elif prox_evento.nombre == "Inicio del dia":
                rnd_llegada_uno, tiempo_llegada_uno = self.get_llegada_cliente(True)
                prox_llegada_uno = tiempo_llegada_uno + self.tiempo_actual
                if prox_llegada_uno <= self.tiempo:
                    self.agregar_evento(Evento("Llegada auto P1", prox_llegada_uno))
                rnd_llegada_dos, tiempo_llegada_dos = self.get_llegada_cliente(False)
                prox_llegada_dos = tiempo_llegada_dos + self.tiempo_actual
                if prox_llegada_dos <= self.tiempo:
                    self.agregar_evento(Evento("Llegada auto P2", prox_llegada_dos))
                if not fin_mostrar and self.tiempo_actual >= self.mostrar_desde:
                    fila_actual = self.mostrar_inicio_dia(rnd_llegada_uno, tiempo_llegada_uno,
                                                          rnd_llegada_dos,tiempo_llegada_dos)

            if contador_filas >= self.iteraciones:
                fin_mostrar = True

            if not fin_mostrar and self.tiempo_actual >= self.mostrar_desde and isinstance(fila_actual,list):
                contador_filas += 1
                fila_actual = self.completar_fila(fila_actual, contador_filas)
                ultima_fila = True
                if contador_filas == 1:
                    tabla = fila_actual
                else:
                    if len(fila_actual.columns.tolist()) != len(tabla.columns.tolist()):
                        tabla = pd.concat([tabla, fila_actual])[fila_actual.columns.tolist()]
                    else:
                        tabla = pd.concat([tabla, fila_actual])


        #No toca contenido de aca para abajo
        tabla_recortada = tabla.loc[:][0:int(contador_filas)]
        if contador_filas != 0 and ultima_fila:
            tabla_recortada.loc[contador_filas]["Estado"] = "Fin atencion"
        return tabla_recortada

        
    def get_llegada_cliente(self, parada_uno):
        rnd = random.random()
        if parada_uno:
            tiempo_espera = (-1) * math.log(1 - rnd)
            return [rnd,tiempo_espera]
        else:
            tiempo_espera = (-15/8) * math.log(1 - rnd)
            return [rnd,tiempo_espera]

    def agregar_obj_temp(self, obj):
        descarte = [n for n in self.objetos_temporales if n.estado in set(["Destino","Abandono"])]
        if len(descarte) > 0:
            obj.index = descarte[0].index
            index = self.objetos_temporales.index(descarte[0])
            self.objetos_temporales[index] = obj
        else:
            self.objetos_temporales.append(obj)
            self.index_columnas += 1
            obj.index = self.index_columnas


    def agregar_evento(self, eventos):
        if type(eventos) != list:
            self.cola_eventos.append(eventos)
        else:
            for e in eventos:
                self.cola_eventos.append(e)
        self.cola_eventos.sort(key=lambda evento: evento.hora)

    def mostrar_inicio_dia(self,rnd_p1,tiempo_p1,rnd_p2,tiempo_p2):
        return ["Inicio del dia", self.tiempo_actual,rnd_p1,tiempo_p1,tiempo_p1, rnd_p2, tiempo_p2,tiempo_p2, "-",
                "-", "-", self.grua.estado,len(self.grua.cola_parada_uno),len(self.grua.cola_parada_dos),0.0,0,0,0]

    def mostrar_abandono(self):
        return ["Abandono", self.tiempo_actual,"-","-","-","-","-","-","-","-","-",self.grua.estado,
                len(self.grua.cola_parada_uno),len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]


    def mostrar_llegada_traslado_p1(self,rnd,tiempo,evento_resp,i):
        return ["Llegada auto P1", self.tiempo_actual, rnd, tiempo, tiempo+self.tiempo_actual,"-","-","-",i,
                "P2", evento_resp.hora, "Viajando a P2",len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]

    def mostrar_llegada_p1(self, rnd, tiempo,i):
        return ["Llegada auto P1", self.tiempo_actual, rnd, tiempo, tiempo+self.tiempo_actual,"-","-","-",i,
                "-", "-", self.grua.estado, len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]

    def mostrar_llegada_traslado_p2(self,rnd,tiempo,evento_resp,i):
        return ["Llegada auto P2", self.tiempo_actual, "-","-","-", rnd, tiempo, tiempo+self.tiempo_actual,i,
                "P1", evento_resp.hora, "Viajando a P1",len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]

    def mostrar_llegada_p2(self, rnd, tiempo,i):
        return ["Llegada auto P2", self.tiempo_actual, "-","-","-", rnd, tiempo, tiempo+self.tiempo_actual,i,
                "-", "-", self.grua.estado, len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]

    def mostrar_recibe_traslado_p1(self, evento_resp):
        return ["Arribo a P1", self.tiempo_actual, "-", "-", "-", "-", "-", "-","-","P2", evento_resp.hora,
                self.grua.estado, len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]

    def mostrar_recibe_p1(self):
        return ["Arribo a P1", self.tiempo_actual, "-", "-", "-", "-", "-", "-","-","-","-",
                self.grua.estado, len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]

    def mostrar_recibe_traslado_p2(self,evento_resp):
        return ["Arribo a P2", self.tiempo_actual, "-", "-", "-", "-", "-", "-","-", "P1", evento_resp.hora,
                self.grua.estado, len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos), self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos, self.acum_permanencia]

    def mostrar_recibe_p2(self):
        return ["Arribo a P2", self.tiempo_actual, "-", "-", "-", "-", "-", "-","-","-","-",
                self.grua.estado, len(self.grua.cola_parada_uno),
                len(self.grua.cola_parada_dos),self.acum_ganancias, self.cont_abandonos,
                self.cont_atendidos,self.acum_permanencia]


    def completar_fila(self,fila_actual,nro_fila):
        fila = pd.DataFrame(columns = self.columnas, index = [nro_fila])
        fila.loc[nro_fila] = fila_actual
        for x in self.objetos_temporales:
            fila = pd.concat([fila,x.get_vector(nro_fila)], axis=1)
        return fila


#s = Simulacion(2.5,1.5,7,480,0,1000,6,5,5)
#s = Simulacion(2.5,1.5,7,480,400,50,4,5,3)
#print(s.simular())
#tabla = s.simular()
#dfgui.show(tabla)
#View(tabla)