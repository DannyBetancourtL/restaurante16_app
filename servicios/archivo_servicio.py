"""ArchivoServicio: lectura de productos, usuarios y ventas desde archivos JSON."""

import json
from pathlib import Path
from typing import Any, List, Type, TypeVar

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

T = TypeVar("T")


class ArchivoServicio:
    """Se encarga solo de leer los datos locales, no conoce reglas de negocio."""

    def __init__(
        self,
        ruta_productos: str = "datos/productos.json",
        ruta_usuarios: str = "datos/usuarios.json",
        ruta_ventas: str = "datos/ventas.json",
    ) -> None:
        self.ruta_productos: Path = Path(ruta_productos)
        self.ruta_usuarios: Path = Path(ruta_usuarios)
        self.ruta_ventas: Path = Path(ruta_ventas)

    def _cargar_lista(self, ruta_archivo: Path, clase: Type[T]) -> List[T]:
        """Lee un JSON y reconstruye la lista de objetos con clase.from_dict()."""
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido: Any = json.load(archivo)
        except FileNotFoundError:
            print(f"Aviso: no se encontró '{ruta_archivo}'. Se iniciará con una colección vacía.")
            return []
        except json.JSONDecodeError:
            print(f"Aviso: el archivo '{ruta_archivo}' no contiene un JSON válido. Se iniciará con una colección vacía.")
            return []
        except PermissionError:
            print(f"Error: no se tienen permisos para leer '{ruta_archivo}'. Se iniciará con una colección vacía.")
            return []

        if not isinstance(contenido, list):
            print(f"Aviso: el contenido de '{ruta_archivo}' no tiene el formato esperado. Se ignorará.")
            return []

        objetos: List[T] = []
        for indice, registro in enumerate(contenido, start=1):
            try:
                if not isinstance(registro, dict):
                    raise ValueError("el registro no es un objeto JSON válido")
                objetos.append(clase.from_dict(registro))  # type: ignore[attr-defined]
            except KeyError as error:
                print(f"Aviso: se omitió el registro #{indice} de '{ruta_archivo}' ({error}).")
            except ValueError as error:
                print(f"Aviso: se omitió el registro #{indice} de '{ruta_archivo}' ({error}).")

        return objetos

    def cargar_productos(self) -> List[Producto]:
        return self._cargar_lista(self.ruta_productos, Producto)

    def cargar_usuarios(self) -> List[Usuario]:
        return self._cargar_lista(self.ruta_usuarios, Usuario)

    def cargar_ventas(self) -> List[Venta]:
        return self._cargar_lista(self.ruta_ventas, Venta)

    def _guardar_lista(self, ruta_archivo: Path, objetos: List[Any]) -> bool:
        datos = [objeto.to_dict() for objeto in objetos]
        try:
            ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            return True
        except PermissionError:
            print(f"Error: no se tienen permisos para escribir en '{ruta_archivo}'.")
            return False
        except OSError as error:
            print(f"Error al guardar '{ruta_archivo}': {error}")
            return False

    def guardar_productos(self, productos: List[Producto]) -> bool:
        return self._guardar_lista(self.ruta_productos, productos)

    def guardar_usuarios(self, usuarios: List[Usuario]) -> bool:
        return self._guardar_lista(self.ruta_usuarios, usuarios)

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        return self._guardar_lista(self.ruta_ventas, ventas)
