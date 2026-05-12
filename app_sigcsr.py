# Grupo_129.
# Fase 4: Sistema Integral de Gestión de Clientes, Servicios y Reservas.
# Ingeniería de Sistemas.
# Autoría propia.
print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")


# ============================================
# IMPORTACIONES (EGC)
# ============================================

# Se importa ABC y abstractmethod para crear clases abstractas y métodos obligatorios que deberán implementar las clases hijas.
# Se importa datetime para trabajar con fechas y horas, especialmente para registrar eventos y errores en los logs.
# Se importa tkinter para crear la interfaz gráfica del sistema.
# Se importa messagebox para mostrar mensajes emergentes de advertencia, error o confirmación al usuario.
# Se importa os para posibles operaciones relacionadas con archivos y rutas del sistema.

from abc import ABC, abstractmethod
import datetime
import tkinter as tk
from tkinter import messagebox
# Importación para estilos personalizados. (JHAR)
from tkinter import ttk
# Textwrap ayuda a mejorar la presentación del texto en el mensaje informativo de ver_reserva. (JHAR)
import textwrap
import os

# ============================================
# LOGS DEL SISTEMA (EGC)
# ============================================

# Clase encargada de registrar eventos y errores del sistema dentro de un archivo de texto llamado logs.txt.
class Logger:
    # Método estático utilizado para guardar mensajes en el archivo de logs.
    @staticmethod
    def registrar(mensaje):
        with open("logs.txt", "a") as archivo:
            fecha = datetime.datetime.now()
            archivo.write(f"{fecha} - {mensaje}\n")

# ============================================
# EXCEPCIÓN PERSONALIZADA (EGC) 
# ============================================

#Excepciones personalizadas para manejar errores específicos del sistema
class IdentificacionInvalidaError(Exception):
    pass
class ReservaError(Exception):
    pass
    """Error base para operaciones de reserva."""

# INICIO REQUERIMIENTO R9 (YTVCH)
class ServicioNoSeleccionadoError(ReservaError):
    """Error lanzado cuando el servicio está vacío en el R2 (YTVCH)"""
    pass
# FIN REQUERIMIENTO R9 (YTVCH)

# ============================================
# CLASE ABSTRACTA SERVICIO (EGC)
# ============================================

# Clase abstracta que representa los servicios generales ofrecidos por el sistema. 
# Las clases hijas deberán implementar el método calcular_costo
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

# Clase hija que representa el servicio de reserva de salas.
# Hereda de la clase abstracta Servicio.
class ReservaSala(Servicio):
    def __init__(self):
        super().__init__("Reserva de sala", 100)

    def calcular_costo(self, dias):
        return self.precio_dia * dias

# Clase hija para el servicio de alquiler de equipos.
class AlquilerEquipos(Servicio):
    def __init__(self):
        super().__init__("Alquiler de equipos", 80)

    def calcular_costo(self, dias):
        return self.precio_dia * dias

# Clase hija para el servicio de asesoría especializada.
class AsesoriaEspecializada(Servicio):
    def __init__(self):
        super().__init__("Asesoría especializada", 150)

    def calcular_costo(self, dias):
        return self.precio_dia * dias

# ============================================
# INICIO REQUERIMIENTO R1
# Clase Cliente: ingreso de datos (EGC) 
# ============================================

#Clase Cliente encargada de almacenar y validar la información personal del cliente.
class Cliente:
    def __init__(self, identificacion, nombre):
        self.__identificacion = None
        self.__nombre = None

        self.set_identificacion(identificacion)
        self.set_nombre(nombre)

# ============================================
# INICIO REQUERIMIENTO R7
# Validación de identificación (EGC)
# ============================================

# Método encargado de validar que la identificación contenga únicamente valores numéricos. 
# Si la validación falla, se lanza una excepción personalizada.
    def set_identificacion(self, identificacion):

        # Elimina espacios
        identificacion = identificacion.strip()

        # Verifica que solo tenga números
        if not identificacion.isdigit():
            raise IdentificacionInvalidaError(
                "La identificación debe ser numérica"
            )

        # Valida longitud mínima y máxima
        if len(identificacion) < 6 or len(identificacion) > 10:
            raise IdentificacionInvalidaError(
                "La identificación debe tener entre 6 y 10 dígitos"
            )

        self.__identificacion = identificacion

    def set_nombre(self, nombre):

        # Elimina espacios al inicio y final
        nombre = nombre.strip()

        # Verifica que no esté vacío
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")

        # Verifica que solo contenga letras y espacios
        if not all(parte.isalpha() for parte in nombre.split()):
            raise ValueError("El nombre solo debe contener letras")

        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

# ============================================
# REQUERIMIENTO R3)
# CLASE RESERVA  (JFM)
# ============================================

class Reserva:
    
    # Se recupera el identificador único
    # para cada reserva. (JFM - JHAR)
    _contador = 0
    
    def __init__(self, cliente, servicio, inicio, fin):
        try:
            
            # Asigna un número a cada reserva. (JFM - JHAR)
            Reserva._contador += 1
            self.id = Reserva._contador
            self.cliente = cliente
            self.servicio = servicio

            # EGC - La validación de fechas actualmente se realiza directamente dentro de
            # la clase Reserva mediante objetos datetime y validaciones lógicas.
            self.inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d").date()
            self.fin = datetime.datetime.strptime(fin, "%Y-%m-%d").date()

            if self.fin <= self.inicio:
                raise ValueError("La fecha final debe ser mayor a la inicial")

            self.estado = "Activa"
            self.costo = self.calcular_dias()

            Logger.registrar(f"Reserva creada para {cliente.get_nombre()}")

        except Exception as e:
            Logger.registrar(f"Error en reserva: {e}")
            raise
    
    # Actualización: anteriormente método 'calcular'
    # ahora 'calcular_dias'. (JHAR)
    def calcular_dias(self):
        # Actualización: Cálculo correcto de días (JFM)
        dias = (self.fin - self.inicio).days + 1
        # Se almacena el valor de los días
        # en una variable de la clase para no perderlo.
        # Con esto se evita redundancia de cálculo
        # que anteriormente se presentaba al repetir
        # la fórmula (self.fin - self.inicio).days + 1
        # en duracion_dias, en el método ver_reserva de la
        # clase SistemaGUI. (JHAR)
        self.dias = dias
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
    # a) en la forma como inicializa la clase SistemaGUI y 
    # b) se actualiza las referencias de root a sel.root en todo el código. (JHAR)
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Software FJ")

        # ===== CONFIGURACIÓN DE VENTANA (JHAR - EGC) =====

        # Aporto funcionalidad al requerimiento R3, para mejorar la
        # la visualización de la ventana del programa. (JHAR)
        self.centrar_ventana(self.root, 1100, 710)
        self.root.configure(bg="#F4F6F9")
        # Permite redimensionar la ventana.
        self.root.resizable(True, True)

        # Aporto funcionalidad al requerimiento R3, para mejorar la visualización de la ventana del programa. (JHAR)
        # ===== CAMBIO INTERFAZ (EGC) =====
        # Paleta de colores general del sistema.
        self.color_fondo = "#F4F6F9"
        self.color_titulo = "#1D3557"
        self.color_boton = "#457B9D"
	
       # ===== PERSONALIZACIÓN VISUAL R6 (JHAR - EGC) =====

        # Se utiliza el tema visual "clam" para proporcionar una apariencia más moderna y uniforme
        # en los componentes ttk del sistema. (JHAR)
        # La configuración de estilos permite centralizar la personalización visual evitando repetir 
        # propiedades en cada componente gráfico. (EGC)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Titulo.TLabel",
            background="#1D3557",
            foreground="white",
            font=("Tahoma", 13, "bold"),
            padding=3
        )

        style.configure(
            "Seccion.TLabelframe",
            background="#F4F6F9",
            font=("Tahoma", 8, "bold")
        )

        style.configure(
            "Seccion.TLabelframe.Label",
            background="#F4F6F9",
            foreground="#1D3557",
            font=("Tahoma", 8, "bold")
        )

        style.configure(
            "TLabel",
            background="#F4F6F9",
            font=("Tahoma", 8)
        )

        style.configure(
            "TButton",
            font=("Tahoma", 8, "bold"),
            padding=4
        )
	
	# ===== CAMBIO INTERFAZ (EGC) =====
	# datos en memoria (sin base de datos) 
        self.clientes = []
        self.reservas = []
        self.servicios = {
            "Sala": ReservaSala(),
            "Equipos": AlquilerEquipos(),
            "Asesoria": AsesoriaEspecializada()
        }
        
  	# ============================================
        # CONTENEDOR PRINCIPAL
        # ===== REDISEÑO Y REORGANIZACIÓN UI (EGC) =====
        # ============================================

        # Se crea el contenedor principal encargado de almacenar y organizar visualmente todas
        # las secciones de la interfaz gráfica. (EGC)
        contenedor = tk.Frame(self.root, bg=self.color_fondo)
        contenedor.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=5)

          # ============================================
        # TITULO PRINCIPAL
        # ===== PERSONALIZACIÓN VISUAL R6 (JHAR) =====
        # ============================================

        # Etiqueta principal del sistema encargada de mostrar el nombre de la aplicación. 
        # (JHAR - EGC)
        titulo = ttk.Label(
            contenedor,
            text="Sistema Integral de Gestión de Reservas",
            style="Titulo.TLabel",
            anchor="center"
        )

        titulo.pack(fill="x", pady=(0, 8))

        # ============================================
        # FRAME CLIENTE
        # -------- REGISTRO CLIENTE (JFM) --------
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        # Se crea la sección correspondiente al registro de clientes dentro de la
        # interfaz gráfica del sistema. (JFM - EGC)
        frame_cliente = ttk.LabelFrame(
            contenedor,
            text="Datos del Cliente",
            style="Seccion.TLabelframe"
        )

        frame_cliente.pack(fill="x", pady=10)

        # "Se crea la etiqueta para mostrar donde se debe ingresar el número de identificación
        # del cliente: ttk.Label, al frente se crea el espacio donde se puede escribir el número:
        # ttk.Entry". (JFM)
        ttk.Label(
            frame_cliente,
            text="ID Cliente"
        ).grid(row=0, column=0, padx=10, pady=4)

        self.id_entry = ttk.Entry(
            frame_cliente,
            width=40
        )

        self.id_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        # "Botón para registrar los datos ingresados". (JFM)
        ttk.Button(
            frame_cliente,
            text="Registrar Cliente",
            command=self.registrar_cliente
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        # "Se crea la etiqueta para mostrar donde se debe ingresar el nombre del cliente:
        # ttk.Label. Al frente se crea el espacio donde se puede escribir el nombre:
        # ttk.Entry". (JFM)
        # (YTVCH)

        ttk.Label(
            frame_cliente,
            text="Nombre"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=3
        )

        self.nombre_entry = ttk.Entry(
            frame_cliente,
            width=40
        )

        self.nombre_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # ============================================
        # FRAME RESERVA
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        # Se crea la sección correspondiente a los datos relacionados con la creación y
        # gestión de reservas. (EGC)
        frame_reserva = ttk.LabelFrame(
            contenedor,
            text="Datos de la Reserva",
            style="Seccion.TLabelframe"
        )

        frame_reserva.pack(fill="x", pady=4)

        # -------- SELECCIÓN CLIENTE (JFM) --------

        # "Se crea la etiqueta para mostrar donde seleccionar el cliente: ttk.Label.
        # Al frente se crea el espacio donde queda la lista desplegable para seleccionar
        # los clientes registrados". (JFM)
        ttk.Label(
            frame_reserva,
            text="Seleccionar Cliente"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        self.cliente_var = tk.StringVar()

        # 🔧 ACTIVACIÓN R8 (IMPORTANTE)
        self.cliente_var.trace_add("write", self.validar_estado_seleccion) #Esto no estaba

        self.combo_clientes = ttk.Combobox(
            frame_reserva,
            textvariable=self.cliente_var,
            state="readonly",
            width=40
        )

        self.combo_clientes.grid(
            row=0,
            column=1,
            padx=10,
            pady=3
        )

        # -------- SECCIÓN DESCUENTOS (JFM) --------

        # Se crean las opciones de descuento aplicables a la reserva mediante botones de selección. 
        # (JFM - EGC) 
        self.descuento_var = tk.IntVar(value=0)

        frame_desc = tk.Frame(
            frame_reserva,
            bg=self.color_fondo
        )

        frame_desc.grid(
            row=0,
            column=2,
            padx=10
        )

        ttk.Label(
            frame_desc,
            text="Desc:"
        ).pack(side="left", padx=3)

        ttk.Radiobutton(
            frame_desc,
            text="5%",
            variable=self.descuento_var,
            value=5
        ).pack(side="left")

        ttk.Radiobutton(
            frame_desc,
            text="10%",
            variable=self.descuento_var,
            value=10
        ).pack(side="left")

        ttk.Radiobutton(
            frame_desc,
            text="15%",
            variable=self.descuento_var,
            value=15
        ).pack(side="left")

        # -------- SERVICIO (JFM) --------

        # "Se crea la etiqueta para mostrar donde seleccionar el servicio: ttk.Label.
        # Al frente se crea el espacio donde queda la lista desplegable para seleccionar
        # los servicios". (JFM)
        ttk.Label(
            frame_reserva,
            text="Servicio"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        self.servicio_var = tk.StringVar()

        self.combo_servicios = ttk.Combobox(
            frame_reserva,
            textvariable=self.servicio_var,
            values=list(self.servicios.keys()),
            state="readonly",
            width=40
        )

        self.combo_servicios.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # -------- FECHAS (JFM) --------

        # "Se crea la etiqueta para mostrar donde ingresar la fecha de inicio: ttk.Label.
        # Al frente se crea el espacio donde queda el campo para ingresar la fecha". (JFM)
        ttk.Label(
            frame_reserva,
            text="Inicio (YYYY-MM-DD)"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=5
        )

        self.inicio_entry = ttk.Entry(
            frame_reserva,
            width=40
        )

        self.inicio_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        # "Se crea la etiqueta para mostrar donde ingresar la fecha final: ttk.Label.
        # Al frente se crea el espacio donde queda el campo para ingresar la fecha". (JFM)

        ttk.Label(
            frame_reserva,
            text="Fin (YYYY-MM-DD)"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=5
        )

        self.fin_entry = ttk.Entry(
            frame_reserva,
            width=40
        )

        self.fin_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=10
        )

        # ===== BOTONES RESERVA (JFM) =====

        # Se crean los botones principales para crear reservas y limpiar los campos del formulario. (JFM - EGC)

        frame_acciones_reserva = tk.Frame(
            frame_reserva,
            bg=self.color_fondo
        )

        frame_acciones_reserva.grid(
            row=4,
            column=1,
            pady=10,
            sticky="w"
        )

        ttk.Button(
            frame_acciones_reserva,
            text="Crear Reserva",
            command=self.crear_reserva
        ).pack(side="left", padx=5)

        ttk.Button(
            frame_acciones_reserva,
            text="Limpiar",
            command=self.limpiar
        ).pack(side="left", padx=5)

        # Actualización: Las entradas de servicios y de fechas deben
        # permanecer deshabilitadas hasta que sea
        # seleccionado un cliente. (JHAR)
        self.combo_servicios.config(state="disabled")
        self.inicio_entry.config(state="disabled")
        self.fin_entry.config(state="disabled")

        # ============================================
        # AREA CENTRAL
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        frame_central = tk.Frame(
            contenedor,
            bg=self.color_fondo
        )

        # Actualización para distribuir elementos equitativamente
        # en pantalla. (JHAR)
        frame_central.columnconfigure(0, weight=1, uniform="columna_igual")
        frame_central.columnconfigure(1, weight=0)
        frame_central.columnconfigure(2, weight=1, uniform="columna_igual")
        
        frame_central.pack(
            fill="both",
            #expand=True,
            pady=5
        )

        # ===================================================
    	# REQUERIMIENTO R6
        # Se crea la sección según las necesidades del programa según las necesidades actuales. 
        # (JHAR)
    	# ============================================

        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # Contenedor visual que agrupa la lista de reservas creadas dentro del sistema. (JHAR)
        frame_reservas = ttk.LabelFrame(
            frame_central,
            text="Reservas Contratadas",
            style="Seccion.TLabelframe"
        )

        # Actualización del posicionamiento de reservas. (JHAR)
        frame_reservas.grid(
            row=0,
            column=0,
            sticky='nsew',
            padx=5
        )

        # -------- LISTA DE RESERVAS y CONTROLES (JFM - JHAR) --------
        self.lista = tk.Listbox(
            frame_reservas,
            font=("Consolas", 11),
            height=12,
            relief="solid",
        )

        self.lista.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5,0),
            pady=5
        )

        scrollbar = ttk.Scrollbar(
            frame_reservas,
            orient="vertical",
            command=self.lista.yview
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=5,
            padx=(0,5)
        )
        
        self.lista.config(
            yscrollcommand=scrollbar.set
        )

        # ============================================
        # BOTONES
        # -------- BOTONES (JFM) --------
        # ===== REORGANIZACIÓN VISUAL (EGC - JHAR) =====
        # ============================================

        # Se crean los botones encargados de visualizar y cancelar reservas. (JHAR - EGC)
        frame_botones = tk.Frame(
            frame_central,
            bg=self.color_fondo
        )

        # Actualización de posicionamiento del marco de los botones. (EGC - JHAR)
        frame_botones.grid(
            row=0,
            column=1,
            sticky='ns',
            padx=10,
            pady=12
        )

        # Actualización de pady para que mantenga las proporciones
        # de los demás elementos. (JHAR)
        ttk.Button(
            frame_botones,
            text="Ver Reserva",
            command=self.ver_reserva
        ).pack(fill="x", pady=5)

        # Se actualiza donde se muestra el botón cancelar reserva. (JFM - JHAR)
        ttk.Button(
            frame_botones,
            text="Cancelar Reserva",
            command=self.cancelar_reserva
        ).pack(fill="x", pady=5)

        # ============================================
        # VISTA DETALLE DE RESERVA
        # -------- SECCIÓN 5: VISTA PREVIA --------
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        # Se crea el área de vista previa donde se muestra la información detallada
        # de la reserva seleccionada. (JFM - EGC - JHAR)
        frame_detalle = ttk.LabelFrame(
            frame_central,
            text="Detalle de reserva",
            style="Seccion.TLabelframe"
        )

        # Actualización: para mantener las proporciones
        # de los demás elementos. (EGC - JHAR)
        frame_detalle.grid(
            row=0,
            column=2,
            sticky='nsew',
            padx=5
        )

        self.preview = tk.Text(
            frame_detalle,
            height=12,
            font=("Consolas", 11),
            relief="solid",
            borderwidth=1
        )

        self.preview.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )
        
        # ============================================
        # BOTONES INFERIORES
        # ===== PERSONALIZACIÓN VISUAL (EGC) =====
        # ============================================

        # Se crean los botones inferiores encargados de visualizar los logs
        # del sistema y cerrar la aplicación. (JFM - EGC)

        frame_inferior = tk.Frame(
            contenedor,
            bg=self.color_fondo
        )

        frame_inferior.pack(
            side=tk.TOP,
            fill="x",
            padx=10,
            pady=10,
            anchor='e'
        )

        boton_salir = tk.Button(
            frame_inferior,
            text="Salir",
            command=self.salir,
            bg="#C1121F",
            fg="white",
            font=("Tahoma", 8, "bold"),
            relief="flat",
            padx=12,
            pady=3
        )

        boton_salir.pack(
            side="right",
            padx=5
        )

        ttk.Button(
            frame_inferior,
            text="Ver Logs",
            command=self.mostrar_logs
        ).pack(
            side="right",
            padx=10
        )

        # ============================================
        # MAIN LOOP
        # ============================================

        self.root.mainloop()
         
       
    # =========================
    # FUNCIONES
    # =========================
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
    
    def registrar_cliente(self):
        try:
            cliente = Cliente(self.id_entry.get(), self.nombre_entry.get())
            self.clientes.append(cliente)

            # ===== CAMBIO INTERFAZ (EGC) =====
            self.combo_clientes["values"] = [c.get_nombre() for c in self.clientes]
            messagebox.showinfo("OK", "Cliente registrado")

        except Exception as e:
            Logger.registrar(str(e))
            messagebox.showerror("Error", str(e))
        
        # Actualización: se trasladan estas líneas del
        # método limpiar, ya que es más fácil realizar
        # limpieza de los datos de un nuevo cliente al
        # momento de registrarlo. (JHAR) 
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)

    def obtener_cliente(self):
        nombre = self.cliente_var.get()
        for c in self.clientes:
            if c.get_nombre() == nombre:
                return c
        raise ValueError("Debe seleccionar un cliente")
 
    def crear_reserva(self):
        # Conexión con requerimiento R9 (YTVCH)
        if not self.verificar_seleccion_servicio():
            return
            
        try:
            cliente = self.obtener_cliente()
            servicio = self.servicios[self.servicio_var.get()]

            reserva = Reserva(
                cliente,
                servicio,
                self.inicio_entry.get(),
                self.fin_entry.get()
            )
	        # Se activa la función encargada de obtener el descuento seleccionado
            # para aplicarlo al costo total de la reserva. (EGC)
            descuento = self.obtener_descuento()

            if descuento > 0:
              reserva.costo = reserva.costo - (reserva.costo * descuento / 100)

            # Se almacena la reserva creada dentro de la lista general de reservas del sistema. (JFM - EGC)
            self.reservas.append(reserva)

            # Se inserta en pantalla el resumen de la reserva creada dentro del listado de reservas contratadas. 
            # (JFM) 
            self.lista.insert(tk.END,
                f"{cliente.get_nombre()} - {servicio.nombre} - ${reserva.costo} - {reserva.estado}"
            )

            messagebox.showinfo("OK", "Reserva creada")

        except Exception as e:
            Logger.registrar(str(e))
            messagebox.showerror("Error", str(e))
    
    # Función encargada de retornar el porcentaje de descuento seleccionado por el usuario. (EGC)
    def obtener_descuento(self):
       
        # Retorna directamente el valor seleccionado en los Radiobuttons de descuento. (EGC)
        return self.descuento_var.get()
    
    # Función para ver detalle completo de la reserva. (JHAR - JJBT)
    def ver_reserva(self):
        self.preview.delete("1.0", tk.END)
        seleccion = self.lista.curselection()
        
        # Busca por índice seleccionado en la lista — así siempre coincide. (JJBT)
        # ===================================================
    	# REQUERIMIENTO R11
        # Mensaje de error al no selecciar una reserva para
        # # visualizar el detalle. 
        # (JHAR)
    	# ============================================
        if not seleccion:
            mensaje_seleccion = "No se ha seleccionado una reserva de la lista."
            Logger.registrar(f"ERROR: {mensaje_seleccion}")
            messagebox.showerror("Error de Selección", mensaje_seleccion)
            return

        i = seleccion[0]
        descuento=self.obtener_descuento()
        reserva_encontrada=self.reservas[i]
        # Son eliminadas varias líneas de cáclculos redundantes
        # que ya se hacían en la clase reserva, como costo, costo
        # con descuento y el cálculo de días. (JHAR)
        # Se usa textwrap para mejorar la presentación y con esto se corrige la identación. (JHAR)
        texto = textwrap.dedent(f"""
                ID Reserva: #{reserva_encontrada.id}
                Cliente: {self.cliente_var.get()}
                Servicio: {self.servicio_var.get()}
                Inicio: {self.inicio_entry.get()}
                Fin: {self.fin_entry.get()}
                Descuento: {self.obtener_descuento()}%
                Duración: {reserva_encontrada.dias} día(s)
                Costo: ${reserva_encontrada.costo:.2f}
                Estado: {reserva_encontrada.estado}
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

    # ============================================
    # FUNCIÓN LIMPIAR
    # ============================================

    # Función encargada de limpiar todos los campos del formulario y reiniciar la interfaz gráfica. 
    # (JFM - EGC)
    def limpiar(self):
        self.inicio_entry.delete(0, tk.END)
        self.fin_entry.delete(0, tk.END)
        # Recuperación: de la línea que regresa al valor
        # por defecto de self.cliente_var, borrada en una
        # actualziación. (JHAR)
        self.cliente_var.set("")
        self.servicio_var.set("")
        self.descuento_var.set(0) # Reinicia descuento seleccionado. (EGC)
        self.preview.delete("1.0", tk.END)

    # ============================================
    # INICIO REQUERIMIENTO R8 (YTVCH)
    # Habilitar selección de servicio tras elegir cliente.
    # ============================================
    def validar_estado_seleccion(self, *args):
        """
        Si el usuario no ha seleccionado un cliente para la reserva no se habilita
        la selección de servicios y las entradas de la duración (YTVCH)
        """
        cliente_seleccionado = self.cliente_var.get()

        # Validación para habilitar widgets solo si hay un cliente válido (YTVCH)
        if cliente_seleccionado != "" and cliente_seleccionado != "No hay clientes":
            self.combo_servicios.config(state="readonly") #Antes self.menu_servicios.config(state="normal")
            self.inicio_entry.config(state="normal")
            self.fin_entry.config(state="normal")
        else:
            # Mantener deshabilitado si no hay selección previa (YTVCH)
            self.combo_servicios.config(state="disabled") #Antes self.menu_servicios.config(state="disabled")
            self.inicio_entry.config(state="disabled")
            self.fin_entry.config(state="disabled")
    # FIN REQUERIMIENTO R8 (YTVCH)

    # ============================================
    # INICIO REQUERIMIENTO R9 (YTVCH)
    # Verificar selección de servicio antes de registrar reserva.
    # ============================================
    def verificar_seleccion_servicio(self):
        """
        Verifica que el servicio seleccionado exista en self.servicios (YTVCH)
        """
        try:
            seleccion = self.servicio_var.get()
            # Se conecta con self.servicios para validar la opción elegida (YTVCH)
            # Actualización: se corrige la validación del servicio seleccionado. (JHAR)
            if seleccion == "" or seleccion not in self.servicios:
                raise ServicioNoSeleccionadoError("Debe seleccionar un servicio válido de la lista")
            return True 

        except ServicioNoSeleccionadoError as e:
            messagebox.showwarning("Información de Selección", str(e))
            Logger.registrar(f"R9 - Intento fallido: {e}")
            return False
    # FIN REQUERIMIENTO R9 (YTVCH)

    # ============================================
    # MOSTRAR LOGS DEL SISTEMA
    # ============================================

    # Función encargada de visualizar los registros de eventos y errores
    # almacenados en el archivo logs.txt.
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
        ventana.geometry("700x500")
    
        texto = tk.Text(ventana, wrap="word", state="normal", font=("Consolas", 10))
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