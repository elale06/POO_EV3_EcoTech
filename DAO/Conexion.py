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
