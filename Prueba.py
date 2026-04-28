# ============================================
# IMPORTACIONES (EGC)
# ============================================
from abc import ABC, abstractmethod
import datetime
import tkinter as tk
from tkinter import messagebox


# ============================================
# LOGS DEL SISTEMA (EGC)
# ============================================
class Logger:
    def registrar(mensaje):
        with open("logs.txt", "a") as archivo:
            fecha = datetime.datetime.now()
            archivo.write(f"{fecha} - {mensaje}\n")


# ============================================
# EXCEPCIÓN PERSONALIZADA (EGC)
# ============================================
class IdentificacionInvalidaError(Exception):
    pass


# ============================================
# CLASE ABSTRACTA SERVICIO (EGC)
# ============================================
class Servicio(ABC):
    def __init__(self, nombre, precio_dia):
        self.nombre = nombre
        self.precio_dia = precio_dia

    @abstractmethod
    def calcular_costo(self, dias):
        pass


# ============================================
# SERVICIOS (POLIMORFISMO) (EGC)
# ============================================
class ReservaSala(Servicio):
    def __init__(self):
        super().__init__("Reserva de sala", 100)

    def calcular_costo(self, dias):
        return self.precio_dia * dias


class AlquilerEquipos(Servicio):
    def __init__(self):
        super().__init__("Alquiler de equipos", 80)

    def calcular_costo(self, dias):
        return self.precio_dia * dias


class AsesoriaEspecializada(Servicio):
    def __init__(self):
        super().__init__("Asesoría especializada", 150)

    def calcular_costo(self, dias):
        return self.precio_dia * dias


# ============================================
# ===== INICIO REQUERIMIENTO R1 =====
# Clase Cliente: ingreso de datos (EGC)
# ============================================
class Cliente:

    def __init__(self, identificacion, nombre, servicio):
        self.__identificacion = None
        self.__nombre = None
        self.servicio = servicio

        self.set_identificacion(identificacion)
        self.set_nombre(nombre)