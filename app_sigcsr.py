# Grupo_129.
# Fase 4: Sistema Integral de Gestión de Clientes, Servicios y Reservas.
# Ingeniería de Sistemas.
# Autoría propia.
print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")

from abc import ABC, abstractmethod
import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================
# REQUERIMIENTO R5
# sección de registro de reservas
# ============================================
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
    
class ReservasFrame(Reserva,tk.Frame):
    """
    Frame completo de registro de reservas.
 
    Parámetros
    ----------
    parent : tk.Widget
        Contenedor padre (ventana o notebook).
    clientes : list
        Lista de objetos Cliente. Deben tener __str__ definido.
    servicios : list
        Lista de objetos Servicio. Deben tener __str__ definido.
    on_registrar : callable, opcional
        Callback con firma on_registrar(datos: dict) -> None.
        Si no se pasa, el frame gestiona la reserva internamente
        (modo demo).
    logger : logging.Logger, opcional
        Logger del proyecto grupal. Si no se pasa se crea uno local.
    clase_reserva : class, opcional
        Clase Reserva del proyecto grupal.  Si no se pasa se usa
        la clase ReservaDummy incluida abajo (modo demo).
    """
 
    MESES = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    DIAS = [str(d) for d in range(1, 32)]
 
    def __init__(
        self,
        parent,
        clientes: list = None,
        servicios: list = None,
        on_registrar=None,
        logger=None,
        clase_reserva=None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.clientes = clientes or []
        self.servicios = servicios or []
        self._on_registrar_externo = on_registrar
        self.logger = logger or logger()
        self._clase_reserva = clase_reserva or Reservaconfi
 
        self._log("INFO", "ReservasFrame inicializado correctamente.")
        self._construir_ui()
 
    # ── HELPERS DE LOG ──────────────────────────────────────
    def _log(self, nivel: str, mensaje: str):
        nivel = nivel.upper()
        metodo = getattr(self.logger, nivel.lower(), self.logger.info)
        metodo(mensaje)
        # Refleja el log en el widget de logs si ya existe
        if hasattr(self, "txt_logs"):
            self._refrescar_logs()
 
    # ── CONSTRUCCIÓN DE LA INTERFAZ ─────────────────────────
    def _construir_ui(self):
        self.configure(bg="#1e2a38", padx=16, pady=16)
 
        # ── Título ──
        tk.Label(
            self,
            text="📋  Registro de Reservas — Software FJ",
            font=("Courier New", 15, "bold"),
            bg="#1e2a38", fg="#00d4ff",
        ).grid(row=0, column=0, columnspan=4, pady=(0, 14), sticky="w")
 
        # ── Sección formulario ──
        frame_form = tk.LabelFrame(
            self, text=" Datos de la Reserva ",
            font=("Courier New", 10, "bold"),
            bg="#1e2a38", fg="#a0b4c8",
            bd=2, relief="groove", padx=12, pady=10,
        )
        frame_form.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        self._build_form(frame_form)
 
        # ── Sección preview ──
        frame_prev = tk.LabelFrame(
            self, text=" Vista previa de la Reserva ",
            font=("Courier New", 10, "bold"),
            bg="#1e2a38", fg="#a0b4c8",
            bd=2, relief="groove", padx=12, pady=10,
        )
        frame_prev.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        self._build_preview(frame_prev)
 
        # ── Sección descuentos ──
        frame_desc = tk.LabelFrame(
            self, text=" Descuentos ",
            font=("Courier New", 10, "bold"),
            bg="#1e2a38", fg="#a0b4c8",
            bd=2, relief="groove", padx=12, pady=10,
        )
        frame_desc.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        self._build_descuentos(frame_desc)
 
        # ── Botones ──
        frame_btn = tk.Frame(self, bg="#1e2a38")
        frame_btn.grid(row=4, column=0, columnspan=4, pady=(4, 10))
        self._build_botones(frame_btn)
 
        # ── Logs ──
        frame_logs = tk.LabelFrame(
            self, text=" 🛠  Registro de Eventos y Errores del Sistema ",
            font=("Courier New", 10, "bold"),
            bg="#1e2a38", fg="#a0b4c8",
            bd=2, relief="groove", padx=12, pady=10,
        )
        frame_logs.grid(row=5, column=0, columnspan=4, sticky="nsew", pady=(0, 4))
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self._build_logs(frame_logs)
 
        # Actualizar preview al cambiar cualquier combobox
        for var in [
            self._var_cliente, self._var_servicio,
            self._var_mes_ini, self._var_dia_ini,
            self._var_mes_fin, self._var_dia_fin,
        ]:
            var.trace_add("write", lambda *_: self._actualizar_preview())
 
    def _build_form(self, parent):
        lbl_cfg = dict(bg="#1e2a38", fg="#c8d8e8", font=("Courier New", 10))
        cmb_cfg = dict(state="readonly", width=22, font=("Courier New", 10))
 
        # Cliente
        tk.Label(parent, text="Cliente:", **lbl_cfg).grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        self._var_cliente = tk.StringVar()
        self._cmb_cliente = ttk.Combobox(
            parent, textvariable=self._var_cliente, **cmb_cfg)
        self._cmb_cliente["values"] = [str(c) for c in self.clientes]
        self._cmb_cliente.grid(row=0, column=1, sticky="w", pady=4)
 
        # Servicio
        tk.Label(parent, text="Tipo de Servicio:", **lbl_cfg).grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        self._var_servicio = tk.StringVar()
        self._cmb_servicio = ttk.Combobox(
            parent, textvariable=self._var_servicio, **cmb_cfg)
        self._cmb_servicio["values"] = [str(s) for s in self.servicios]
        self._cmb_servicio.grid(row=1, column=1, sticky="w", pady=4)
 
        # Fechas — inicio
        tk.Label(parent, text="Fecha Inicio:", **lbl_cfg).grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=4)
        frame_ini = tk.Frame(parent, bg="#1e2a38")
        frame_ini.grid(row=2, column=1, sticky="w")
        self._var_mes_ini = tk.StringVar()
        self._var_dia_ini = tk.StringVar()
        ttk.Combobox(frame_ini, textvariable=self._var_mes_ini,
                     values=self.MESES, width=12,
                     state="readonly", font=("Courier New", 10)
                     ).pack(side="left", padx=(0, 6))
        ttk.Combobox(frame_ini, textvariable=self._var_dia_ini,
                     values=self.DIAS, width=5,
                     state="readonly", font=("Courier New", 10)
                     ).pack(side="left")
 
        # Fechas — fin
        tk.Label(parent, text="Fecha Fin:", **lbl_cfg).grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=4)
        frame_fin = tk.Frame(parent, bg="#1e2a38")
        frame_fin.grid(row=3, column=1, sticky="w")
        self._var_mes_fin = tk.StringVar()
        self._var_dia_fin = tk.StringVar()
        ttk.Combobox(frame_fin, textvariable=self._var_mes_fin,
                     values=self.MESES, width=12,
                     state="readonly", font=("Courier New", 10)
                     ).pack(side="left", padx=(0, 6))
        ttk.Combobox(frame_fin, textvariable=self._var_dia_fin,
                     values=self.DIAS, width=5,
                     state="readonly", font=("Courier New", 10)
                     ).pack(side="left")
 
    def _build_preview(self, parent):
        self._txt_preview = tk.Text(
            parent, height=6, width=70,
            bg="#0d1520", fg="#7effa0",
            font=("Courier New", 10),
            relief="flat", state="disabled",
            insertbackground="white",
        )
        self._txt_preview.pack(fill="both", expand=True)
 
    def _build_descuentos(self, parent):
        lbl_cfg = dict(bg="#1e2a38", fg="#c8d8e8", font=("Courier New", 10))
 
        # ¿Aplica descuento?
        tk.Label(parent, text="¿Aplica descuento?", **lbl_cfg).grid(
            row=0, column=0, sticky="w", padx=(0, 12))
        self._var_aplica_si = tk.BooleanVar(value=False)
        self._var_aplica_no = tk.BooleanVar(value=True)
 
        tk.Checkbutton(
            parent, text="Sí", variable=self._var_aplica_si,
            command=self._toggle_descuento_si,
            bg="#1e2a38", fg="#00d4ff",
            selectcolor="#0d1520", activebackground="#1e2a38",
            font=("Courier New", 10),
        ).grid(row=0, column=1, sticky="w")
 
        tk.Checkbutton(
            parent, text="No", variable=self._var_aplica_no,
            command=self._toggle_descuento_no,
            bg="#1e2a38", fg="#ff6b6b",
            selectcolor="#0d1520", activebackground="#1e2a38",
            font=("Courier New", 10),
        ).grid(row=0, column=2, sticky="w", padx=(0, 20))
 
        # Porcentaje
        tk.Label(parent, text="Porcentaje:", **lbl_cfg).grid(
            row=0, column=3, sticky="w", padx=(0, 8))
        self._var_desc_5 = tk.BooleanVar()
        self._var_desc_10 = tk.BooleanVar()
        self._var_desc_15 = tk.BooleanVar()
 
        self._chk5 = tk.Checkbutton(
            parent, text="5 %", variable=self._var_desc_5,
            command=lambda: self._elegir_porcentaje(5),
            bg="#1e2a38", fg="#ffd700",
            selectcolor="#0d1520", activebackground="#1e2a38",
            font=("Courier New", 10), state="disabled",
        )
        self._chk5.grid(row=0, column=4, sticky="w")
 
        self._chk10 = tk.Checkbutton(
            parent, text="10 %", variable=self._var_desc_10,
            command=lambda: self._elegir_porcentaje(10),
            bg="#1e2a38", fg="#ffd700",
            selectcolor="#0d1520", activebackground="#1e2a38",
            font=("Courier New", 10), state="disabled",
        )
        self._chk10.grid(row=0, column=5, sticky="w")
 
        self._chk15 = tk.Checkbutton(
            parent, text="15 %", variable=self._var_desc_15,
            command=lambda: self._elegir_porcentaje(15),
            bg="#1e2a38", fg="#ffd700",
            selectcolor="#0d1520", activebackground="#1e2a38",
            font=("Courier New", 10), state="disabled",
        )
        self._chk15.grid(row=0, column=6, sticky="w")
 
        self._porcentaje_activo = 0
 
    def _toggle_descuento_si(self):
        if self._var_aplica_si.get():
            self._var_aplica_no.set(False)
            for chk in (self._chk5, self._chk10, self._chk15):
                chk.configure(state="normal")
        else:
            self._limpiar_porcentajes()
        self._actualizar_preview()
 
    def _toggle_descuento_no(self):
        if self._var_aplica_no.get():
            self._var_aplica_si.set(False)
            self._limpiar_porcentajes()
            for chk in (self._chk5, self._chk10, self._chk15):
                chk.configure(state="disabled")
        self._actualizar_preview()
 
    def _elegir_porcentaje(self, pct: int):
        """Solo un porcentaje activo a la vez."""
        self._porcentaje_activo = pct if getattr(
            {5: self._var_desc_5,
             10: self._var_desc_10,
             15: self._var_desc_15}[pct], "get")() else 0
        mapa = {5: self._var_desc_5, 10: self._var_desc_10, 15: self._var_desc_15}
        for p, var in mapa.items():
            if p != pct:
                var.set(False)
        self._actualizar_preview()
 
    def _limpiar_porcentajes(self):
        self._var_desc_5.set(False)
        self._var_desc_10.set(False)
        self._var_desc_15.set(False)
        self._porcentaje_activo = 0
 
    def _build_botones(self, parent):
        btn_cfg = dict(font=("Courier New", 11, "bold"),
                       relief="flat", padx=18, pady=8, cursor="hand2")
        tk.Button(
            parent, text="✔  Registrar Reserva",
            bg="#00a86b", fg="white",
            command=self._registrar,
            **btn_cfg,
        ).pack(side="left", padx=(0, 12))
 
        tk.Button(
            parent, text="✖  Limpiar Formulario",
            bg="#c0392b", fg="white",
            command=self._limpiar,
            **btn_cfg,
        ).pack(side="left", padx=(0, 12))
 
        tk.Button(
            parent, text="🔄  Actualizar Logs",
            bg="#2980b9", fg="white",
            command=self._refrescar_logs,
            **btn_cfg,
        ).pack(side="left")
 
    def _build_logs(self, parent):
        self.txt_logs = tk.Text(
            parent, height=10, width=80,
            bg="#0d1520", fg="#ff9999",
            font=("Courier New", 9),
            relief="flat", state="disabled",
        )
        scroll = ttk.Scrollbar(parent, command=self.txt_logs.yview)
        self.txt_logs.configure(yscrollcommand=scroll.set)
        self.txt_logs.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._refrescar_logs()
 
    # ── LÓGICA ──────────────────────────────────────────────
    def _fecha_desde_vars(self, var_mes, var_dia) -> datetime.date:
        mes_str = var_mes.get()
        dia_str = var_dia.get()
        if not mes_str or not dia_str:
            raise FechaInvalidaError("Debe seleccionar mes y día completos.")
        mes = self.MESES.index(mes_str) + 1
        dia = int(dia_str)
        anio = datetime.date.today().year
        try:
            return datetime.date(anio, mes, dia)
        except ValueError as e:
            raise FechaInvalidaError(
                f"La fecha {dia}/{mes}/{anio} no es válida."
            ) from e
 
    def _obtener_descuento(self) -> float:
        if not self._var_aplica_si.get():
            return 0.0
        return self._porcentaje_activo / 100.0
 
    def _validar_campos(self):
        """Lanza excepciones personalizadas si falta algo."""
        if not self._var_cliente.get():
            raise ClienteNoSeleccionadoError("No se ha seleccionado un cliente.")
        if not self._var_servicio.get():
            raise ServicioNoSeleccionadoError("No se ha seleccionado un servicio.")
        fecha_ini = self._fecha_desde_vars(self._var_mes_ini, self._var_dia_ini)
        fecha_fin = self._fecha_desde_vars(self._var_mes_fin, self._var_dia_fin)
        if fecha_fin <= fecha_ini:
            raise FechaInvalidaError(
                f"La fecha de fin ({fecha_fin}) debe ser posterior "
                f"a la fecha de inicio ({fecha_ini})."
            )
        if self._var_aplica_si.get() and self._porcentaje_activo == 0:
            raise DescuentoInvalidoError(
                "Se marcó 'Sí' a descuento pero no se eligió porcentaje."
            )
        return fecha_ini, fecha_fin
 
    def _registrar(self):
        try:
            fecha_ini, fecha_fin = self._validar_campos()
 
            idx_cliente = [str(c) for c in self.clientes].index(
                self._var_cliente.get())
            idx_servicio = [str(s) for s in self.servicios].index(
                self._var_servicio.get())
            cliente_obj = self.clientes[idx_cliente]
            servicio_obj = self.servicios[idx_servicio]
            descuento = self._obtener_descuento()
 
            datos = {
                "cliente": cliente_obj,
                "servicio": servicio_obj,
                "fecha_inicio": fecha_ini,
                "fecha_fin": fecha_fin,
                "descuento": descuento,
            }
 
            if self._on_registrar_externo:
                # ── Modo integración: el controlador del grupo hace el trabajo
                self._on_registrar_externo(datos)
            else:
                # ── Modo demo: instanciar ReservaDummy internamente
                reserva = self._clase_reserva(**datos)
                reserva.confirmar()
                self._log(
                    "INFO",
                    f"Reserva registrada: {reserva}"
                )
                messagebox.showinfo(
                    "Reserva Exitosa",
                    f"Reserva registrada correctamente.\n\n{reserva}"
                )
 
        except (ClienteNoSeleccionadoError,
                ServicioNoSeleccionadoError,
                FechaInvalidaError,
                DescuentoInvalidoError) as e:
            self._log("WARNING", f"Validación fallida: {e}")
            messagebox.showwarning("Campo inválido", str(e))
 
        except Exception as e:
            self._log("ERROR", f"Error inesperado al registrar reserva: {e}")
            messagebox.showerror(
                "Error del sistema",
                f"Ocurrió un error inesperado:\n{e}"
            )
 
        finally:
            self._refrescar_logs()
 
    def _limpiar(self):
        try:
            self._var_cliente.set("")
            self._var_servicio.set("")
            self._var_mes_ini.set("")
            self._var_dia_ini.set("")
            self._var_mes_fin.set("")
            self._var_dia_fin.set("")
            self._var_aplica_si.set(False)
            self._var_aplica_no.set(True)
            self._limpiar_porcentajes()
            for chk in (self._chk5, self._chk10, self._chk15):
                chk.configure(state="disabled")
            self._actualizar_preview()
            self._log("INFO", "Formulario de reserva limpiado.")
        except Exception as e:
            self._log("ERROR", f"Error al limpiar formulario: {e}")
 
    def _actualizar_preview(self):
        try:
            cliente = self._var_cliente.get() or "—"
            servicio = self._var_servicio.get() or "—"
            m_ini = self._var_mes_ini.get() or "—"
            d_ini = self._var_dia_ini.get() or "—"
            m_fin = self._var_mes_fin.get() or "—"
            d_fin = self._var_dia_fin.get() or "—"
            aplica = "Sí" if self._var_aplica_si.get() else "No"
            pct = f"{self._porcentaje_activo} %" if self._porcentaje_activo else "—"
 
            texto = (
                f"  Cliente       : {cliente}\n"
                f"  Servicio      : {servicio}\n"
                f"  Fecha inicio  : {d_ini} de {m_ini}\n"
                f"  Fecha fin     : {d_fin} de {m_fin}\n"
                f"  Descuento     : {aplica}  →  {pct}\n"
            )
            self._txt_preview.configure(state="normal")
            self._txt_preview.delete("1.0", "end")
            self._txt_preview.insert("end", texto)
            self._txt_preview.configure(state="disabled")
        except Exception as e:
            self._log("ERROR", f"Error actualizando preview: {e}")
 
    def _refrescar_logs(self):
        """Lee el archivo de log y lo muestra en el widget."""
        try:
            ruta = "logs_sistema.log"
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
            else:
                contenido = ""
 
            self.txt_logs.configure(state="normal")
            self.txt_logs.delete("1.0", "end")
 
            if contenido:
                self.txt_logs.insert("end", contenido)
            else:
                self.txt_logs.insert(
                    "end",
                    "✔  El sistema se ha ejecutado sin errores hasta el momento."
                )
            self.txt_logs.configure(state="disabled")
            self.txt_logs.see("end")
        except Exception as e:
            # No podemos loggear dentro del logger, evitamos recursión
            print(f"[LOGS WIDGET] Error al refrescar logs: {e}")
 
    def actualizar_clientes(self, clientes: list):
        """Permite que el controlador del grupo recargue la lista de clientes."""
        self.clientes = clientes
        self._cmb_cliente["values"] = [str(c) for c in self.clientes]
 
    def actualizar_servicios(self, servicios: list):
        """Permite que el controlador del grupo recargue la lista de servicios."""
        self.servicios = servicios
        self._cmb_servicio["values"] = [str(s) for s in self.servicios]        

# =========================================================
# Requerimiento 12 Logs
# =========================================================
def _construir_tab_logs(self):
        f = self.tab_logs
        tk.Label(f, text="Registro de Eventos y Errores del Sistema",
                 font=("Arial", 13, "bold"), bg="#f0f4f8").pack(pady=(12, 6))
 
        frame_txt = tk.Frame(f, bg="#f0f4f8")
        frame_txt.pack(fill="both", expand=True, padx=10, pady=4)
 
        self.txt_logs = tk.Text(
            frame_txt, height=20, width=80,
            bg="#1e1e1e", fg="#dcdcdc",
            font=("Courier New", 9),
            relief="flat", state="disabled"
        )
        scroll_logs = tk.Scrollbar(frame_txt, command=self.txt_logs.yview)
        self.txt_logs.configure(yscrollcommand=scroll_logs.set)
        self.txt_logs.pack(side="left", fill="both", expand=True)
        scroll_logs.pack(side="right", fill="y")
 
        tk.Button(
            f, text="🔄  Actualizar Logs",
            command=self._refrescar_logs,
            bg="#2980b9", fg="white",
            font=("Arial", 10, "bold"), padx=12, pady=4
        ).pack(pady=8)
 
def _refrescar_logs(self):
        """Lee logs.txt y lo muestra. Si no hay errores lo indica. (R12)"""
        try:
            ruta = "logs.txt"
            contenido = ""
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
 
            self.txt_logs.configure(state="normal")
            self.txt_logs.delete("1.0", "end")
 
            if contenido:
                self.txt_logs.insert("end", contenido)
            else:
                self.txt_logs.insert(
                    "end",
                    "✔  El sistema se ha ejecutado sin errores hasta el momento."
                )
            self.txt_logs.configure(state="disabled")
            self.txt_logs.see("end")
        except Exception as e:
            print(f"[R12] Error al leer logs: {e}")
