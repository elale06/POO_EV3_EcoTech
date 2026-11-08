import os, re
from datetime import datetime

from DAO import CRUDAsignacion_emp, CRUDDepartamento, CRUDEmpleado, CRUDProyecto, CRUDTiempo
from DTO.AsignacionEmp import AsignacionEmp
from DTO.Departamento import Departamento
from DTO.Empleado import Empleado
from DTO.Proyecto import Proyecto
from DTO.RegistroTiempo import RegistroTiempo
from seguridad_api import autenticar, consultar_clima, consultar_tipo_cambio

def limpiar_pantalla():
    os.system("cls")

def pausa():
    input("\nPresione una tecla para continuar...")

def leer_entero(mensaje, minimo=None, maximo=None, permitir_vacio=False, valor_por_defecto=None):
    while True:
        texto = input(mensaje).strip()
        if permitir_vacio and texto == "":
            return valor_por_defecto
        try:
            valor = int(texto)
            if minimo is not None and valor < minimo:
                print(f"Debe ser mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Debe ser menor o igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Ingrese un número válido.")

def leer_texto(mensaje, permitir_vacio=False, valor_por_defecto=None):
    texto = input(mensaje).strip()
    if texto == "" and permitir_vacio:
        return valor_por_defecto
    return texto

def leer_fecha(mensaje, permitir_vacio=False, valor_por_defecto=None):
    año_max = 2026
    while True:
        texto = input(mensaje).strip()
        if permitir_vacio and texto == "":
            return valor_por_defecto
        try:
            fecha = datetime.strptime(texto, "%Y-%m-%d").date()
            if fecha.year > año_max:
                print(f"Ingrese una fecha con año menor o igual a {año_max}.")
                continue
            return fecha
        except ValueError:
            print("Ingrese una fecha válida con formato YYYY-MM-DD.")

# Verifica que el RUN tenga formato chileno básico: 12345678-9.
def leer_run(mensaje, permitir_vacio=False, valor_por_defecto=None):
    patron = re.compile(r"^[0-9]{7,8}-[0-9kK]$")
    while True:
        texto = input(mensaje).strip()
        if permitir_vacio and texto == "":
            return valor_por_defecto
        if patron.match(texto):
            return texto
        print("RUN inválido. Use formato 12345678-9.")

# Verifica que el correo tenga dominio y TLD válidos.
def leer_correo(mensaje, permitir_vacio=False, valor_por_defecto=None):
    patron = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
    while True:
        texto = input(mensaje).strip()
        if permitir_vacio and texto == "":
            return valor_por_defecto
        if patron.match(texto):
            return texto
        print("Correo inválido. Ejemplo: nombre@correo.com")


# Repite la lectura hasta encontrar un departamento que exista en la base.
def leer_departamento_existente(mensaje, permitir_vacio=False, valor_por_defecto=None, permitir_cancelar=False):
    while True:
        departamento_id = leer_entero(
            mensaje,
            minimo=0 if permitir_cancelar else 1,
            permitir_vacio=permitir_vacio,
            valor_por_defecto=valor_por_defecto,
        )
        if departamento_id == 0 and permitir_cancelar:
            return None
        if CRUDEmpleado.existe_departamento(departamento_id):
            return departamento_id
        print("El departamento indicado no existe. Intente nuevamente.")

# Verifica que el teléfono tenga solo números y una longitud razonable.
def leer_telefono(mensaje, permitir_vacio=False, valor_por_defecto=None):
    patron = re.compile(r"^[0-9]{7,15}$")
    while True:
        texto = input(f"{mensaje}(ej: 56912345678):").strip()
        if permitir_vacio and texto == "":
            return valor_por_defecto
        if patron.match(texto):
            return int(texto)
        print("Telefono inválido. Ingrese solo números, entre 7 y 15 dígitos. Ejemplo: 56912345678")


def recortar_texto(valor, maximo):
    texto = str(valor)
    if len(texto) <= maximo:
        return texto
    return texto[: maximo - 3] + "..."

# Normaliza fechas para que las tablas se vean consistentes.
def formatear_fecha(valor):
    return valor.strftime("%Y-%m-%d") if hasattr(valor, "strftime") else str(valor)

# Repite la lectura hasta que el ID exista en la tabla indicada.
def leer_id_existente(mensaje, existe_func, entidad, permitir_cancelar=False):
    while True:
        valor = leer_entero(mensaje, minimo=0)
        if valor == 0 and permitir_cancelar:
            return None
        if existe_func(valor):
            return valor
        print(f"El {entidad} indicado no existe. Ingrese un ID válido o 0 para cancelar.")

# Muestra los registros disponibles con su ID para que el usuario elija uno válido.
def mostrar_ids_disponibles(entidad, datos):
    if not datos:
        print(f"No hay {entidad}s registrados.")
        return False

    indice_nombre = {
        "empleado": 2,
        "departamento": 1,
        "proyecto": 1,
    }.get(entidad)

    print(f"\n{entidad.capitalize()}s disponibles:")
    for item in datos:
        nombre = f" - {item[indice_nombre]}" if indice_nombre is not None else ""
        print(f"ID: {item[0]}{nombre}")
    return True

# Pregunta de confirmación antes de borrar un registro.
def confirmar_eliminacion(entidad):
    while True:
        respuesta = input(f"¿Está seguro que desea eliminar este {entidad}? (S/N): ").strip().lower()
        if respuesta in ["s", "si", "sí", "y"]:
            return True
        if respuesta in ["n", "no"]:
            return False
        print("Respuesta inválida. Ingrese S o N.")

# Permite asignar gerente o usar 0 si no quiere definirlo.
def leer_gerente_existente(mensaje, valor_por_defecto=None, permitir_vacio=False):
    while True:
        gerente_id = leer_entero(mensaje, minimo=0, permitir_vacio=permitir_vacio, valor_por_defecto=valor_por_defecto)
        if gerente_id == 0:
            return 0
        if CRUDDepartamento.existe_gerente_empleado(gerente_id):
            return gerente_id
        print("El empleado indicado no existe. Intente nuevamente.")

def mostrar_departamentos_existentes():
    datos = CRUDDepartamento.mostrarTodos()
    if not datos:
        print("No hay departamentos registrados.")
        return False

    print("\nDepartamentos disponibles:")
    for departamento in datos:
        print(f"{departamento[0]} - {departamento[1]}")
    return True

def mostrar_empleados_existentes():
    datos = CRUDEmpleado.mostrarTodos()
    if not datos:
        print("No hay empleados registrados.")
        return False

    print("\nEmpleados disponibles:")
    for empleado in datos:
        print(f"{empleado[0]} - {empleado[2]}")
    return True

def mostrar_proyectos_existentes():
    datos = CRUDProyecto.mostrarTodos()
    if not datos:
        print("No hay proyectos registrados.")
        return False

    print("\nProyectos disponibles:")
    for proyecto in datos:
        print(f"{proyecto[0]} - {proyecto[1]}")
    return True

def menu_principal():
    print("==============================")
    print("        MENÚ PRINCIPAL        ")
    print("==============================")
    print("1. Gestión de Empleados")
    print("2. Gestión de Departamentos")
    print("3. Gestión de Proyectos")
    print("4. Registro de Tiempo")
    print("5. Asignación de empleado a proyectos")
    print("6. Consultar servicios externos")
    print("7. Salir")
    print("==============================")

def menu_empleados():
    print("=== Empleados ===")
    print("1. Ingresar empleado")
    print("2. Mostrar todos")
    print("3. Mostrar uno")
    print("4. Modificar")
    print("5. Eliminar")
    print("6. Volver")
    print("==============")

def menu_departamentos():
    print("=== Departamentos ===")
    print("1. Ingresar departamento")
    print("2. Mostrar todos")
    print("3. Mostrar uno")
    print("4. Modificar")
    print("5. Eliminar")
    print("6. Volver")
    print("=================")

def menu_proyectos():
    print("=== Proyectos ===")
    print("1. Ingresar proyecto")
    print("2. Mostrar todos")
    print("3. Modificar")
    print("4. Eliminar")
    print("5. Volver")
    print("=============")

def menu_tiempo():
    print("=== Registro de Tiempo ===")
    print("1. Ingresar registro")
    print("2. Mostrar por empleado")
    print("3. Volver")
    print("=================")

def menu_asignacion():
    print("=== Asignaciones Empleado-Proyecto ===")
    print("1. Asignar")
    print("2. Desasignar")
    print("3. Mostrar por empleado")
    print("4. Volver")
    print("====================================")

def menu_servicios():
    print("=== Servicios externos ===")
    print("1. Consultar clima")
    print("2. Consultar tipo de cambio")
    print("3. Volver")
    print("==========================")

def gestion_servicios(sesion):
    while True:
        limpiar_pantalla()
        menu_servicios()
        opcion = leer_entero("Opción: ", minimo=0, maximo=3)

        if opcion == 0 or opcion == 3:
            return

        try:
            if opcion == 1:
                ciudad = leer_texto("Ciudad: ")
                clima = consultar_clima(sesion, ciudad)
                print(
                    f"{clima['ciudad']}: {clima['temperatura']} °C, "
                    f"código meteorológico {clima['codigo_clima']}."
                )
            elif opcion == 2:
                moneda = leer_texto("Moneda (USD o CLP): ")
                tipo_cambio = consultar_tipo_cambio(sesion, moneda)
                print(
                    f"1 {tipo_cambio['moneda']} = "
                    f"{tipo_cambio['valor']:.6f} {tipo_cambio['moneda_destino']} "
                    f"(fecha: {tipo_cambio['fecha']})."
                )
        except (ValueError, PermissionError, RuntimeError) as error:
            print(error)
        pausa()

def ingresar_empleado():
    limpiar_pantalla()
    print("=== Empleados ===")

    if not CRUDDepartamento.existe_departamentos():
        print("No se puede ingresar un empleado si no existen departamentos.")
        pausa()
        return

    run = leer_run("RUN: ")
    nombre = leer_texto("Nombre: ")
    direccion = leer_texto("Direccion: ")
    telefono = leer_telefono("Telefono ")
    correo = leer_correo("Correo: ")
    fecha_inicio = leer_fecha("Fecha de inicio (YYYY-MM-DD): ")
    salario = leer_entero("Salario: ", minimo=0)

    mostrar_departamentos_existentes()
    departamento_id = leer_departamento_existente("Departamento ID: ", permitir_cancelar=True)
    if departamento_id is None:
        print("Ingreso cancelado.")
        pausa()
        return

    empleado = Empleado(run, nombre, direccion, telefono, correo, fecha_inicio, salario, departamento_id)
    nuevo_id = CRUDEmpleado.agregar(empleado)

    if nuevo_id:
        print(f"Empleado ingresado correctamente. ID: {nuevo_id}")
    else:
        print("No se pudo ingresar el empleado.")
    pausa()

def mostrar_empleados():
    limpiar_pantalla()
    print("=== Empleados ===")
    datos = CRUDEmpleado.mostrarTodos()

    if not datos:
        print("No hay empleados registrados.")
        pausa()
        return

    print("=" * 150)
    print("{:<5} {:<13} {:<18} {:<22} {:<12} {:<25} {:<12} {:>10} {:<10} {:<18}".format(
        "ID", "RUN", "NOMBRE", "DIRECCION", "TELF", "CORREO", "INICIO", "SALARIO", "DEPTO ID", "DEPTO"
    ))
    print("=" * 150)
    for empleado in datos:
        print("{:<5} {:<13} {:<18} {:<22} {:<12} {:<25} {:<12} {:>10} {:<10} {:<18}".format(
            empleado[0],
            recortar_texto(empleado[1], 13),
            recortar_texto(empleado[2], 18),
            recortar_texto(empleado[3], 22),
            recortar_texto(empleado[4], 12),
            recortar_texto(empleado[5], 25),
            recortar_texto(empleado[6], 12),
            empleado[7],
            empleado[8],
            recortar_texto(empleado[9], 18)
        ))
    print("=" * 150)
    pausa()

# Vista individual del empleado, útil para depurar un ID específico.
def mostrar_un_empleado():
    limpiar_pantalla()
    print("=== Empleados ===")
    empleado_id = leer_id_existente(
        "ID del empleado: ",
        CRUDEmpleado.existe_empleado,
        "empleado",
        permitir_cancelar=True,
    )
    if empleado_id is None:
        print("Consulta cancelada.")
        pausa()
        return
    empleado = CRUDEmpleado.consultaParticular(empleado_id)

    if not empleado:
        print("Empleado no encontrado.")
        pausa()
        return

    print(f"ID: {empleado[0]}")
    print(f"RUN: {empleado[1]}")
    print(f"Nombre: {empleado[2]}")
    print(f"Direccion: {empleado[3]}")
    print(f"Telefono: {empleado[4]}")
    print(f"Correo: {empleado[5]}")
    print(f"Fecha inicio: {empleado[6]}")
    print(f"Salario: {empleado[7]}")
    print(f"Departamento ID: {empleado[8]}")
    print(f"Departamento: {empleado[9]}")
    pausa()

# Formulario de edición: primero carga el registro y luego permite cambiar campos.
def modificar_empleado():
    limpiar_pantalla()
    print("=== Empleados ===")
    datos_empleados = CRUDEmpleado.mostrarTodos()
    if not mostrar_ids_disponibles("empleado", datos_empleados):
        pausa()
        return
    empleado_id = leer_id_existente("ID del empleado a modificar: ", CRUDEmpleado.existe_empleado, "empleado", permitir_cancelar=True)
    if empleado_id is None:
        print("Modificación cancelada.")
        pausa()
        return
    datos = CRUDEmpleado.consultaParticular(empleado_id)

    if not datos:
        print("Empleado no encontrado.")
        pausa()
        return

    print("Deje vacio para mantener el valor actual.")
    run = leer_run(f"RUN [{datos[1]}]: ", permitir_vacio=True, valor_por_defecto=datos[1])
    nombre = leer_texto(f"Nombre [{datos[2]}]: ", permitir_vacio=True, valor_por_defecto=datos[2])
    direccion = leer_texto(f"Direccion [{datos[3]}]: ", permitir_vacio=True, valor_por_defecto=datos[3])
    telefono = leer_telefono(f"Telefono [{datos[4]}]: ", permitir_vacio=True, valor_por_defecto=datos[4])
    correo = leer_correo(f"Correo [{datos[5]}]: ", permitir_vacio=True, valor_por_defecto=datos[5])
    fecha_inicio = leer_fecha(f"Fecha inicio [{datos[6]}] (YYYY-MM-DD): ", permitir_vacio=True, valor_por_defecto=datos[6])
    salario = leer_entero(f"Salario [{datos[7]}]: ", permitir_vacio=True, valor_por_defecto=datos[7])

    mostrar_departamentos_existentes()
    departamento_id = leer_departamento_existente(
        f"Departamento ID [{datos[8]}]: ",
        permitir_vacio=True,
        valor_por_defecto=datos[8],
        permitir_cancelar=True,
    )
    if departamento_id is None:
        print("Modificación cancelada.")
        pausa()
        return

    empleado = Empleado(run, nombre, direccion, telefono, correo, fecha_inicio, salario, departamento_id, empleado_id)
    if CRUDEmpleado.editar(empleado):
        print("Empleado modificado correctamente.")
    else:
        print("No se pudo modificar el empleado.")
    pausa()

# Borrado validado: no continúa si el empleado no existe.
def eliminar_empleado():
    limpiar_pantalla()
    print("=== Empleados ===")
    mostrar_empleados()
    empleado_id = leer_id_existente(
        "ID del empleado a eliminar: ",
        CRUDEmpleado.existe_empleado,
        "empleado",
        permitir_cancelar=True,
    )
    if empleado_id is None:
        print("Eliminación cancelada.")
        pausa()
        return

    if not confirmar_eliminacion("empleado"):
        print("Eliminación cancelada.")
        pausa()
        return

    if CRUDEmpleado.eliminar(empleado_id):
        print("Empleado eliminado correctamente.")
    else:
        print("No se pudo eliminar el empleado.")
    pausa()

# Alta de departamento con gerente opcional.
def ingresar_departamento():
    limpiar_pantalla()
    print("=== Departamentos ===")

    nombre = leer_texto("Nombre: ")
    descripcion = leer_texto("Descripcion: ")

    if mostrar_empleados_existentes():
        print("Si aun no quiere asignar gerente, use 0.")
        gerente_empleado_id = leer_gerente_existente("Gerente empleado ID: ")
    else:
        gerente_empleado_id = 0

    departamento = Departamento(nombre, gerente_empleado_id, descripcion)
    nuevo_id = CRUDDepartamento.agregar(departamento)

    if nuevo_id:
        print(f"Departamento ingresado correctamente. ID: {nuevo_id}")
    else:
        print("No se pudo ingresar el departamento.")
    pausa()

# Tabla resumida de departamentos, con recorte para que no se desordene.
def mostrar_departamentos():
    limpiar_pantalla()
    print("=== Departamentos ===")
    datos = CRUDDepartamento.mostrarTodos()

    if not datos:
        print("No hay departamentos registrados.")
        pausa()
        return

    print("=" * 110)
    print("{:<5} {:<24} {:<12} {:<22} {:<45}".format("ID", "NOMBRE", "GERENTE ID", "GERENTE", "DESCRIPCION"))
    print("=" * 110)
    for departamento in datos:
        print("{:<5} {:<24} {:<12} {:<22} {:<45}".format(
            departamento[0],
            recortar_texto(departamento[1], 24),
            departamento[2],
            recortar_texto(departamento[3], 22),
            recortar_texto(departamento[4], 45),
        ))
    print("=" * 110)
    pausa()

# Consulta puntual de un departamento por su ID.
def mostrar_un_departamento():
    limpiar_pantalla()
    print("=== Departamentos ===")
    departamento_id = leer_id_existente(
        "ID del departamento: ",
        CRUDDepartamento.existe_departamento,
        "departamento",
        permitir_cancelar=True,
    )
    if departamento_id is None:
        print("Consulta cancelada.")
        pausa()
        return
    departamento = CRUDDepartamento.consultaParticular(departamento_id)

    if not departamento:
        print("Departamento no encontrado.")
        pausa()
        return

    print(f"ID: {departamento[0]}")
    print(f"Nombre: {departamento[1]}")
    print(f"Gerente ID: {departamento[2]}")
    print(f"Gerente: {departamento[3]}")
    print(f"Descripcion: {departamento[4]}")
    pausa()

# Edición de departamento, conservando valores si se deja vacío.
def modificar_departamento():
    limpiar_pantalla()
    print("=== Departamentos ===")
    datos_departamentos = CRUDDepartamento.mostrarTodos()
    if not mostrar_ids_disponibles("departamento", datos_departamentos):
        pausa()
        return
    departamento_id = leer_id_existente("ID del departamento a modificar: ", CRUDDepartamento.existe_departamento, "departamento", permitir_cancelar=True)
    if departamento_id is None:
        print("Modificación cancelada.")
        pausa()
        return
    datos = CRUDDepartamento.consultaParticular(departamento_id)

    if not datos:
        print("Departamento no encontrado.")
        pausa()
        return

    print("Deje vacio para mantener el valor actual.")
    nombre = leer_texto(f"Nombre [{datos[1]}]: ", permitir_vacio=True, valor_por_defecto=datos[1])
    descripcion = leer_texto(f"Descripcion [{datos[4]}]: ", permitir_vacio=True, valor_por_defecto=datos[4])
    if mostrar_empleados_existentes():
        print("Si no desea gerente, use 0.")
        gerente_empleado_id = leer_entero(f"Gerente empleado ID [{datos[2]}]: ", permitir_vacio=True, valor_por_defecto=datos[2])
        if gerente_empleado_id != 0 and not CRUDEmpleado.consultaParticular(gerente_empleado_id):
            print("El gerente indicado no existe.")
            pausa()
            return
    else:
        gerente_empleado_id = 0

    departamento = Departamento(nombre, gerente_empleado_id, descripcion, departamento_id)
    if CRUDDepartamento.editar(departamento):
        print("Departamento modificado correctamente.")
    else:
        print("No se pudo modificar el departamento.")
    pausa()

# Eliminación validada de departamento.
def eliminar_departamento():
    limpiar_pantalla()
    print("=== Departamentos ===")
    mostrar_departamentos()
    departamento_id = leer_id_existente(
        "ID del departamento a eliminar: ",
        CRUDDepartamento.existe_departamento,
        "departamento",
        permitir_cancelar=True,
    )
    if departamento_id is None:
        print("Eliminación cancelada.")
        pausa()
        return

    if not confirmar_eliminacion("departamento"):
        print("Eliminación cancelada.")
        pausa()
        return

    if CRUDDepartamento.eliminar(departamento_id):
        print("Departamento eliminado correctamente.")
    else:
        print("No se pudo eliminar el departamento.")
    pausa()

# Alta de proyecto.
def ingresar_proyecto():
    limpiar_pantalla()
    print("=== Proyectos ===")
    nombre = leer_texto("Nombre: ")
    descripcion = leer_texto("Descripcion: ")
    fecha_inicio = leer_fecha("Fecha de inicio (YYYY-MM-DD): ")

    proyecto = Proyecto(nombre, descripcion, fecha_inicio)
    nuevo_id = CRUDProyecto.agregar(proyecto)
    if nuevo_id:
        print(f"Proyecto ingresado correctamente. ID: {nuevo_id}")
    else:
        print("No se pudo ingresar el proyecto.")
    pausa()


# Listado de proyectos con fecha formateada.
def mostrar_proyectos():
    limpiar_pantalla()
    print("=== Proyectos ===")
    datos = CRUDProyecto.mostrarTodos()

    if not datos:
        print("No hay proyectos registrados.")
        pausa()
        return

    print("=" * 95)
    print("{:<5} {:<25} {:<48} {:<12}".format("ID", "NOMBRE", "DESCRIPCION", "INICIO"))
    print("=" * 95)
    for proyecto in datos:
        print("{:<5} {:<25} {:<48} {:<12}".format(
            proyecto[0],
            recortar_texto(proyecto[1], 25),
            recortar_texto(proyecto[2], 48),
            formatear_fecha(proyecto[3]),
        ))
    print("=" * 95)
    pausa()


# Edición de proyecto.
def modificar_proyecto():
    limpiar_pantalla()
    print("=== Proyectos ===")
    datos_proyectos = CRUDProyecto.mostrarTodos()
    if not mostrar_ids_disponibles("proyecto", datos_proyectos):
        pausa()
        return
    proyecto_id = leer_id_existente("ID del proyecto a modificar: ", CRUDProyecto.existe_proyecto, "proyecto", permitir_cancelar=True)
    if proyecto_id is None:
        print("Modificación cancelada.")
        pausa()
        return
    datos = CRUDProyecto.consultaParticular(proyecto_id)

    if not datos:
        print("Proyecto no encontrado.")
        pausa()
        return

    print("Deje vacio para mantener el valor actual.")
    nombre = leer_texto(f"Nombre [{datos[1]}]: ", permitir_vacio=True, valor_por_defecto=datos[1])
    descripcion = leer_texto(f"Descripcion [{datos[2]}]: ", permitir_vacio=True, valor_por_defecto=datos[2])
    fecha_inicio = leer_fecha(f"Fecha de inicio [{datos[3]}] (YYYY-MM-DD): ", permitir_vacio=True, valor_por_defecto=datos[3])

    proyecto = Proyecto(nombre, descripcion, fecha_inicio, proyecto_id)
    if CRUDProyecto.editar(proyecto):
        print("Proyecto modificado correctamente.")
    else:
        print("No se pudo modificar el proyecto.")
    pausa()

# Eliminación validada de proyecto.
def eliminar_proyecto():
    limpiar_pantalla()
    print("=== Proyectos ===")
    mostrar_proyectos()
    proyecto_id = leer_id_existente(
        "ID del proyecto a eliminar: ",
        CRUDProyecto.existe_proyecto,
        "proyecto",
        permitir_cancelar=True,
    )

    if proyecto_id is None:
        print("Eliminación cancelada.")
        pausa()
        return

    if not confirmar_eliminacion("proyecto"):
        print("Eliminación cancelada.")
        pausa()
        return

    if CRUDProyecto.eliminar(proyecto_id):
        print("Proyecto eliminado correctamente.")
    else:
        print("No se pudo eliminar el proyecto.")
    pausa()

# Registro de horas trabajadas por empleado y proyecto.
def ingresar_registro_tiempo():
    limpiar_pantalla()
    print("=== Registro Tiempo ===")

    if not mostrar_empleados_existentes():
        pausa()
        return
    empleado_id = leer_id_existente("Empleado ID: ", CRUDEmpleado.existe_empleado, "empleado", permitir_cancelar=True)
    if empleado_id is None:
        print("Ingreso cancelado.")
        pausa()
        return

    if not mostrar_proyectos_existentes():
        pausa()
        return
    proyecto_id = leer_id_existente("Proyecto ID: ", CRUDProyecto.existe_proyecto, "proyecto", permitir_cancelar=True)
    if proyecto_id is None:
        print("Ingreso cancelado.")
        pausa()
        return

    fecha = leer_fecha("Fecha (YYYY-MM-DD): ")
    horas = leer_entero("Horas: ", minimo=0)
    descripcion = leer_texto("Descripcion: ")

    registro = RegistroTiempo(empleado_id, proyecto_id, fecha, horas, descripcion)
    nuevo_id = CRUDTiempo.agregar(registro)
    if nuevo_id:
        print(f"Registro ingresado correctamente. ID: {nuevo_id}")
    else:
        print("No se pudo ingresar el registro.")
    pausa()

# Historial de tiempo por empleado.
def mostrar_registros_por_empleado():
    limpiar_pantalla()
    print("=== Registro Tiempo ===")
    if not mostrar_empleados_existentes():
        pausa()
        return
    empleado_id = leer_id_existente(
        "Empleado ID: ",
        CRUDEmpleado.existe_empleado,
        "empleado",
        permitir_cancelar=True,
    )
    if empleado_id is None:
        print("Consulta cancelada.")
        pausa()
        return
    registros = CRUDTiempo.mostrarPorEmpleado(empleado_id)

    if not registros:
        print("No hay registros para ese empleado.")
        pausa()
        return

    print("=" * 120)
    print("{:<5} {:<10} {:<20} {:<10} {:<22} {:<12} {:>8} {:<35}".format(
        "ID", "EMP ID", "EMPLEADO", "PROY ID", "PROYECTO", "FECHA", "HORAS", "DESCRIPCION"
    ))
    print("=" * 120)
    for registro in registros:
        print("{:<5} {:<10} {:<20} {:<10} {:<22} {:<12} {:>8} {:<35}".format(
            registro[0],
            registro[1],
            recortar_texto(registro[2], 20),
            registro[3],
            recortar_texto(registro[4], 22),
            formatear_fecha(registro[5]),
            registro[6],
            recortar_texto(registro[7], 35),
        ))
    print("=" * 120)
    pausa()

# Asignación de un empleado a un proyecto.
def asignar_empleado_a_proyecto():
    limpiar_pantalla()
    print("=== Asignaciones Empleado-Proyecto ===")

    if not mostrar_empleados_existentes():
        pausa()
        return
    empleado_id = leer_id_existente("Empleado ID: ", CRUDEmpleado.existe_empleado, "empleado", permitir_cancelar=True)
    if empleado_id is None:
        print("Asignación cancelada.")
        pausa()
        return

    if not mostrar_proyectos_existentes():
        pausa()
        return
    proyecto_id = leer_id_existente("Proyecto ID: ", CRUDProyecto.existe_proyecto, "proyecto", permitir_cancelar=True)
    if proyecto_id is None:
        print("Asignación cancelada.")
        pausa()
        return

    fecha_asignacion = leer_fecha("Fecha asignacion (YYYY-MM-DD): ")
    rol = leer_texto("Rol: ")

    asignacion = AsignacionEmp(empleado_id, proyecto_id, fecha_asignacion, rol)
    nuevo_id = CRUDAsignacion_emp.agregar(asignacion)
    if nuevo_id:
        print(f"Asignación ingresada correctamente. ID: {nuevo_id}")
    else:
        print("No se pudo ingresar la asignación.")
    pausa()

# Historial de asignaciones por empleado.
def mostrar_asignaciones():
    limpiar_pantalla()
    print("=== Asignaciones Empleado-Proyecto ===")
    if not mostrar_empleados_existentes():
        pausa()
        return
    empleado_id = leer_id_existente(
        "Empleado ID: ",
        CRUDEmpleado.existe_empleado,
        "empleado",
        permitir_cancelar=True,
    )
    if empleado_id is None:
        print("Consulta cancelada.")
        pausa()
        return
    datos = CRUDAsignacion_emp.mostrarPorEmpleado(empleado_id)

    if not datos:
        print("No hay asignaciones registradas para ese empleado.")
        pausa()
        return

    print("=" * 110)
    print("{:<5} {:<10} {:<22} {:<10} {:<22} {:<12} {:<25}".format(
        "ID", "EMP ID", "EMPLEADO", "PROY ID", "PROYECTO", "FECHA", "ROL"
    ))
    print("=" * 110)
    for asignacion in datos:
        print("{:<5} {:<10} {:<22} {:<10} {:<22} {:<12} {:<25}".format(
            asignacion[0],
            asignacion[1],
            recortar_texto(asignacion[2], 22),
            asignacion[3],
            recortar_texto(asignacion[4], 22),
            formatear_fecha(asignacion[5]),
            recortar_texto(asignacion[6], 25),
        ))
    print("=" * 110)
    pausa()

# Elimina una asignación perteneciente al empleado seleccionado.
def desasignar_empleado_de_proyecto():
    limpiar_pantalla()
    print("=== Desasignar empleado de proyecto ===")

    if not mostrar_empleados_existentes():
        pausa()
        return
    empleado_id = leer_id_existente(
        "Empleado ID: ",
        CRUDEmpleado.existe_empleado,
        "empleado",
        permitir_cancelar=True,
    )
    if empleado_id is None:
        print("Desasignación cancelada.")
        pausa()
        return

    asignaciones = CRUDAsignacion_emp.mostrarPorEmpleado(empleado_id)
    if not asignaciones:
        print("No hay asignaciones registradas para ese empleado.")
        pausa()
        return

    print("\nAsignaciones del empleado:")
    print("=" * 95)
    print("{:<5} {:<10} {:<25} {:<12} {:<25}".format(
        "ID", "PROY ID", "PROYECTO", "FECHA", "ROL"
    ))
    print("=" * 95)
    for asignacion in asignaciones:
        print("{:<5} {:<10} {:<25} {:<12} {:<25}".format(
            asignacion[0],
            asignacion[3],
            recortar_texto(asignacion[4], 25),
            formatear_fecha(asignacion[5]),
            recortar_texto(asignacion[6], 25),
        ))
    print("=" * 95)

    ids_asignaciones = {asignacion[0] for asignacion in asignaciones}
    while True:
        asignacion_id = leer_entero(
            "ID de la asignación a eliminar (0 para cancelar): ",
            minimo=0,
        )
        if asignacion_id == 0:
            print("Desasignación cancelada.")
            pausa()
            return
        if asignacion_id in ids_asignaciones:
            break
        print("La asignación indicada no pertenece a ese empleado.")

    if not confirmar_eliminacion("asignación"):
        print("Desasignación cancelada.")
        pausa()
        return

    if CRUDAsignacion_emp.eliminar(asignacion_id):
        print("Empleado desasignado del proyecto correctamente.")
    else:
        print("No se pudo desasignar el empleado del proyecto.")
    pausa()

def gestion_empleados():
    while True:
        limpiar_pantalla()
        menu_empleados()
        opcion = leer_entero("Ingrese opción: ", minimo=0, maximo=6)

        if opcion == 0 or opcion == 6:
            break
        elif opcion == 1:
            ingresar_empleado()
        elif opcion == 2:
            mostrar_empleados()
        elif opcion == 3:
            mostrar_un_empleado()
        elif opcion == 4:
            modificar_empleado()
        elif opcion == 5:
            eliminar_empleado()
def gestion_departamentos():
    while True:
        limpiar_pantalla()
        menu_departamentos()
        opcion = leer_entero("Ingrese opción: ", minimo=0, maximo=6)

        if opcion == 0 or opcion == 6:
            break
        elif opcion == 1:
            ingresar_departamento()
        elif opcion == 2:
            mostrar_departamentos()
        elif opcion == 3:
            mostrar_un_departamento()
        elif opcion == 4:
            modificar_departamento()
        elif opcion == 5:
            eliminar_departamento()
def gestion_proyectos():
    while True:
        limpiar_pantalla()
        menu_proyectos()
        opcion = leer_entero("Ingrese opción: ", minimo=0, maximo=5)

        if opcion == 0 or opcion == 5:
            break
        elif opcion == 1:
            ingresar_proyecto()
        elif opcion == 2:
            mostrar_proyectos()
        elif opcion == 3:
            modificar_proyecto()
        elif opcion == 4:
            eliminar_proyecto()
def gestion_tiempo():
    while True:
        limpiar_pantalla()
        menu_tiempo()
        opcion = leer_entero("Opción: ", minimo=0, maximo=3)

        if opcion == 0 or opcion == 3:
            break
        elif opcion == 1:
            ingresar_registro_tiempo()
        elif opcion == 2:
            mostrar_registros_por_empleado()
def gestion_asignacion():
    while True:
        limpiar_pantalla()
        menu_asignacion()
        opcion = leer_entero("Opción: ", minimo=0, maximo=4)

        if opcion == 0 or opcion == 4:
            break
        elif opcion == 1:
            asignar_empleado_a_proyecto()
        elif opcion == 2:
            desasignar_empleado_de_proyecto()
        elif opcion == 3:
            mostrar_asignaciones()
def main():
    limpiar_pantalla()
    sesion = autenticar()
    if sesion is None:
        return

    while True:
        limpiar_pantalla()
        menu_principal()
        opcion = leer_entero("INGRESE OPCIÓN : ", minimo=0, maximo=7)

        if opcion == 0 or opcion == 7:
            break
        elif opcion == 1:
            gestion_empleados()
        elif opcion == 2:
            gestion_departamentos()
        elif opcion == 3:
            gestion_proyectos()
        elif opcion == 4:
            gestion_tiempo()
        elif opcion == 5:
            gestion_asignacion()
        elif opcion == 6:
            gestion_servicios(sesion)

if __name__ == "__main__":
    main()