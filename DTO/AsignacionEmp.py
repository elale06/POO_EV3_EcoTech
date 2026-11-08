class AsignacionEmp:
    def __init__(self, empleado_id, proyecto_id, fecha_asignacion, rol, id=None):
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha_asignacion = fecha_asignacion
        self.rol = rol
        self.id = id