class Empleado:
    def __init__(self, run, nombre, direccion, telefono, correo, fecha_inicio, salario, departamento_id, id=None):
        self.run = run
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_inicio = fecha_inicio
        self.salario = salario
        self.departamento_id = departamento_id
        self.id = id