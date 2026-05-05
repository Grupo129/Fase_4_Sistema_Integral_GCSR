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

    # ============================================
    # ===== INICIO REQUERIMIENTO R7 =====
    # Validación de identificación (EGC)
    # ============================================
    def set_identificacion(self, identificacion):
        if not identificacion.isdigit():
            Logger.registrar("ERROR R7: Identificación no numérica")
            raise IdentificacionInvalidaError("Solo números permitidos")

        self.__identificacion = identificacion

    def set_nombre(self, nombre):
        if nombre.strip() == "":
            raise ValueError("Nombre vacío")
        self.__nombre = nombre

    def get_datos(self):
        return f"{self.__identificacion} - {self.__nombre} | {self.servicio.nombre}"


# ============================================
# GESTOR DEL SISTEMA (EGC)
# ============================================
class GestorSistema:

    def __init__(self):
        self.clientes = []
        self.servicios = [
            ReservaSala(),
            AlquilerEquipos(),
            AsesoriaEspecializada()
        ]

    # ============================================
    # ===== INICIO REQUERIMIENTO R1 + R2 =====
    # Registro de cliente + asignación de servicio (EGC)
    # ============================================
    def registrar_cliente(self, identificacion, nombre, servicio_index):
        try:
            servicio = self.servicios[servicio_index]
            cliente = Cliente(identificacion, nombre, servicio)
            self.clientes.append(cliente)
            return True

        except Exception as e:
            Logger.registrar(f"ERROR REGISTRO: {e}")
            return False


# ============================================
# INTERFAZ GRÁFICA (EGC)
# ============================================
sistema = GestorSistema()


def actualizar_lista():
    lista_clientes.delete(0, tk.END)
    for cliente in sistema.clientes:
        lista_clientes.insert(tk.END, cliente.get_datos())


# ============================================
# ===== INICIO REQUERIMIENTO R1 + R2 + R7 =====
# Botón para registrar cliente con validación (EGC)
# ============================================
def registrar_cliente():
    identificacion = entry_id.get()
    nombre = entry_nombre.get()
    seleccion_servicio = lista_servicios.curselection()

    if not seleccion_servicio:
        messagebox.showerror("Error", "Debe seleccionar un servicio")
        return

    servicio_index = seleccion_servicio[0]

    if sistema.registrar_cliente(identificacion, nombre, servicio_index):
        messagebox.showinfo("Éxito", "Cliente registrado correctamente")
        actualizar_lista()

        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Identificación inválida o datos incorrectos")


# ============================================
# VENTANA PRINCIPAL (EGC)
# ============================================
ventana = tk.Tk()
ventana.title("Sistema Software FJ")
ventana.geometry("450x450")


# CAMPOS DE ENTRADA (R1) (EGC)
tk.Label(ventana, text="Identificación").pack()
entry_id = tk.Entry(ventana)
entry_id.pack()

tk.Label(ventana, text="Nombre").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()


# ============================================
# ===== INICIO REQUERIMIENTO R2 =====
# Lista de servicios (sin mostrar precios) (EGC)
# ============================================
tk.Label(ventana, text="Seleccione un servicio").pack()
lista_servicios = tk.Listbox(ventana)

lista_servicios.insert(0, "Reserva de sala")
lista_servicios.insert(1, "Alquiler de equipos")
lista_servicios.insert(2, "Asesoría especializada")

lista_servicios.pack()


# BOTÓN (R1) (EGC)
tk.Button(ventana, text="Registrar Cliente", command=registrar_cliente).pack()


# LISTA DE CLIENTES (EGC)
tk.Label(ventana, text="Clientes registrados").pack()
lista_clientes = tk.Listbox(ventana, width=50)
lista_clientes.pack()


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
        
        
# =========================
# R8 - R9 (Tatiana)
# =========================

from datetime import datetime


# 🔷 LOGGER
class Logger:
    @staticmethod
    def registrar(mensaje):
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {mensaje}\n")


# 🔷 EXCEPCIONES
class ClienteNoSeleccionadoError(Exception):
    pass


class ServicioNoSeleccionadoError(Exception):
    pass


# 🔷 CLASES BASE
class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre


class Servicio:
    def __init__(self, nombre):
        self.nombre = nombre


# 🔷 R8: VALIDACIÓN
def r8_validar_cliente(cliente):
    if cliente is None:
        raise ClienteNoSeleccionadoError(
            "Debe seleccionar un cliente antes de usar servicios"
        )


# 🔷 R9: VALIDACIÓN
def r9_validar_servicio(servicio):
    if servicio is None:
        raise ServicioNoSeleccionadoError(
            "Debe seleccionar un servicio antes de registrar la reserva"
        )


# 🔷 MENÚ 
def menu():
    clientes = []
    cliente_actual = None
    servicios = [
        Servicio("Sala"),
        Servicio("Equipos"),
        Servicio("Asesoría")
    ]
    reservas = []

    while True:
        print("\n===== MENÚ =====")
        print("1. Registrar cliente")
        print("2. Seleccionar cliente")
        print("3. Mostrar servicios (R8)")
        print("4. Crear reserva (R9)")
        print("5. Salir")

        opcion = input("Seleccione: ")

        # 🔷 REGISTRAR CLIENTE
        if opcion == "1":
            nombre = input("Nombre del cliente: ")
            cliente = Cliente(nombre)
            clientes.append(cliente)
            print("✅ Cliente registrado")

        # 🔷 SELECCIONAR CLIENTE
        elif opcion == "2":
            if not clientes:
                print("⚠️ No hay clientes")
                continue

            for i, c in enumerate(clientes, 1):
                print(f"{i}. {c.nombre}")

            try:
                i = int(input("Seleccione cliente: ")) - 1
                cliente_actual = clientes[i]
                print("✅ Cliente seleccionado")

            except:
                print("❌ Selección inválida")

        # 🔷 R8: MOSTRAR SERVICIOS
        elif opcion == "3":
            try:
                r8_validar_cliente(cliente_actual)

                print("\n📋 Servicios:")
                for i, s in enumerate(servicios, 1):
                    print(f"{i}. {s.nombre}")

            except ClienteNoSeleccionadoError as e:
                print(f"⚠️ {e}")
                Logger.registrar(f"R8 - {e}")

        # 🔷 R9: CREAR RESERVA
        elif opcion == "4":
            try:
                r8_validar_cliente(cliente_actual)

                for i, s in enumerate(servicios, 1):
                    print(f"{i}. {s.nombre}")

                servicio = None

                try:
                    i = int(input("Seleccione servicio: ")) - 1
                    servicio = servicios[i]
                except:
                    servicio = None

                # 🔴 VALIDACIÓN R9
                r9_validar_servicio(servicio)

                reservas.append((cliente_actual.nombre, servicio.nombre))
                print("✅ Reserva registrada")

            except ClienteNoSeleccionadoError as e:
                print(f"⚠️ {e}")
                Logger.registrar(f"R8 - {e}")

            except ServicioNoSeleccionadoError as e:
                print(f"⚠️ {e}")
                Logger.registrar(f"R9 - {e}")

        elif opcion == "5":
            print("👋 Saliendo...")
            break

        else:
            print("❌ Opción inválida")

ventana.mainloop()