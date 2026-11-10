from DAO.Conexion import Conexion
import bcrypt

host = 'localhost'
user = 'userempresa'
passwordS = 'V3ntana.13'
db = 'ecotech'

class Usuario:
    TIPOS_VALIDOS = {"Administrador", "Empleado"}

    def __init__(self, username, password_hash, nombre, apellido, email, tipo_usuario):
        self.username = username
        self.password_hash = password_hash
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.tipo_usuario = self.normalizar_tipo(tipo_usuario)

    @staticmethod
    def normalizar_tipo(tipo_usuario):
        if tipo_usuario not in Usuario.TIPOS_VALIDOS:
            raise ValueError("Tipo de usuario inválido.")
        return tipo_usuario

    @staticmethod # Método estático para iniciar sesión (no requiere instancia de la clase)
    def login(username, password):
        con = None
        try:
            # La contraseña que llega aquí es la de la cuenta del usuario
            # y NO debe reemplazar la contraseña de la base de datos.
            con = Conexion(host, user, passwordS, db)
            if not con or not con.db:
                return None

            usuario_data = con.obtenerUsuario(username)

            if usuario_data:
                hashed_password = usuario_data[2].encode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return Usuario(
                        username=usuario_data[1],
                        password_hash=usuario_data[2],
                        nombre=usuario_data[3],
                        apellido=usuario_data[4],
                        email=usuario_data[5],
                        tipo_usuario=usuario_data[6]
                    )
                return None
        except Exception as e:
            print("Error en login:", e)
            return None
        finally:
            if con:
                con.desconectar()

    @staticmethod
    def registrar_usuario(username, password, nombre, apellido, email, tipo_usuario):
        con = None
        try:
            tipo_usuario = Usuario.normalizar_tipo(tipo_usuario)
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            con = Conexion(host, user, passwordS, db)

            exito = con.agregarUsuario(
                username=username,
                password_hash=hashed_password,
                nombre=nombre,
                apellido=apellido,
                email=email,
                tipo_usuario=tipo_usuario
            )
            return exito
        except Exception as e:
            print("Error en registro:", e)
            return False
        finally:
            if con:
                con.desconectar()