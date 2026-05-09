# Grupo_129.
# Fase 4: Sistema Integral de Gestión de Clientes, Servicios y Reservas.
# Ingeniería de Sistemas.
# Autoría propia.
print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")


# ============================================
# IMPORTACIONES (EGC)
# ============================================

# Se importa ABC y abstractmethod para crear clases abstractas
# y métodos obligatorios que deberán implementar las clases hijas.
# Se importa datetime para trabajar con fechas y horas,
# especialmente para registrar eventos y errores en los logs.
# Se importa tkinter para crear la interfaz gráfica del sistema.
# Se importa messagebox para mostrar mensajes emergentes
# de advertencia, error o confirmación al usuario.
# Importación para estilos personalizados y componentes mejorados.
# Se importa os para posibles operaciones relacionadas
# con archivos y rutas del sistema.

from abc import ABC, abstractmethod
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import textwrap
import os

# ============================================
# LOGS DEL SISTEMA (EGC)
# ============================================

# Clase encargada de registrar eventos y errores del sistema
# dentro de un archivo de texto llamado logs.txt.
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
    """Error base para operaciones de reserva."""

# INICIO REQUERIMIENTO R9 (YTVCH)
class ServicioNoSeleccionadoError(ReservaError):
    """Error lanzado cuando el servicio está vacío en el R2 (YTVCH)"""
    pass
# FIN REQUERIMIENTO R9 (YTVCH)

# ============================================
# CLASE ABSTRACTA SERVICIO (EGC)
# ============================================

# Clase abstracta que representa los servicios generales
# ofrecidos por el sistema. Las clases hijas deberán implementar el método calcular_costo
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

#Clase Cliente encargada de almacenar y validar
# la información personal del cliente.
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

# Método encargado de validar que la identificación
# contenga únicamente valores numéricos. Si la validación falla, se lanza una excepción personalizada.
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

        # ===== CAMBIO INTERFAZ (EGC) =====
        # Permite redimensionar la ventana.
        self.root.geometry("1100x760")
        self.root.state("zoomed")
        self.root.configure(bg="#F4F6F9")
        self.root.resizable(True, True)

        # ===== CAMBIO INTERFAZ (EGC) =====
        # Paleta de colores general del sistema.
        self.color_fondo = "#F4F6F9"
        self.color_titulo = "#1D3557"
        self.color_boton = "#457B9D"
	
        # ===== CAMBIO INTERFAZ (EGC) =====
        # Se utiliza el tema "clam" para una apariencia más moderna
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

        # Se crea el contenedor principal encargado
        # de almacenar y organizar visualmente todas
        # las secciones de la interfaz gráfica. (EGC)

        contenedor = tk.Frame(self.root, bg=self.color_fondo)
        contenedor.pack(fill="x",padx=15,pady=2,side="bottom")

          # ============================================
        # TITULO PRINCIPAL
        # ===== PERSONALIZACIÓN VISUAL R6 (JHAR) =====
        # ============================================

        # Etiqueta principal del sistema encargada
        # de mostrar el nombre de la aplicación. (JHAR - EGC)

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

        # Se crea la sección correspondiente al
        # registro de clientes dentro de la
        # interfaz gráfica del sistema. (JFM - EGC)

        frame_cliente = ttk.LabelFrame(
            contenedor,
            text="Datos del Cliente",
            style="Seccion.TLabelframe"
        )

        frame_cliente.pack(fill="x", pady=10)

        # "Se crea la etiqueta para mostrar donde
        # se debe ingresar el número de identificación
        # del cliente: ttk.Label, al frente se crea
        # el espacio donde se puede escribir el número:
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

        # "Se crea la etiqueta para mostrar donde
        # se debe ingresar el nombre del cliente:
        # ttk.Label. Al frente se crea el espacio
        # donde se puede escribir el nombre:
        # ttk.Entry". (JFM)

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

        # Se crea la sección correspondiente a los
        # datos relacionados con la creación y
        # gestión de reservas. (EGC)

        frame_reserva = ttk.LabelFrame(
            contenedor,
            text="Datos de la Reserva",
            style="Seccion.TLabelframe"
        )

        frame_reserva.pack(fill="x", pady=4)

        # -------- SELECCIÓN CLIENTE (JFM) --------

        # "Se crea la etiqueta para mostrar donde
        # seleccionar el cliente: ttk.Label.
        # Al frente se crea el espacio donde queda
        # la lista desplegable para seleccionar
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

        # -------- SECCIÓN DESCUENTOS (EGC) --------

        # Se crea la sección correspondiente a los
        # descuentos aplicables a la reserva. (EGC)

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

        # "Se crea la etiqueta para mostrar donde
        # seleccionar el servicio: ttk.Label.
        # Al frente se crea el espacio donde queda
        # la lista desplegable para seleccionar
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

        # "Se crea la etiqueta para mostrar donde
        # ingresar la fecha de inicio: ttk.Label.
        # Al frente se crea el espacio donde queda
        # el campo para ingresar la fecha". (JFM)

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

        # "Se crea la etiqueta para mostrar donde
        # ingresar la fecha final: ttk.Label.
        # Al frente se crea el espacio donde queda
        # el campo para ingresar la fecha". (JFM)

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

        # ============================================
        # AREA CENTRAL
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        frame_central = tk.Frame(
            contenedor,
            bg=self.color_fondo
        )

        frame_central.pack(
            fill="both",
            pady=5
        )

        # ============================================
        # VISTA PREVIA
        # -------- SECCIÓN 5: VISTA PREVIA --------
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        frame_preview = ttk.LabelFrame(
            frame_central,
            text="Vista Previa",
            style="Seccion.TLabelframe"
        )

        frame_preview.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.preview = tk.Text(
            frame_preview,
            height=1,
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
        # BOTONES
        # -------- BOTONES (JFM) --------
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        frame_botones = ttk.LabelFrame(
            frame_central,
            text="Acciones",
            style="Seccion.TLabelframe"
        )

        frame_botones.pack(
            side="right",
            fill="y"
        )

        ttk.Button(
            frame_botones,
            text="Crear Reserva",
            command=self.crear_reserva
        ).pack(fill="x", padx=8, pady=2)

        ttk.Button(
            frame_botones,
            text="Ver Reserva",
            command=self.ver_reserva
        ).pack(fill="x", padx=8, pady=1)

        ttk.Button(
            frame_botones,
            text="Limpiar",
            command=self.limpiar
        ).pack(fill="x", padx=8, pady=1)

        ttk.Button(
            frame_botones,
            text="Ver Logs",
            command=self.mostrar_logs
        ).pack(fill="x", padx=8, pady=1)

        ttk.Button(
            frame_botones,
            text="Cancelar Reserva",
            command=self.cancelar_reserva
        ).pack(fill="x", padx=8, pady=1)

	# ===================================================
    	# REQUERIMIENTO R6
    	# Diseñar sección de visualización de reservas
    	# Se crea la sección según las necesidades del
    	# programa según las necesidades actuales. (JHAR)
        # ===== REORGANIZACIÓN VISUAL (EGC) =====
        # ============================================

        frame_reservas = ttk.LabelFrame(
            contenedor,
            text="Reservas Contratadas",
            style="Seccion.TLabelframe"
        )

        frame_reservas.pack(
            fill="both",
            expand=False,
            pady=4
        )

        self.lista = tk.Listbox(
            frame_reservas,
            font=("Consolas", 11),
            height=4,
            relief="solid",
            borderwidth=1
        )

        self.lista.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        scrollbar = ttk.Scrollbar(
            frame_reservas,
            orient="vertical",
            command=self.lista.yview
        )

        self.lista.config(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=5
        )

        # ============================================
        # BOTÓN SALIR
        # ===== PERSONALIZACIÓN VISUAL (EGC) =====
        # ============================================

        # Botón encargado de cerrar el sistema
        # y finalizar la ejecución del programa. (EGC)

        boton_salir = tk.Button(
            contenedor,
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
            anchor="e",
            pady=2,
            padx=5
        )

        # ============================================
        # MAIN LOOP
        # ============================================

        self.root.mainloop()
         
       
    # =========================
    # FUNCIONES
    # =========================
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
	    #Se activa la funcion de descuentos 
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
       
        # Retorna directamente el valor seleccionado
        # en los Radiobuttons de descuento. (EGC)

        return self.descuento_var.get()
    
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

    # EGC
    #la validación realmente la está haciendo la clase Reserva. 	
    '''def validar_fechas(self):
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
            raise ValueError("Error en fechas: " + str(e))'''


    # Limpia todos los campos
    def limpiar(self):

        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.servicio_var.set("")
        self.inicio_entry.delete(0, tk.END)
        self.fin_entry.delete(0, tk.END)
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
            self.menu_servicios.config(state="normal")
            self.inicio_entry.config(state="normal")
            self.fin_entry.config(state="normal")
        else:
            # Mantener deshabilitado si no hay selección previa (YTVCH)
            self.menu_servicios.config(state="disabled")
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
            if seleccion == "Escoge un servicio" or seleccion == "" or self.servicios[seleccion] is None:
                raise ServicioNoSeleccionadoError("Debe seleccionar un servicio de la lista")
            return True 

        except ServicioNoSeleccionadoError as e:
            messagebox.showwarning("Información de Selección", str(e))
            Logger.registrar(f"R9 - Intento fallido: {e}")
            return False
    # FIN REQUERIMIENTO R9 (YTVCH)

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
