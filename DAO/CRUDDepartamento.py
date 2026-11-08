from DAO.Conexion import Conexion

host = 'localhost'
user = 'userempresa'
password = 'V3ntana.13'
db = 'ecotech'

def agregar(departamento):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO departamento (nombre, gerente_empleado_id, descripcion)
        VALUES (%s, %s, %s)
        """
        valores = (
            departamento.nombre,
            departamento.gerente_empleado_id,
            departamento.descripcion,
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

def editar(departamento):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        UPDATE departamento SET
            nombre=%s,
            gerente_empleado_id=%s,
            descripcion=%s
        WHERE USER_ID=%s
        """
        valores = (
            departamento.nombre,
            departamento.gerente_empleado_id,
            departamento.descripcion,
            departamento.id,
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

def eliminar(departamento_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM departamento WHERE USER_ID=%s"
        cursor = con.ejecuta_query(sql, (departamento_id,))
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
            d.USER_ID,
            d.nombre,
            d.gerente_empleado_id,
            COALESCE(e.nombre, 'Sin asignar') AS gerente_nombre,
            d.descripcion
        FROM departamento d
        LEFT JOIN empleado e ON d.gerente_empleado_id = e.USER_ID
        ORDER BY d.USER_ID
        """
        cursor = con.ejecuta_query(sql)
        return cursor.fetchall() if cursor else []
    except Exception:
        return []
    finally:
        if con:
            con.desconectar()

def consultaParticular(departamento_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT
            d.USER_ID,
            d.nombre,
            d.gerente_empleado_id,
            COALESCE(e.nombre, 'Sin asignar') AS gerente_nombre,
            d.descripcion
        FROM departamento d
        LEFT JOIN empleado e ON d.gerente_empleado_id = e.USER_ID
        WHERE d.USER_ID=%s
        """
        cursor = con.ejecuta_query(sql, (departamento_id,))
        return cursor.fetchone() if cursor else None
    except Exception:
        return None
    finally:
        if con:
            con.desconectar()


def existe_gerente_empleado(empleado_id):
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

def existe_departamentos():
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT 1 FROM departamento LIMIT 1"
        cursor = con.ejecuta_query(sql)
        return cursor.fetchone() is not None if cursor else False
    except Exception:
        return False
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