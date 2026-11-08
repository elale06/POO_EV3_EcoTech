## Para ejecutar requerimientos.txt
* py -m pip install -r requerimientos.txt

## Para actualización:
* py -m pip install --upgrade pip
* py -m pip install --upgrade mysql-connector-python

## Seguridad y servicios externos

La aplicación solicita autenticación antes de mostrar el menú. Las
contraseñas se comparan mediante bcrypt y nunca se guardan en texto plano.
Las consultas usan servicios públicos sin API Key: Open-Meteo para clima e
Indicadores.cl para el dólar observado. Las peticiones externas usan
`requests`, tiempo de espera y mensajes de error genéricos.

admin
4dmin.2026