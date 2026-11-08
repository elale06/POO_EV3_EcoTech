from DAO.Conexion import Conexion

host = 'localhost'
user = 'userempresa'
password = 'V3ntana.13'
db = 'ecotech'

def agregar(registro):
    # Guarda horas trabajadas asociadas a empleado y proyecto
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO tiempo (empleado_id, proyecto_id, fecha, horas, descripcion)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (
            registro.empleado_id,
            registro.proyecto_id,
            registro.fecha,
            registro.horas,
            registro.descripcion,
        )
        cursor = con.ejecuta_query(sql, valores)
        con.commit()
        return cursor.lastrowid if cursor else None
    except Exception:
        if con:
            con.rollback()
        return None
    finally:
        if con:
            con.desconectar()

def mostrarPorEmpleado(empleado_id):
    # Obtiene el historial de tiempo de un empleado
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT
            t.USER_ID,
            t.empleado_id,
            COALESCE(e.nombre, 'Sin nombre') AS empleado_nombre,
            t.proyecto_id,
            COALESCE(p.nombre, 'Sin nombre') AS proyecto_nombre,
            t.fecha,
            t.horas,
            t.descripcion
        FROM tiempo t
        LEFT JOIN empleado e ON t.empleado_id = e.USER_ID
        LEFT JOIN proyecto p ON t.proyecto_id = p.USER_ID
        WHERE t.empleado_id=%s
        ORDER BY t.fecha DESC, t.USER_ID DESC
        """
        cursor = con.ejecuta_query(sql, (empleado_id,))
        return cursor.fetchall() if cursor else []
    except Exception:
        return []
    finally:
        if con:
            con.desconectar()

def consultaParticular(registro_id):
    # Obtiene un registro de tiempo específico por ID
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT USER_ID, empleado_id, proyecto_id, fecha, horas, descripcion
        FROM tiempo
        WHERE USER_ID=%s
        """
        cursor = con.ejecuta_query(sql, (registro_id,))
        return cursor.fetchone() if cursor else None
    except Exception:
        return None
    finally:
        if con:
            con.desconectar()