from DTO.Persona import Persona

class Empleado(Persona):
    def __init__(self, run, nombre, direccion, telefono, correo, fecha_inicio, salario, departamento_id, id=None):
        super().__init__(run, nombre, direccion, telefono, correo)
        self.fecha_inicio = fecha_inicio
        self.salario = salario
        self.departamento_id = departamento_id
        self.id = id