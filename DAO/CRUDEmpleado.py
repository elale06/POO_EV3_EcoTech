from DAO.Conexion import Conexion

host = 'localhost'
user = 'userempresa'
password = 'V3ntana.13'
db = 'ecotech'

def agregar(empleado):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO empleado
        (run, nombre, direccion, telefono, correo, fecha_inicio, salario, departamento_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            empleado.run,
            empleado.nombre,
            empleado.direccion,
            empleado.telefono,
            empleado.correo,
            empleado.fecha_inicio,
            empleado.salario,
            empleado.departamento_id,
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

def editar(empleado):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        UPDATE empleado SET
            run=%s,
            nombre=%s,
            direccion=%s,
            telefono=%s,
            correo=%s,
            fecha_inicio=%s,
            salario=%s,
            departamento_id=%s
        WHERE USER_ID=%s
        """
        valores = (
            empleado.run,
            empleado.nombre,
            empleado.direccion,
            empleado.telefono,
            empleado.correo,
            empleado.fecha_inicio,
            empleado.salario,
            empleado.departamento_id,
            empleado.id,
        )
        con.ejecuta_query(sql, valores)
        con.commit()
        return True
    except Exception:
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.desconectar()

def eliminar(empleado_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM empleado WHERE USER_ID=%s"
        cursor = con.ejecuta_query(sql, (empleado_id,))
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
            e.USER_ID,
            e.run,
            e.nombre,
            e.direccion,
            e.telefono,
            e.correo,
            e.fecha_inicio,
            e.salario,
            e.departamento_id,
            COALESCE(d.nombre, 'Sin departamento') AS departamento_nombre
        FROM empleado e
        LEFT JOIN departamento d ON e.departamento_id = d.USER_ID
        ORDER BY e.USER_ID
        """
        cursor = con.ejecuta_query(sql)
        return cursor.fetchall() if cursor else []
    except Exception:
        return []
    finally:
        if con:
            con.desconectar()

def consultaParticular(empleado_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT
            e.USER_ID,
            e.run,
            e.nombre,
            e.direccion,
            e.telefono,
            e.correo,
            e.fecha_inicio,
            e.salario,
            e.departamento_id,
            COALESCE(d.nombre, 'Sin departamento') AS departamento_nombre
        FROM empleado e
        LEFT JOIN departamento d ON e.departamento_id = d.USER_ID
        WHERE e.USER_ID=%s
        """
        cursor = con.ejecuta_query(sql, (empleado_id,))
        return cursor.fetchone() if cursor else None
    except Exception:
        return None
    finally:
        if con:
            con.desconectar()

def existe_departamento(departamento_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT 1 FROM departamento WHERE USER_ID=%s"
        cursor = con.ejecuta_query(sql, (departamento_id,))
        return cursor.fetchone() is not None if cursor else False
    except Exception:
        return False
    finally:
        if con:
            con.desconectar()


def existe_empleado(empleado_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT 1 FROM empleado WHERE USER_ID=%s"
        cursor = con.ejecuta_query(sql, (empleado_id,))
        return cursor.fetchone() is not None if cursor else False
    except Exception:
        return False
    finally:
        if con:
            con.desconectar()