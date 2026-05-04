# Grupo_129.
# Fase 4: Sistema Integral de Gestión de Clientes, Servicios y Reservas.
# Ingeniería de Sistemas.
# Autoría propia.
print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")


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
    @staticmethod
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
# SERVICIOS (POLIMORFISMO) (EGC
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
# INICIO REQUERIMIENTO R1
# Clase Cliente: ingreso de datos (EGC) 
# ============================================
class Cliente:
    def __init__(self, identificacion, nombre):
        self.__identificacion = None
        self.__nombre = None

        self.set_identificacion(identificacion)
        self.set_nombre(nombre)

    def set_identificacion(self, identificacion):
        if not identificacion.isdigit():
            raise IdentificacionInvalidaError("La identificación debe ser numérica")
        self.__identificacion = identificacion

    def set_nombre(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

# ============================================
# REQUERIMIENTO R3)
# CLASE RESERVA  (JFM)
# ============================================
class Reserva:
    def __init__(self, cliente, servicio, inicio, fin):
        try:
            self.cliente = cliente
            self.servicio = servicio

            self.inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
            self.fin = datetime.datetime.strptime(fin, "%Y-%m-%d")

            if self.fin <= self.inicio:
                raise ValueError("La fecha final debe ser mayor a la inicial")

            self.estado = "Activa"
            self.costo = self.calcular()

            Logger.registrar(f"Reserva creada para {cliente.get_nombre()}")

        except Exception as e:
            Logger.registrar(f"Error en reserva: {e}")
            raise

    def calcular(self):
        dias = (self.fin - self.inicio).days
        return self.servicio.calcular_costo(dias)

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ValueError("La reserva ya está cancelada")

        self.estado = "Cancelada"
        Logger.registrar("Reserva cancelada")

# ============================================
# REQUERIMIENTO R4
# INTERFAZ TKINTER(JFM)
# ============================================
class SistemaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ")

        self.clientes = []
        self.reservas = []

        self.servicios = {
            "Sala": ReservaSala(),
            "Equipos": AlquilerEquipos(),
            "Asesoria": AsesoriaEspecializada()
        }

        # -------- REGISTRO CLIENTE (JFM)--------
        tk.Label(root, text="ID Cliente").grid(row=0, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1)

        tk.Label(root, text="Nombre").grid(row=1, column=0)
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.grid(row=1, column=1)

        tk.Button(root, text="Registrar Cliente", command=self.registrar_cliente).grid(row=2, column=0, columnspan=2)

        # -------- SELECCIÓN CLIENTE (JFM)--------
        tk.Label(root, text="Seleccionar Cliente").grid(row=3, column=0)
        self.cliente_var = tk.StringVar()
        self.menu_clientes = tk.OptionMenu(root, self.cliente_var, "")
        self.menu_clientes.grid(row=3, column=1)

        # -------- SERVICIO (JFM) --------
        tk.Label(root, text="Servicio").grid(row=4, column=0)
        self.servicio_var = tk.StringVar(value="Sala")
        tk.OptionMenu(root, self.servicio_var, *self.servicios.keys()).grid(row=4, column=1)

        # -------- FECHAS (JFM)--------
        tk.Label(root, text="Inicio (YYYY-MM-DD)").grid(row=5, column=0)
        self.inicio_entry = tk.Entry(root)
        self.inicio_entry.grid(row=5, column=1)

        tk.Label(root, text="Fin").grid(row=6, column=0)
        self.fin_entry = tk.Entry(root)
        self.fin_entry.grid(row=6, column=1)

        # -------- BOTONES (JFM)--------
        tk.Button(root, text="Crear Reserva", command=self.crear_reserva).grid(row=7, column=0, columnspan=2)
        tk.Button(root, text="Cancelar Reserva", command=self.cancelar_reserva).grid(row=8, column=0, columnspan=2)
        tk.Button(root, text="Salir", command=self.salir, bg="red", fg="white").grid(row=10, column=0, columnspan=2)
        
        # -------- LISTA (JFM)--------
        self.lista = tk.Listbox(root, width=60)
        self.lista.grid(row=9, column=0, columnspan=2)

        
        
