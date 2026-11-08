## Para ejecutar requerimientos.txt
* py -m pip install -r requerimientos.txt

## Para actualización:
* py -m pip install --upgrade pip
* py -m pip install --upgrade mysql-connector-python

## Seguridad y servicios externos

Antes de ejecutar las consultas de clima y tipo de cambio, configure las
credenciales como variables de entorno. No las agregue al código ni al
repositorio:

```powershell
$env:OPENWEATHER_API_KEY = "su_api_key"
$env:EXCHANGE_RATE_API_KEY = "su_api_key"
python .\main.py
```

La aplicación solicita autenticación antes de mostrar el menú. Las
contraseñas se comparan mediante bcrypt y nunca se guardan en texto plano.
Las peticiones externas usan `requests`, tiempo de espera y mensajes de error
genéricos.