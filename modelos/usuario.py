"""Usuario: persona registrada en el sistema, con un rol que define que
puede hacer dentro de la aplicacion."""

from typing import Any, Dict

ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")


class Usuario:

    def __init__(self, identificacion: str, nombre: str, correo: str, contrasena: str, rol: str) -> None:
        self._validar_datos(identificacion, nombre, correo, contrasena, rol)
        self.identificacion: str = identificacion
        self.nombre: str = nombre
        self.correo: str = correo
        self.contrasena: str = contrasena
        self.rol: str = rol

    @staticmethod
    def _validar_datos(identificacion: str, nombre: str, correo: str, contrasena: str, rol: str) -> None:
        if not identificacion or not str(identificacion).strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo or "@" not in correo:
            raise ValueError("El correo del usuario no es válido.")
        if not contrasena or not str(contrasena).strip():
            raise ValueError("La contraseña del usuario no puede estar vacía.")
        if rol not in ROLES_VALIDOS:
            raise ValueError(f"El rol debe ser uno de: {', '.join(ROLES_VALIDOS)}.")

    def mostrar_informacion(self) -> str:
        return (
            f"Identificación: {self.identificacion} | Nombre: {self.nombre} | "
            f"Correo: {self.correo} | Rol: {self.rol}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Usuario":
        try:
            # el rol se agrego en una version mas reciente del sistema; si
            # un registro guardado antes no lo trae, se usa Cliente por
            # defecto en lugar de descartar al usuario completo (eso era
            # lo que antes hacia que el login fallara sin motivo claro)
            rol = str(datos.get("rol", "Cliente"))
            return cls(
                identificacion=str(datos["identificacion"]),
                nombre=str(datos["nombre"]),
                correo=str(datos["correo"]),
                contrasena=str(datos["contrasena"]),
                rol=rol,
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de usuario no contiene la clave requerida: {error}"
            ) from error
