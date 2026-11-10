import pymysql

class Conexion:
    # Administra el cursor y las operaciones básicas de la base de datos
    def __init__(self, host, user, password, db):
        self.db = None
        self.cursor = None
        try:
            self.db = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db
            )
            self.cursor = self.db.cursor()
        except Exception as e:
            print("Error de conexión:", e)

    def ejecuta_query(self, sql, valores=None):
        # Ejecuta SQL parametrizado para evitar concatenar valores de usuario
        try:
            if not self.cursor:
                return None
            if valores:
                self.cursor.execute(sql, valores)
            else:
                self.cursor.execute(sql)
            return self.cursor
        except Exception as e:
            print("Error en query:", e)
            return None

    def desconectar(self):
        # Cierra la conexión abierta con la base de datos
        if self.db:
            self.db.close()

    def commit(self):
        # Confirma la transacción actual
        if self.db:
            self.db.commit()

    def rollback(self):
        # Reviente la transacción actual cuando ocurre un error
        if self.db:
            self.db.rollback()

        # --------------------------------------------
    def obtenerUsuario(self, username):
        try:
            if not self.db or not self.cursor:
                return None
            sql = "SELECT * FROM usuarios WHERE username = %s"
            cursor = self.ejecuta_query(sql, (username,))
            if cursor:
                return cursor.fetchone()
            return None
        except Exception as e:
            print("Error al obtener usuario:", e)
            return None

    def existenUsuarios(self):
        try:
            if not self.db or not self.cursor:
                return False
            cursor = self.ejecuta_query("SELECT 1 FROM usuarios LIMIT 1")
            return bool(cursor and cursor.fetchone())
        except Exception as e:
            print("Error al verificar usuarios:", e)
            return False

    # --------------------------------------------
    def agregarUsuario(self, username, password_hash, nombre, apellido, email, tipo_usuario):
        try:
            sql = """INSERT INTO usuarios
            (username, password_hash, nombre, apellido, email, tipo_usuario)
            VALUES(%s, %s, %s, %s, %s, %s)"""

            valores = (username, password_hash, nombre, apellido, email, tipo_usuario)

            cursor = self.ejecuta_query(sql, valores)
            if not cursor:
                self.rollback()
                return False
            self.commit()
            return True
        except Exception as e:
            print("Error al agregar usuario:", e)
            self.rollback()
            return False