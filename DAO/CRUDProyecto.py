from DAO.Conexion import Conexion

host = 'localhost'
user = 'userempresa'
password = 'V3ntana.13'
db = 'ecotech'

def agregar(proyecto):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
        VALUES (%s, %s, %s)
        """
        valores = (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio)
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

def editar(proyecto):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        UPDATE proyecto SET
            nombre=%s,
            descripcion=%s,
            fecha_inicio=%s
        WHERE USER_ID=%s
        """
        valores = (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.id)
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

def eliminar(proyecto_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM proyecto WHERE USER_ID=%s"
        cursor = con.ejecuta_query(sql, (proyecto_id,))
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
        SELECT USER_ID, nombre, descripcion, fecha_inicio
        FROM proyecto
        ORDER BY USER_ID
        """
        cursor = con.ejecuta_query(sql)
        return cursor.fetchall() if cursor else []
    except Exception:
        return []
    finally:
        if con:
            con.desconectar()

def consultaParticular(proyecto_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT USER_ID, nombre, descripcion, fecha_inicio
        FROM proyecto
        WHERE USER_ID=%s
        """
        cursor = con.ejecuta_query(sql, (proyecto_id,))
        return cursor.fetchone() if cursor else None
    except Exception:
        return None
    finally:
        if con:
            con.desconectar()


def existe_proyecto(proyecto_id):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT 1 FROM proyecto WHERE USER_ID=%s"
        cursor = con.ejecuta_query(sql, (proyecto_id,))
        return cursor.fetchone() is not None if cursor else False
    except Exception:
        return False
    finally:
        if con:
            con.desconectar()