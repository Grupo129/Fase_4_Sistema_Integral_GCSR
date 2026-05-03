# Grupo_129.
# Fase 4: Sistema Integral de Gestión de Clientes, Servicios y Reservas.
# Ingeniería de Sistemas.
# Autoría propia.

print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")

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
