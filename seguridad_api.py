import os, re, getpass, bcrypt, requests
from typing import Optional

_USUARIOS = {
    # Hash bcrypt: la contraseña nunca se almacena en texto plano.
    "admin": "$2b$12$hSYnSuaZb4RveCZnMVJAl.EHkcBfR3V4BjQPqpq.KNKVTafdYEGS2",
}

class Sesion:
    def __init__(self, usuario: str):
        self.usuario = usuario

def autenticar(max_intentos: int = 3) -> Optional[Sesion]:
    for _ in range(max_intentos):
        usuario = input("Usuario: ").strip()
        contraseña = getpass.getpass("Contraseña: ")

        if not usuario or not contraseña:
            print("El usuario y la contraseña son obligatorios.")
            continue

        hash_guardado = _USUARIOS.get(usuario)
        if hash_guardado and bcrypt.checkpw(
            contraseña.encode("utf-8"), hash_guardado.encode("utf-8")
        ):
            return Sesion(usuario)

        print("Credenciales inválidas.")

    print("No fue posible iniciar sesión.")
    return None

def _exigir_sesion(sesion: Optional[Sesion]) -> None:
    if not isinstance(sesion, Sesion):
        raise PermissionError("Se requiere una sesión autenticada.")

def _obtener_api_key(nombre: str) -> str:
    api_key = os.getenv(nombre, "").strip()
    if not api_key:
        raise RuntimeError("Servicio no configurado.")
    return api_key

def _validar_ciudad(ciudad: str) -> str:
    ciudad = ciudad.strip()
    if not ciudad or len(ciudad) > 100 or not re.fullmatch(r"[A-Za-zÀ-ÿ0-9 .,'-]+", ciudad):
        raise ValueError("Ciudad inválida.")
    return ciudad

def _validar_moneda(moneda: str) -> str:
    moneda = moneda.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", moneda):
        raise ValueError("Moneda inválida.")
    return moneda

def consultar_clima(sesion: Optional[Sesion], ciudad: str) -> Optional[dict]:
    _exigir_sesion(sesion)
    ciudad = _validar_ciudad(ciudad)
    api_key = _obtener_api_key("OPENWEATHER_API_KEY")

    try:
        respuesta = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": ciudad,
                "appid": api_key,
                "units": "metric",
                "lang": "es",
            },
            timeout=10,
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("El servicio tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No fue posible conectar con el servicio.")
    except requests.exceptions.RequestException:
        raise RuntimeError("No fue posible consultar el servicio.")

    if respuesta.status_code == 404:
        raise RuntimeError("No se encontró la ciudad indicada.")
    if respuesta.status_code != 200:
        raise RuntimeError("El servicio del clima no está disponible.")

    try:
        datos = respuesta.json()
        return {
            "ciudad": datos["name"],
            "temperatura": datos["main"]["temp"],
            "descripcion": datos["weather"][0]["description"],
        }
    except (ValueError, KeyError, IndexError, TypeError):
        raise RuntimeError("El servicio devolvió una respuesta inválida.")

def consultar_tipo_cambio(sesion: Optional[Sesion], moneda: str) -> Optional[dict]:
    _exigir_sesion(sesion)
    moneda = _validar_moneda(moneda)
    api_key = _obtener_api_key("EXCHANGE_RATE_API_KEY")

    try:
        respuesta = requests.get(
            f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moneda}",
            timeout=10,
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("El servicio tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No fue posible conectar con el servicio.")
    except requests.exceptions.RequestException:
        raise RuntimeError("No fue posible consultar el servicio.")

    if respuesta.status_code == 404:
        raise RuntimeError("La moneda indicada no está disponible.")
    if respuesta.status_code != 200:
        raise RuntimeError("El servicio económico no está disponible.")

    try:
        datos = respuesta.json()
        if datos.get("result") != "success":
            raise RuntimeError("El servicio económico no está disponible.")
        return {
            "moneda": datos["base_code"],
            "tasas": datos["conversion_rates"],
        }
    except (ValueError, KeyError, TypeError):
        raise RuntimeError("El servicio devolvió una respuesta inválida.")
