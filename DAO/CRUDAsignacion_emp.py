from DAO.Conexion import Conexion

host = 'localhost'
user = 'userempresa'
password = 'V3ntana.13'
db = 'ecotech'

def agregar(asignacion):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO asignacion_emp (empleado_id, proyecto_id, fecha_asignacion, rol)
        VALUES (%s, %s, %s, %s)
        """
        valores = (
            asignacion.empleado_id,
            asignacion.proyecto_id,
            asignacion.fecha_asignacion,
            asignacion.rol,
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

def eliminar(asignacion_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM asignacion_emp WHERE USER_ID=%s"
        cursor = con.ejecuta_query(sql, (asignacion_id,))
        con.commit()
        return bool(cursor and cursor.rowcount > 0)
    except Exception:
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.desconectar()

def mostrarTodos():
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT
            a.USER_ID,
            a.empleado_id,
            COALESCE(e.nombre, 'Sin nombre') AS empleado_nombre,
            a.proyecto_id,
            COALESCE(p.nombre, 'Sin nombre') AS proyecto_nombre,
            a.fecha_asignacion,
            a.rol
        FROM asignacion_emp a
        LEFT JOIN empleado e ON a.empleado_id = e.USER_ID
        LEFT JOIN proyecto p ON a.proyecto_id = p.USER_ID
        ORDER BY a.USER_ID
        """
        cursor = con.ejecuta_query(sql)
        return cursor.fetchall() if cursor else []
    except Exception:
        return []
    finally:
        if con:
            con.desconectar()


def mostrarPorEmpleado(empleado_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT
            a.USER_ID,
            a.empleado_id,
            COALESCE(e.nombre, 'Sin nombre') AS empleado_nombre,
            a.proyecto_id,
            COALESCE(p.nombre, 'Sin nombre') AS proyecto_nombre,
            a.fecha_asignacion,
            a.rol
        FROM asignacion_emp a
        LEFT JOIN empleado e ON a.empleado_id = e.USER_ID
        LEFT JOIN proyecto p ON a.proyecto_id = p.USER_ID
        WHERE a.empleado_id=%s
        ORDER BY a.USER_ID
        """
        cursor = con.ejecuta_query(sql, (empleado_id,))
        return cursor.fetchall() if cursor else []
    except Exception:
        return []
    finally:
        if con:
            con.desconectar()