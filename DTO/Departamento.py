class Departamento:
    def __init__(self, nombre, gerente_empleado_id, descripcion, id=None):
        self.nombre = nombre
        self.gerente_empleado_id = gerente_empleado_id
        self.descripcion = descripcion
        self.id = id