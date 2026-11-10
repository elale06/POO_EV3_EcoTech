# Autenticación local y consumo seguro de servicios públicos externos
import re, requests
from datetime import datetime
from typing import Optional

class Sesion:
    # Representa la sesión autenticada que habilita las consultas externas
    def __init__(self, usuario: str, tipo_usuario: str):
        self.usuario = usuario
        self.tipo_usuario = tipo_usuario

def _exigir_sesion(sesion: Optional[Sesion]) -> None:
    # Impide consumir APIs cuando no existe una sesión autenticada
    if not isinstance(sesion, Sesion):
        raise PermissionError("Se requiere una sesión autenticada.")

def _validar_ciudad(ciudad: str) -> str:
    #Valida el texto de ciudad antes de enviarlo al servicio geográfico
    ciudad = ciudad.strip()
    if not ciudad or len(ciudad) > 100 or not re.fullmatch(r"[A-Za-zÀ-ÿ0-9 .,'-]+", ciudad):
        raise ValueError("Ciudad inválida.")
    return ciudad

def _validar_moneda(moneda: str) -> str:
    # Normaliza y valida un código de moneda de tres letras
    moneda = moneda.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", moneda):
        raise ValueError("Moneda inválida.")
    return moneda

def consultar_clima(sesion: Optional[Sesion], ciudad: str) -> Optional[dict]:
    # Obtiene el clima actual usando geocodificación y Open-Meteo
    _exigir_sesion(sesion)
    ciudad = _validar_ciudad(ciudad)

    # Primero se convierten el nombre de la ciudad en coordenadas
    try:
        geocodificacion = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": ciudad,
                "count": 1,
                "language": "es",
                "format": "json",
            },
            timeout=10,
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("El servicio tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No fue posible conectar con el servicio.")
    except requests.exceptions.RequestException:
        raise RuntimeError("No fue posible consultar el servicio.")

    if geocodificacion.status_code != 200:
        raise RuntimeError("El servicio del clima no está disponible.")

    # Luego se consultan las condiciones actuales de esas coordenadas
    try:
        lugares = geocodificacion.json().get("results", [])
        latitud = lugares[0]["latitude"]
        longitud = lugares[0]["longitude"]
        nombre = lugares[0]["name"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise RuntimeError("No se encontró la ciudad indicada.")

    try:
        respuesta = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitud,
                "longitude": longitud,
                "current": "temperature_2m,weather_code",
                "timezone": "auto",
            },
            timeout=10,
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("El servicio tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No fue posible conectar con el servicio.")
    except requests.exceptions.RequestException:
        raise RuntimeError("No fue posible consultar el servicio.")

    if respuesta.status_code != 200:
        raise RuntimeError("El servicio del clima no está disponible.")

    try:
        actual = respuesta.json()["current"]
        return {
            "ciudad": nombre,
            "temperatura": actual["temperature_2m"],
            "codigo_clima": actual["weather_code"],
        }
    except (ValueError, KeyError, IndexError, TypeError):
        raise RuntimeError("El servicio devolvió una respuesta inválida.")

def consultar_tipo_cambio(sesion: Optional[Sesion], moneda: str) -> Optional[dict]:
    # Obtiene USD/CLP y calcula el inverso cuando la moneda base es CLP
    _exigir_sesion(sesion)
    moneda = _validar_moneda(moneda)
    if moneda not in {"USD", "CLP"}:
        raise ValueError("Solo se admite USD o CLP en este indicador.")

    try:
        respuesta = requests.get(
            f"https://indicadores.cl/api/v1/historico/dolar/{datetime.now().year}.json",
            timeout=10,
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("El servicio tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No fue posible conectar con el servicio.")
    except requests.exceptions.RequestException:
        raise RuntimeError("No fue posible consultar el servicio.")

    if respuesta.status_code != 200:
        raise RuntimeError("El servicio económico no está disponible.")

    try:
        serie = respuesta.json()["serie"]
        if not serie:
            raise RuntimeError("El servicio económico no está disponible.")
        ultimo = serie[-1]
        valor_usd_clp = float(ultimo["valor"])
        return {
            "moneda": moneda,
            "fecha": ultimo["fecha"],
            "valor": (
                valor_usd_clp
                if moneda == "USD"
                else 1 / valor_usd_clp
            ),
            "moneda_destino": "CLP" if moneda == "USD" else "USD",
        }
    except (ValueError, KeyError, TypeError):
        raise RuntimeError("El servicio devolvió una respuesta inválida.")
