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
# Importación para estilos personalizados. (JHAR)
from tkinter import ttk
# Textwrap ayuda a mejorar la presentación del
# texto en el mensaje informativo de ver_reserva. (JHAR)
import textwrap
import os

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
class ReservaError(Exception):
    """Error base para operaciones de reserva."""
class FechaInvalidaError(ReservaError):
    """Fecha de inicio posterior o igual a fecha de fin."""
class ClienteNoSeleccionadoError(ReservaError):
    """No se seleccionó un cliente."""
class ServicioNoSeleccionadoError(ReservaError):
    """No se seleccionó un servicio."""
class DescuentoInvalidoError(ReservaError):
    """Combinación de descuento inválida."""

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
        dias = (self.fin - self.inicio).days + 1
        return self.servicio.calcular_costo(dias)

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ValueError("La reserva ya está cancelada")

        self.estado = "Cancelada"
        Logger.registrar("Reserva cancelada")

# ============================================
# REQUERIMIENTO R4
# INTERFAZ TKINTER(JFM)
# Se crea la interfaz de la ventana 
# ============================================
class SistemaGUI:
    
    # Por buenas prácticas se realiza actualizaciones:
    # a) en la forma como inicializa la clase SistemaGUI
    # y b) se actualiza las referencias de root a 
    # sel.root en todo el código. (JHAR)
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Software FJ")

        self.clientes = []
        self.reservas = []
        self.servicios = {
            "Escoge un servicio": None,
            "Sala": ReservaSala(),
            "Equipos": AlquilerEquipos(),
            "Asesoria": AsesoriaEspecializada()
        }

        # Aporto funcionalidad al requerimiento R3, para mejorar la
        # la visualización de la ventana del programa. (JHAR)
        self.centrar_ventana(self.root, 566, 800)
        
        self.root.mainloop()

    # ------- Funcionalidad para centrar la ventana (JHAR) -------
    
    def centrar_ventana(self, ventana, ancho, alto):
        
        # Variables para obtener el ancho y el alto de la pantalla. (JHAR)
        ancho_dispositivo = ventana.winfo_screenwidth()
        alto_dispositivo = ventana.winfo_screenheight()
        
        # Calculos para centrar la ventana. (JHAR)
        posicion_x = round((ancho_dispositivo - ancho) / 2)
        posicion_y = round((alto_dispositivo - alto) / 2)
        
        # Le indico a Python como centar la ventana. (JHAR)
        ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")
    
        # -------- Sección de personalización para R6 (JHAR) --------
        
        # Este estilo ayuda a no saturar el código
        # de la etiqueta del título de R6. (JHAR)
        estilo_interfaz = ttk.Style()
        estilo_interfaz.theme_use('clam')
    
        estilo_interfaz.configure('Titulo.TLabel',
                                  background='#1d2d44',
                                  foreground='white',
                                  font=('Tahoma', 11, 'bold'))

        # -------- REGISTRO CLIENTE (JFM)--------
        
        # "Se crea la etiqueta para mostar donde se debe 
        # ingresar el numero de identificacion del cliente: tk.Label , 
        # al frente se crea el espacio donde se puede escribir el numero: tk.Entry "
        
        tk.Label(self.root, text="ID Cliente").grid(row=0, column=0)
        self.id_entry = tk.Entry(self.root)
        self.id_entry.grid(row=0, column=1)


     # "Se crea la etiqueta para mostar donde se debe 
     # ingresar nombre del cliente: tk.Label  
     # al frente se crea el espacio donde se puede escribir el nombre: tk.Entry"
        
        tk.Label(self.root, text="Nombre").grid(row=1, column=0)
        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.grid(row=1, column=1, sticky="ew")

        
     #"Boton para registrar los datos ingresados"
     
        tk.Button(self.root, text="Registrar Cliente", command=self.registrar_cliente).grid(row=2, column=0, columnspan=2)

        # -------- SELECCIÓN CLIENTE (JFM)--------
        
     # "Se crea la etiqueta para mostar donde seleccionar
     # el cliente: tk.Label  
     # al frente se crea el espacio donde queda el boton en forma 
     # de lista para selecionar los clientes "
        
        tk.Label(self.root, text="Seleccionar Cliente").grid(row=3, column=0)
        self.cliente_var = tk.StringVar()
        self.menu_clientes = tk.OptionMenu(self.root, self.cliente_var, "")
        self.menu_clientes.grid(row=3, column=1)


        # -------- SERVICIO (JFM) --------
        
     # "Se crea la etiqueta para mostar donde seleccionar
     # el servicio: tk.Label  
     # al frente se crea el espacio donde queda el boton en forma 
     # de lista para selecionar los servicios "
        
        tk.Label(self.root, text="Servicio").grid(row=4, column=0)
        self.servicio_var = tk.StringVar(value="Escoge un servicio")
        tk.OptionMenu(self.root, self.servicio_var, *self.servicios.keys())\
        .grid(row=4, column=1, sticky="ew")

        # -------- FECHAS (JFM)--------
        
     # "Se crea la etiqueta para mostar donde ingresar
     # la fecha de inicio: tk.Label  
     # al frente se crea el espacio donde queda el espacio 
     # para ingresar la fecha "
     
        tk.Label(self.root, text="Inicio (YYYY-MM-DD)").grid(row=5, column=0, sticky="e", padx=4)
        self.inicio_entry = tk.Entry(self.root)
        self.inicio_entry.grid(row=5, column=1, sticky="ew")
    
     # "Se crea la etiqueta para mostar donde ingresar
     # la fecha de fin tk.Label  
     # al frente se crea el espacio donde queda el espacio 
     # para ingresar la fecha "
     
        tk.Label(self.root, text="Fin (YYYY-MM-DD)").grid(row=6, column=0, sticky="e", padx=4)
        self.fin_entry = tk.Entry(self.root)
        self.fin_entry.grid(row=6, column=1, sticky="ew")

# -------- SECCIÓN 5: VISTA PREVIA --------
        ttk.Label(self.root, text="Vista previa:").grid(row=8, column=0, sticky="nw", padx=4)
        self.preview = tk.Text(self.root, height=5, width=40)
        self.preview.grid(row=8, column=1, columnspan=3, pady=4)
        # -------- BOTONES (JFM)--------
        # -------- SECCIÓN 4: DESCUENTOS --------
        self.descuento_habilitado = tk.BooleanVar()
        ttk.Checkbutton(self.root, text="Aplicar descuento", variable=self.descuento_habilitado)\
    .grid(row=7, column=0, sticky="w", padx=4)

        self.desc_5  = tk.BooleanVar()
        self.desc_10 = tk.BooleanVar()
        self.desc_15 = tk.BooleanVar()
        ttk.Checkbutton(self.root, text="5%",  variable=self.desc_5) .grid(row=7, column=1)
        ttk.Checkbutton(self.root, text="10%", variable=self.desc_10).grid(row=7, column=2)
        ttk.Checkbutton(self.root, text="15%", variable=self.desc_15).grid(row=7, column=3)

     # "Se crean los botones para 
     # crear reseva, Cancelar Reserva , mostrar  logs, limpiar campos y Salir
        tk.Button(self.root, text="Crear Reserva", command=self.crear_reserva).grid(row=7, column=0, columnspan=2)
        # Modificó está línea para redistribuir la interfaz
        # mejorando su presentación. (JFM - JHAR)
        tk.Button(self.root, text="Cancelar Reserva", command=self.cancelar_reserva).grid(row=9, column=2, columnspan=2, sticky="ew", padx=2)
       
        tk.Button(self.root, text="Limpiar",  command=self.limpiar).grid(row=10, column=0, sticky="ew", padx=2)
        tk.Button(self.root, text="Ver Logs", command=self.mostrar_logs).grid(row=10, column=1, sticky="ew", padx=2)
        # -------- SECCIÓN 7: LISTA DE RESERVAS (JFM) --------
        self.lista = tk.Listbox(self.root, width=60)
        self.lista.grid(row=11, column=0, columnspan=4, pady=(6, 4))
        
        tk.Button(self.root, text="Salir", command=self.salir, bg="red", fg="white").grid(row=10, column=0, columnspan=2)
    # ===================================================
    # REQUERIMIENTO R6
    # Diseñar sección de visualización de reservas
    # Se crea la sección según las necesidades del
    # programa según las necesidades actuales. (JHAR)
    # ===================================================
        
    # Contenedor que desplegará la sección de las reservas
    # creadas. (JHAR)
        cont_reservas_creadas = tk.Frame(self.root, background="#8CB7E2")
        cont_reservas_creadas.columnconfigure(0, weight=6)
        cont_reservas_creadas.columnconfigure(1, weight=1)
        cont_reservas_creadas.rowconfigure(1, weight=1)
        cont_reservas_creadas.grid(row=9, column=0, columnspan=3, padx=20, pady=15, sticky='nsew')
        
    # Etiqueta para el título de R6. (JHAR)   
        tit_reservas_contratadas = ttk.Label(cont_reservas_creadas,
                                      text='Reservas Contratadas',
                                      style='Titulo.TLabel',
                                      anchor='center',
                                      padding=10)
        tit_reservas_contratadas.grid(row=0, column=0, columnspan=2, sticky='we')
        
        # -------- LISTA DE RESERVAS y CONTROLES (JFM-JHAR) --------
        self.lista = tk.Listbox(cont_reservas_creadas, width=60)
        self.lista.grid(row=1, column=0, padx=10, pady=10)
        
        # Contenedor para organizar los botones correspondientes
        # a R6. (JHAR)
        cont_botones = tk.Frame(cont_reservas_creadas, background="#8CB7E2")
        cont_botones.rowconfigure(0, weight=1)
        cont_botones.rowconfigure(1, weight=1)
        cont_botones.rowconfigure(2, weight=1)
        cont_botones.rowconfigure(3, weight=1)
        cont_botones.columnconfigure(1, weight=1)
        cont_botones.grid(row=1, column=1, padx=10, pady=10, sticky='n')
        
        # Agrego el botón de ver detalle de la reserva. (JHAR)
        bot_ver_reserva = tk.Button(cont_botones, text="Ver Reserva", command=self.ver_reserva)
        bot_ver_reserva.grid(row=0, column=1, padx=10, pady=10, sticky='we')
        
        
        # Se actualiza donde se muestra el botón cancelar
        # reserva. (JFM - JHAR)
        tk.Button(cont_botones, text="Cancelar Reserva", command=self.cancelar_reserva).grid(row=1, column=1, padx=10, pady=10, sticky='we')

   
    # =========================
    # FUNCIONES
    # =========================
    def registrar_cliente(self):
        try:
            cliente = Cliente(self.id_entry.get(), self.nombre_entry.get())
            self.clientes.append(cliente)

            menu = self.menu_clientes["menu"]
            menu.delete(0, "end")

            for c in self.clientes:
                menu.add_command(label=c.get_nombre(),
                                 command=lambda value=c.get_nombre(): self.cliente_var.set(value))

            messagebox.showinfo("OK", "Cliente registrado")

        except Exception as e:
            Logger.registrar(str(e))
            messagebox.showerror("Error", str(e))

    def obtener_cliente(self):
        nombre = self.cliente_var.get()
        for c in self.clientes:
            if c.get_nombre() == nombre:
                return c
        raise ValueError("Debe seleccionar un cliente")

    def crear_reserva(self):
        try:
            cliente = self.obtener_cliente()
            servicio = self.servicios[self.servicio_var.get()]

            reserva = Reserva(
                cliente,
                servicio,
                self.inicio_entry.get(),
                self.fin_entry.get()
            
            )
            
            
            descuento = self.obtener_descuento()

            if descuento > 0:
              reserva.costo = reserva.costo - (reserva.costo * descuento / 100)
            
            
               
               
               
            self.reservas.append(reserva)

            self.lista.insert(tk.END,
                f"{cliente.get_nombre()} - {servicio.nombre} - ${reserva.costo} - {reserva.estado}"
            )

            messagebox.showinfo("OK", "Reserva creada")

        except Exception as e:
            Logger.registrar(str(e))
            messagebox.showerror("Error", str(e))
    
    def obtener_descuento(self):

        # Si no está activado el descuento, retorna 0%
        if not self.descuento_habilitado.get():
            return 0

        # Verifica qué checkbox está activo
        if self.desc_5.get():
            return 5
        if self.desc_10.get():
            return 10
        if self.desc_15.get():
            return 15

        return 0
    # Función para ver detalle completo de la reserva. (JHAR - JJBT)
    def ver_reserva(self):
       self.preview.delete("1.0", tk.END)
       
       # Se usa textwrap para mejorar la presentación
       # y con esto se corrige la identación. (JHAR)
       texto = textwrap.dedent(f"""
                Cliente: {self.cliente_var.get()}
                Servicio: {self.servicio_var.get()}
                Inicio: {self.inicio_entry.get()}
                Fin: {self.fin_entry.get()}
                Descuento: {self.obtener_descuento()}%
                """)
       self.preview.insert(tk.END, texto)
    
    def cancelar_reserva(self):
        try:
            seleccion = self.lista.curselection()
            if not seleccion:
                raise ValueError("Seleccione una reserva")

            i = seleccion[0]
            self.reservas[i].cancelar()

            self.lista.delete(i)
            r = self.reservas[i]

            self.lista.insert(i,
                f"{r.cliente.get_nombre()} - {r.servicio.nombre} - ${r.costo} - {r.estado}"
            )

        except Exception as e:
            Logger.registrar(str(e))
            messagebox.showerror("Error", str(e))
    def validar_fechas(self):
        try:
            # Construimos fechas reales
            inicio = datetime.date(2025, int(self.inicio_entry.get()))
            fin = datetime.date(2025, int(self.fin_entry.get()))

            # Validación lógica
            if fin <= inicio:
                raise ValueError("La fecha final debe ser mayor a la inicial")

            return inicio, fin

        except Exception as e:
            # Encadenamiento de error
            raise ValueError("Error en fechas: " + str(e))


    # Limpia todos los campos
    def limpiar(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.servicio_var.set("")
        self.inicio_entry.delete(0, tk.END)
        self.fin_entry.delete(0, tk.END)
        self.descuento_habilitado.set(False)
        self.desc_5.set(False)
        self.desc_10.set(False)
        self.desc_15.set(False)
        self.preview.delete("1.0", tk.END)


    # Muestra los logs del sistema
    def mostrar_logs(self):
     if not os.path.exists("logs.txt"):
        messagebox.showinfo("Logs", "No hay registros de errores.")
        return

     with open("logs.txt", "r") as archivo:
        contenido = archivo.read().strip()

     if not contenido:
        messagebox.showinfo("Logs", "No hay registros de errores.")
        return

    # Ventana emergente con los logs
     ventana = tk.Toplevel(self.root)
     ventana.title("Registros del sistema")
     ventana.geometry("600x400")
 
     texto = tk.Text(ventana, wrap="word", state="normal")
     texto.insert("1.0", contenido)
     texto.config(state="disabled")  # solo lectura

     scroll = tk.Scrollbar(ventana, command=texto.yview)
     texto.config(yscrollcommand=scroll.set)

     texto.pack(side="left", fill="both", expand=True)
     scroll.pack(side="right", fill="y")
     
    def salir(self):
        Logger.registrar("Sistema cerrado")
        self.root.destroy()

# ============================================
# Inicialización de programa (JFM - JHAR)
# ============================================
if __name__ == "__main__":
    SistemaGUI()