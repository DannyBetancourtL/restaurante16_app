"""Venta: relaciona un usuario con un producto vendido, en una fecha dada."""

from typing import Any, Dict


class Venta:

    def __init__(self, identificacion_usuario: str, codigo_producto: str, cantidad: int, fecha: str) -> None:
        self._validar_datos(identificacion_usuario, codigo_producto, cantidad, fecha)
        self.identificacion_usuario: str = identificacion_usuario
        self.codigo_producto: str = codigo_producto
        self.cantidad: int = cantidad
        self.fecha: str = fecha

    @staticmethod
    def _validar_datos(identificacion_usuario: str, codigo_producto: str, cantidad: int, fecha: str) -> None:
        if not identificacion_usuario or not str(identificacion_usuario).strip():
            raise ValueError("La venta debe tener un usuario.")
        if not codigo_producto or not str(codigo_producto).strip():
            raise ValueError("La venta debe tener un producto.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser un número entero mayor que cero.")
        if not fecha or not str(fecha).strip():
            raise ValueError("La venta debe tener una fecha.")

    def mostrar_informacion(self, nombre_usuario: str = "", nombre_producto: str = "") -> str:
        usuario = f"{self.identificacion_usuario} ({nombre_usuario})" if nombre_usuario else self.identificacion_usuario
        producto = f"{self.codigo_producto} ({nombre_producto})" if nombre_producto else self.codigo_producto
        return f"Fecha: {self.fecha} | Usuario: {usuario} | Producto: {producto} | Cantidad: {self.cantidad}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Venta":
        try:
            return cls(
                identificacion_usuario=str(datos["identificacion_usuario"]),
                codigo_producto=str(datos["codigo_producto"]),
                cantidad=int(datos["cantidad"]),
                fecha=str(datos["fecha"]),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de venta no contiene la clave requerida: {error}"
            ) from error
