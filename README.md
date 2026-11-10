## Para ejecutar requerimientos.txt
* py -m pip install -r requerimientos.txt

## Para actualización:
* py -m pip install --upgrade pip
* py -m pip install --upgrade mysql-connector-python

## Seguridad y servicios externos

La aplicación solicita autenticación antes de mostrar el menú. Las
contraseñas se comparan mediante `bcrypt` y nunca se guardan en texto plano.
Las consultas usan servicios públicos sin API Key: Open-Meteo para clima e
Indicadores.cl para el dólar observado. Las peticiones externas usan
`requests`, tiempo de espera y mensajes de error genéricos.

## Roles de usuario

La aplicación reconoce los tipos `Administrador` y `Empleado`. El
Administrador puede acceder a todas las gestiones, mientras que el Empleado
puede registrar y consultar tiempos, consultar asignaciones y usar los
servicios externos. Las operaciones de empleados, departamentos, proyectos y
los cambios de asignaciones están restringidos al Administrador.

La primera cuenta registrada se crea como `Administrador`, permitiendo iniciar
el sistema sin usuarios preconfigurados. Las cuentas siguientes se crean como
`Empleado`; un Administrador puede gestionar las cuentas administrativas desde
la base de datos si se requiere otra.
