from enum import Enum

class UserRole(str, Enum):
    Administrador = "Administrador"
    Vendedor = "Vendedor"
    Bodega = "Bodega"
    Taller = "Taller"
    Asistente = "Asistente"