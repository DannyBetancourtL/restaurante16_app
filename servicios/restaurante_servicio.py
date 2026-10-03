"""RestauranteServicio: aqui vive toda la logica del negocio. Las vistas
piden lo que necesitan a traves de estos metodos, nunca leen ni escriben
los archivos JSON por su cuenta."""

from datetime import datetime
from typing import List, Optional

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:

    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self.archivo_servicio = archivo_servicio
        self._productos: List[Producto] = self.archivo_servicio.cargar_productos()
        self._usuarios: List[Usuario] = self.archivo_servicio.cargar_usuarios()
        self._ventas: List[Venta] = self.archivo_servicio.cargar_ventas()
        self._contador_producto: int = self._calcular_contador_inicial()

    def _calcular_contador_inicial(self) -> int:
        mayor = 0
        for producto in self._productos:
            try:
                numero = int(producto.codigo)
                if numero > mayor:
                    mayor = numero
            except ValueError:
                pass
        return mayor

    # ------------------------- acceso -------------------------

    def validar_acceso(self, identificacion: str, contrasena: str) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion and usuario.contrasena == contrasena:
                return usuario
        return None

    # ------------------------- usuarios -------------------------

    def listar_usuarios(self) -> List[str]:
        return [usuario.mostrar_informacion() for usuario in self._usuarios]

    def obtener_usuarios(self) -> List[Usuario]:
        return list(self._usuarios)

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def registrar_usuario(self, identificacion: str, nombre: str, correo: str, contrasena: str, rol: str) -> Usuario:
        if self.buscar_usuario(identificacion) is not None:
            raise ValueError(f"Ya existe un usuario con la identificación {identificacion}.")
        if rol == "Administrador":
            raise ValueError("No se pueden registrar nuevas cuentas de administrador desde este formulario.")
        usuario = Usuario(identificacion, nombre, correo, contrasena, rol)
        self._usuarios.append(usuario)
        self._guardar_usuarios()
        return usuario

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str,
        identificacion_sesion: str,
    ) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False

        if identificacion == identificacion_sesion and rol != usuario.rol:
            raise ValueError("No puede cambiar su propio rol mientras está autenticado.")

        Usuario._validar_datos(identificacion, nombre, correo, contrasena, rol)
        usuario.nombre = nombre
        usuario.correo = correo
        usuario.contrasena = contrasena
        usuario.rol = rol
        self._guardar_usuarios()
        return True

    def eliminar_usuario(self, identificacion: str, identificacion_sesion: str) -> bool:
        if identificacion == identificacion_sesion:
            raise ValueError("No puede eliminar la cuenta con la que inició sesión.")

        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        self._usuarios.remove(usuario)
        self._guardar_usuarios()
        return True

    def _guardar_usuarios(self) -> None:
        self.archivo_servicio.guardar_usuarios(self._usuarios)

    # ------------------------- productos -------------------------

    def listar_productos(self) -> List[str]:
        return [producto.mostrar_informacion() for producto in self._productos]

    def obtener_productos(self) -> List[Producto]:
        return list(self._productos)

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def consultar_cantidad_producto(self, codigo: str) -> Optional[int]:
        producto = self.buscar_producto(codigo)
        return producto.stock if producto is not None else None

    def registrar_producto(
        self, nombre: str, categoria: str, precio: float, disponible: bool, stock: int
    ) -> Producto:
        self._contador_producto += 1
        codigo = str(self._contador_producto)
        producto = Producto(codigo, nombre, categoria, precio, disponible, stock)
        self._productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        disponible: bool,
        stock: int,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

        Producto._validar_datos(codigo, nombre, categoria, precio, stock)
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.disponible = disponible
        producto.stock = stock
        self._guardar_productos()
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        self._guardar_productos()
        return True

    def _guardar_productos(self) -> None:
        self.archivo_servicio.guardar_productos(self._productos)

    # ------------------------- ventas -------------------------

    def listar_ventas(self) -> List[str]:
        ventas_info = []
        for venta in self._ventas:
            usuario = self.buscar_usuario(venta.identificacion_usuario)
            producto = self.buscar_producto(venta.codigo_producto)
            nombre_usuario = usuario.nombre if usuario is not None else ""
            nombre_producto = producto.nombre if producto is not None else ""
            ventas_info.append(venta.mostrar_informacion(nombre_usuario, nombre_producto))
        return ventas_info

    def obtener_ventas(self) -> List[Venta]:
        return list(self._ventas)

    def registrar_venta(self, identificacion_usuario: str, codigo_producto: str, cantidad: int) -> Venta:
        """Registra la venta de un producto a un usuario existente.

        Valida que el usuario exista, que el producto exista, que la
        cantidad sea valida y que haya stock suficiente. Si todo esta
        correcto, descuenta el stock, guarda la venta con la fecha
        actual y persiste tanto productos.json como ventas.json.
        """
        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            raise ValueError(f"No existe un usuario con identificación {identificacion_usuario}.")

        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            raise ValueError(f"No existe un producto con código {codigo_producto}.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if cantidad > producto.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}.")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        venta = Venta(identificacion_usuario, codigo_producto, cantidad, fecha)

        producto.stock -= cantidad
        self._ventas.append(venta)
        self._guardar_productos()
        self._guardar_ventas()
        return venta

    def _guardar_ventas(self) -> None:
        self.archivo_servicio.guardar_ventas(self._ventas)
