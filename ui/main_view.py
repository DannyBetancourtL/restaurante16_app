"""MainView: panel principal tras el acceso. Desde aqui se maneja
Productos, Usuarios y un proceso sencillo de Ventas."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio
from ui.fondo_marca_agua import FondoMarcaAgua

RUTA_LOGO = Path("assets/logo_sabor_lojano.jpg")


class MainView(tk.Frame):

    def __init__(
        self,
        parent: tk.Widget,
        restaurante_servicio: RestauranteServicio,
        usuario: Usuario,
        on_cerrar_sesion,
    ):
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.usuario = usuario
        self.on_cerrar_sesion = on_cerrar_sesion

        self._aplicar_estilo_pastel()
        self._construir_encabezado()
        self._construir_cuerpo()

        self.mostrar_productos()

    def _aplicar_estilo_pastel(self) -> None:
        """Deja los componentes ttk (botones, tabla, pestañas de formulario)
        con los mismos tonos suaves que el resto de la ventana."""
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("TButton", background="#6FA8DC", foreground="white", padding=6, relief="flat")
        estilo.map("TButton", background=[("active", "#5C94C7")])

        estilo.configure("TLabelframe", background="#EAF4F3", bordercolor="#BFE3DF")
        estilo.configure("TLabelframe.Label", background="#EAF4F3", foreground="#2F6F6B", font=("Segoe UI", 9, "bold"))

        estilo.configure("Treeview", background="white", fieldbackground="white", rowheight=24)
        estilo.configure("Treeview.Heading", background="#AEDCD9", foreground="#2F6F6B", font=("Segoe UI", 9, "bold"))
        estilo.map("Treeview", background=[("selected", "#BFE3DF")], foreground=[("selected", "#2F6F6B")])

        estilo.configure("TSeparator", background="#CDEAE7")
        estilo.configure("TLabel", background="#EAF4F3", foreground="#4A4A4A")
        estilo.configure("TCombobox", fieldbackground="white")
        estilo.configure("TCheckbutton", background="#EAF4F3")

    # ---------------- estructura general ----------------

    def _construir_encabezado(self) -> None:
        encabezado = tk.Frame(self, bg="#AEDCD9")
        encabezado.pack(fill="x")

        self._mostrar_logo_encabezado(encabezado)

        tk.Label(
            encabezado,
            text="Restaurante Sabor Lojano",
            bg="#AEDCD9",
            fg="#2F6F6B",
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left", padx=(5, 15), pady=10)

        tk.Label(
            encabezado,
            text=f"Sesión: {self.usuario.nombre}",
            bg="#AEDCD9",
            fg="#2F6F6B",
            font=("Segoe UI", 9),
        ).pack(side="right", padx=15)

    def _mostrar_logo_encabezado(self, encabezado: tk.Widget) -> None:
        if not RUTA_LOGO.exists():
            return
        try:
            from PIL import Image, ImageTk

            imagen = Image.open(RUTA_LOGO)
            imagen.thumbnail((40, 40))
            self._logo_encabezado = ImageTk.PhotoImage(imagen)
            tk.Label(encabezado, image=self._logo_encabezado, bg="#AEDCD9").pack(
                side="left", padx=(15, 0), pady=10
            )
        except Exception:
            pass

    def _cargar_icono_menu(self, nombre: str):
        ruta = Path(f"assets/icons/{nombre}.png")
        if not ruta.exists():
            return None
        try:
            from PIL import Image, ImageTk

            imagen = Image.open(ruta)
            imagen.thumbnail((20, 20))
            icono = ImageTk.PhotoImage(imagen)
            self._iconos_menu[nombre] = icono  # se guarda la referencia, si no se pierde la imagen
            return icono
        except Exception:
            return None

    def _construir_cuerpo(self) -> None:
        cuerpo = tk.Frame(self)
        cuerpo.pack(fill="both", expand=True)

        self.panel_navegacion = tk.Frame(cuerpo, bg="#F4EFE6", width=160)
        self.panel_navegacion.pack(side="left", fill="y")
        self.panel_navegacion.pack_propagate(False)

        tk.Label(self.panel_navegacion, text="Secciones", bg="#F4EFE6", font=("Segoe UI", 10, "bold")).pack(
            pady=(15, 5), padx=10, anchor="w"
        )

        self._iconos_menu = {}

        ttk.Button(
            self.panel_navegacion, text=" Productos", command=self.mostrar_productos,
            image=self._cargar_icono_menu("productos"), compound="left",
        ).pack(fill="x", padx=10, pady=4)

        if self.usuario.rol == "Administrador":
            ttk.Button(
                self.panel_navegacion, text=" Usuarios", command=self.mostrar_usuarios,
                image=self._cargar_icono_menu("usuarios"), compound="left",
            ).pack(fill="x", padx=10, pady=4)

        ttk.Button(
            self.panel_navegacion, text=" Ventas", command=self.mostrar_ventas,
            image=self._cargar_icono_menu("ventas"), compound="left",
        ).pack(fill="x", padx=10, pady=4)

        ttk.Separator(self.panel_navegacion, orient="horizontal").pack(fill="x", padx=10, pady=15)

        ttk.Button(
            self.panel_navegacion, text=" Cerrar sesión", command=self.on_cerrar_sesion,
            image=self._cargar_icono_menu("salir"), compound="left",
        ).pack(fill="x", padx=10, pady=4)

        self.fondo_contenido = FondoMarcaAgua(cuerpo)
        self.fondo_contenido.pack(side="left", fill="both", expand=True)

        self.panel_contenido = tk.Frame(self.fondo_contenido, bg="#EAF4F3")
        self.fondo_contenido.colocar_contenido(self.panel_contenido, anclaje="n")

    def _limpiar_contenido(self) -> None:
        for hijo in self.panel_contenido.winfo_children():
            hijo.destroy()

    # ---------------- seccion usuarios ----------------

    def mostrar_usuarios(self) -> None:
        self._limpiar_contenido()
        contenedor = tk.Frame(self.panel_contenido, bg="#EAF4F3")
        contenedor.pack(padx=15, pady=15)

        tk.Label(contenedor, text="Usuarios del sistema", font=("Segoe UI", 12, "bold"), bg="#EAF4F3").pack(
            anchor="w", pady=(0, 10)
        )
        tk.Label(
            contenedor,
            text="Seleccione una fila de la tabla para cargarla en el formulario. Enter registra, Escape limpia.",
            bg="#EAF4F3", fg="#555555",
        ).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(contenedor, text="Datos del usuario")
        formulario.pack(fill="x", pady=(0, 10))

        self.var_usr_identificacion = tk.StringVar()
        self.var_usr_nombre = tk.StringVar()
        self.var_usr_correo = tk.StringVar()
        self.var_usr_contrasena = tk.StringVar()
        self.var_usr_rol = tk.StringVar()

        ttk.Label(formulario, text="Identificación:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_identificacion = ttk.Entry(formulario, textvariable=self.var_usr_identificacion, width=20)
        entry_identificacion.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_nombre = ttk.Entry(formulario, textvariable=self.var_usr_nombre, width=25)
        entry_nombre.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Correo:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        entry_correo = ttk.Entry(formulario, textvariable=self.var_usr_correo, width=25)
        entry_correo.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Contraseña:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        entry_contrasena = ttk.Entry(formulario, textvariable=self.var_usr_contrasena, width=20)
        entry_contrasena.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Rol:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        combo_rol = ttk.Combobox(
            formulario, textvariable=self.var_usr_rol, width=18, state="readonly",
            values=("Empleado", "Cliente", "Administrador"),
        )
        combo_rol.current(0)
        combo_rol.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        self.mensaje_usuarios = tk.Label(contenedor, text="", fg="#D98880", bg="#EAF4F3")
        self.mensaje_usuarios.pack(anchor="w")

        acciones = tk.Frame(contenedor, bg="#EAF4F3")
        acciones.pack(fill="x", pady=8)

        ttk.Button(acciones, text="Registrar", command=self._registrar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Actualizar", command=self._actualizar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_formulario_usuario).pack(side="left", padx=3)

        self.tabla_usuarios = ttk.Treeview(
            contenedor,
            columns=("identificacion", "nombre", "correo", "rol"),
            show="headings",
            height=10,
        )
        for clave, texto, ancho in (
            ("identificacion", "Identificación", 110),
            ("nombre", "Nombre", 160),
            ("correo", "Correo", 170),
            ("rol", "Rol", 100),
        ):
            self.tabla_usuarios.heading(clave, text=texto)
            self.tabla_usuarios.column(clave, width=ancho, anchor="center")
        self.tabla_usuarios.pack(pady=(10, 0))

        # eventos: la tabla carga el formulario al seleccionar una fila,
        # el teclado confirma o cancela, y el combo avisa el cambio de rol
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self._al_seleccionar_fila_usuario)
        for campo in (entry_identificacion, entry_nombre, entry_correo, entry_contrasena, combo_rol):
            campo.bind("<Return>", self._al_presionar_enter)
            campo.bind("<Escape>", self._al_presionar_escape)
        combo_rol.bind("<<ComboboxSelected>>", self._al_cambiar_rol)

        self._refrescar_tabla_usuarios()

    def _refrescar_tabla_usuarios(self) -> None:
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)
        for usuario in self.restaurante_servicio.obtener_usuarios():
            # no se incluye la contraseña en la tabla, solo lo que hace
            # falta para identificar al usuario de un vistazo
            self.tabla_usuarios.insert(
                "", "end",
                values=(usuario.identificacion, usuario.nombre, usuario.correo, usuario.rol),
            )

    def _limpiar_formulario_usuario(self) -> None:
        self.var_usr_identificacion.set("")
        self.var_usr_nombre.set("")
        self.var_usr_correo.set("")
        self.var_usr_contrasena.set("")
        self.var_usr_rol.set("Empleado")
        self.mensaje_usuarios.config(text="")
        for fila in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(fila)

    def _al_seleccionar_fila_usuario(self, event: tk.Event) -> None:
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        identificacion = self.tabla_usuarios.item(seleccion[0], "values")[0]
        usuario = self.restaurante_servicio.buscar_usuario(str(identificacion))
        if usuario is None:
            return

        self.var_usr_identificacion.set(usuario.identificacion)
        self.var_usr_nombre.set(usuario.nombre)
        self.var_usr_correo.set(usuario.correo)
        self.var_usr_contrasena.set(usuario.contrasena)
        self.var_usr_rol.set(usuario.rol)
        self.mensaje_usuarios.config(text="Usuario cargado desde la tabla.", fg="#5FA88A")

    def _al_presionar_enter(self, event: tk.Event) -> None:
        # Enter reutiliza el mismo registro que usa el boton, no repite logica
        self._registrar_usuario()

    def _al_presionar_escape(self, event: tk.Event) -> None:
        # Escape reutiliza el mismo limpiar que usa el boton
        self._limpiar_formulario_usuario()

    def _al_cambiar_rol(self, event: tk.Event) -> None:
        self.mensaje_usuarios.config(text=f"Rol seleccionado: {self.var_usr_rol.get()}.", fg="#555555")

    def _registrar_usuario(self) -> None:
        identificacion = self.var_usr_identificacion.get().strip()
        nombre = self.var_usr_nombre.get().strip()
        correo = self.var_usr_correo.get().strip()
        contrasena = self.var_usr_contrasena.get().strip()
        rol = self.var_usr_rol.get().strip()

        try:
            self.restaurante_servicio.registrar_usuario(identificacion, nombre, correo, contrasena, rol)
        except ValueError as error:
            self.mensaje_usuarios.config(text=str(error), fg="#D98880")
            return

        self.mensaje_usuarios.config(text="Usuario registrado.", fg="#5FA88A")
        self._limpiar_formulario_usuario()
        self._refrescar_tabla_usuarios()

    def _actualizar_usuario(self) -> None:
        identificacion = self.var_usr_identificacion.get().strip()
        if not identificacion:
            self.mensaje_usuarios.config(text="Seleccione primero un usuario en la tabla.", fg="#D98880")
            return

        try:
            actualizado = self.restaurante_servicio.actualizar_usuario(
                identificacion,
                self.var_usr_nombre.get().strip(),
                self.var_usr_correo.get().strip(),
                self.var_usr_contrasena.get().strip(),
                self.var_usr_rol.get().strip(),
                self.usuario.identificacion,
            )
        except ValueError as error:
            self.mensaje_usuarios.config(text=str(error), fg="#D98880")
            return

        if not actualizado:
            self.mensaje_usuarios.config(text=f"No existe un usuario con identificación {identificacion}.", fg="#D98880")
            return

        self.mensaje_usuarios.config(text="Usuario actualizado.", fg="#5FA88A")
        self._refrescar_tabla_usuarios()

    def _eliminar_usuario(self) -> None:
        identificacion = self.var_usr_identificacion.get().strip()
        usuario = self.restaurante_servicio.buscar_usuario(identificacion)
        if usuario is None:
            self.mensaje_usuarios.config(text=f"No existe un usuario con identificación {identificacion}.", fg="#D98880")
            return

        confirmar = messagebox.askyesno("Eliminar usuario", f"¿Eliminar al usuario {usuario.nombre}?")
        if not confirmar:
            return

        try:
            self.restaurante_servicio.eliminar_usuario(identificacion, self.usuario.identificacion)
        except ValueError as error:
            self.mensaje_usuarios.config(text=str(error), fg="#D98880")
            return

        self.mensaje_usuarios.config(text="Usuario eliminado.", fg="#5FA88A")
        self._limpiar_formulario_usuario()
        self._refrescar_tabla_usuarios()

    # ---------------- seccion ventas ----------------

    def mostrar_ventas(self) -> None:
        self._limpiar_contenido()
        contenedor = tk.Frame(self.panel_contenido, bg="#EAF4F3")
        contenedor.pack(padx=15, pady=15)

        tk.Label(contenedor, text="Registro de ventas", font=("Segoe UI", 12, "bold"), bg="#EAF4F3").pack(
            anchor="w", pady=(0, 10)
        )

        formulario = ttk.LabelFrame(contenedor, text="Nueva venta")
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_usuario_venta = ttk.Combobox(formulario, width=35, state="readonly")
        self.combo_usuario_venta.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Producto:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_producto_venta = ttk.Combobox(formulario, width=35, state="readonly")
        self.combo_producto_venta.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Cantidad:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.var_cantidad_venta = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_cantidad_venta, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(formulario, text="Registrar venta", command=self._registrar_venta).grid(
            row=3, column=1, sticky="w", padx=5, pady=8
        )

        self.mensaje_ventas = tk.Label(contenedor, text="", fg="#D98880", bg="#EAF4F3")
        self.mensaje_ventas.pack(anchor="w")

        self.tabla_ventas = ttk.Treeview(
            contenedor,
            columns=("fecha", "usuario", "producto", "cantidad", "subtotal"),
            show="headings",
            height=8,
        )
        for clave, texto, ancho in (
            ("fecha", "Fecha", 120),
            ("usuario", "Usuario", 140),
            ("producto", "Producto", 140),
            ("cantidad", "Cantidad", 70),
            ("subtotal", "Subtotal", 80),
        ):
            self.tabla_ventas.heading(clave, text=texto)
            self.tabla_ventas.column(clave, width=ancho, anchor="center")
        self.tabla_ventas.pack(pady=(10, 5))

        self.label_total_ventas = tk.Label(
            contenedor, text="", font=("Segoe UI", 10, "bold"), bg="#EAF4F3"
        )
        self.label_total_ventas.pack(anchor="e")

        self._cargar_usuarios_combo()
        self._cargar_productos_combo()
        self._refrescar_tabla_ventas()

    def _cargar_usuarios_combo(self) -> None:
        opciones = []
        for usuario in self.restaurante_servicio.obtener_usuarios():
            opciones.append(f"{usuario.identificacion} - {usuario.nombre}")
        self.combo_usuario_venta["values"] = opciones
        if opciones:
            self.combo_usuario_venta.current(0)

    def _cargar_productos_combo(self) -> None:
        opciones = []
        for producto in self.restaurante_servicio.obtener_productos():
            opciones.append(f"{producto.codigo} - {producto.nombre} (stock: {producto.stock})")
        self.combo_producto_venta["values"] = opciones
        if opciones:
            self.combo_producto_venta.current(0)

    def _refrescar_tabla_ventas(self) -> None:
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)

        total = 0.0
        for venta in self.restaurante_servicio.obtener_ventas():
            usuario = self.restaurante_servicio.buscar_usuario(venta.identificacion_usuario)
            producto = self.restaurante_servicio.buscar_producto(venta.codigo_producto)
            nombre_usuario = usuario.nombre if usuario is not None else venta.identificacion_usuario
            nombre_producto = producto.nombre if producto is not None else venta.codigo_producto
            precio = producto.precio if producto is not None else 0.0
            subtotal = precio * venta.cantidad
            total += subtotal
            self.tabla_ventas.insert(
                "", "end",
                values=(venta.fecha, nombre_usuario, nombre_producto, venta.cantidad, f"{subtotal:.2f}"),
            )

        self.label_total_ventas.config(text=f"Total vendido: ${total:.2f}")

    def _registrar_venta(self) -> None:
        seleccion_usuario = self.combo_usuario_venta.get()
        if not seleccion_usuario:
            self.mensaje_ventas.config(text="Seleccione un usuario.", fg="#D98880")
            return
        identificacion_usuario = seleccion_usuario.split(" - ")[0]

        seleccion_producto = self.combo_producto_venta.get()
        if not seleccion_producto:
            self.mensaje_ventas.config(text="Seleccione un producto.", fg="#D98880")
            return
        codigo_producto = seleccion_producto.split(" - ")[0]

        try:
            cantidad = int(self.var_cantidad_venta.get())
        except ValueError:
            self.mensaje_ventas.config(text="La cantidad debe ser un número entero.", fg="#D98880")
            return

        try:
            venta = self.restaurante_servicio.registrar_venta(identificacion_usuario, codigo_producto, cantidad)
        except ValueError as error:
            self.mensaje_ventas.config(text=str(error), fg="#D98880")
            return

        producto = self.restaurante_servicio.buscar_producto(venta.codigo_producto)
        self.mensaje_ventas.config(
            text=f"Venta registrada. Stock restante: {producto.stock}.", fg="#5FA88A"
        )
        self.var_cantidad_venta.set("")
        self._cargar_productos_combo()
        self._refrescar_tabla_ventas()

    # ---------------- seccion productos ----------------

    def mostrar_productos(self) -> None:
        self._limpiar_contenido()
        contenedor = tk.Frame(self.panel_contenido, bg="#EAF4F3")
        contenedor.pack(padx=15, pady=15)

        tk.Label(contenedor, text="Gestión de productos", font=("Segoe UI", 12, "bold"), bg="#EAF4F3").pack(
            anchor="w", pady=(0, 10)
        )

        formulario = ttk.LabelFrame(contenedor, text="Datos del producto")
        formulario.pack(fill="x", pady=(0, 10))

        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_stock = tk.StringVar()
        self.var_disponible = tk.BooleanVar(value=True)

        ttk.Label(formulario, text="Código:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.var_codigo, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(formulario, text="(vacío al registrar, se genera automáticamente)").grid(
            row=0, column=2, columnspan=2, sticky="w", padx=5
        )

        ttk.Label(formulario, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.var_nombre, width=25).grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Categoría:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.var_categoria, width=25).grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Precio:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.var_precio, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Stock:").grid(row=3, column=2, sticky="e", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.var_stock, width=10).grid(row=3, column=3, sticky="w", padx=5, pady=5)

        ttk.Checkbutton(formulario, text="Disponible", variable=self.var_disponible).grid(
            row=4, column=1, sticky="w", padx=5, pady=5
        )

        self.mensaje_productos = tk.Label(contenedor, text="", fg="#D98880", bg="#EAF4F3")
        self.mensaje_productos.pack(anchor="w")

        acciones = tk.Frame(contenedor, bg="#EAF4F3")
        acciones.pack(fill="x", pady=8)

        ttk.Button(acciones, text="Registrar", command=self._registrar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Cargar", command=self._cargar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Actualizar", command=self._actualizar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_formulario_producto).pack(side="left", padx=3)

        self.tabla_productos = ttk.Treeview(
            contenedor,
            columns=("codigo", "nombre", "categoria", "precio", "disponible", "stock"),
            show="headings",
            height=10,
        )
        for clave, texto, ancho in (
            ("codigo", "Código", 60),
            ("nombre", "Nombre", 160),
            ("categoria", "Categoría", 100),
            ("precio", "Precio", 70),
            ("disponible", "Disponible", 80),
            ("stock", "Stock", 60),
        ):
            self.tabla_productos.heading(clave, text=texto)
            self.tabla_productos.column(clave, width=ancho, anchor="center")
        self.tabla_productos.pack(pady=(10, 0))

        self._refrescar_tabla_productos()

    def _refrescar_tabla_productos(self) -> None:
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)
        for producto in self.restaurante_servicio.obtener_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"{producto.precio:.2f}",
                    "Sí" if producto.disponible else "No",
                    producto.stock,
                ),
            )

    def _limpiar_formulario_producto(self) -> None:
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_categoria.set("")
        self.var_precio.set("")
        self.var_stock.set("")
        self.var_disponible.set(True)
        self.mensaje_productos.config(text="", fg="#D98880")

    def _leer_precio_stock(self):
        try:
            precio = float(self.var_precio.get())
        except ValueError:
            self.mensaje_productos.config(text="El precio debe ser un número.", fg="#D98880")
            return None
        try:
            stock = int(self.var_stock.get())
        except ValueError:
            self.mensaje_productos.config(text="El stock debe ser un número entero.", fg="#D98880")
            return None
        return precio, stock

    def _registrar_producto(self) -> None:
        nombre = self.var_nombre.get().strip()
        categoria = self.var_categoria.get().strip()

        if not nombre or not categoria:
            self.mensaje_productos.config(text="Complete nombre y categoría.", fg="#D98880")
            return

        datos = self._leer_precio_stock()
        if datos is None:
            return
        precio, stock = datos

        try:
            producto = self.restaurante_servicio.registrar_producto(
                nombre, categoria, precio, self.var_disponible.get(), stock
            )
        except ValueError as error:
            self.mensaje_productos.config(text=str(error), fg="#D98880")
            return

        self.mensaje_productos.config(text=f"Producto registrado con código {producto.codigo}.", fg="#5FA88A")
        self._limpiar_formulario_producto()
        self._refrescar_tabla_productos()

    def _cargar_producto(self) -> None:
        codigo = self.var_codigo.get().strip()
        if not codigo:
            self.mensaje_productos.config(text="Escriba un código para cargar.", fg="#D98880")
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self.mensaje_productos.config(text=f"No existe un producto con código {codigo}.", fg="#D98880")
            return

        self.var_nombre.set(producto.nombre)
        self.var_categoria.set(producto.categoria)
        self.var_precio.set(str(producto.precio))
        self.var_stock.set(str(producto.stock))
        self.var_disponible.set(producto.disponible)
        self.mensaje_productos.config(text="Producto cargado. Puede actualizar o eliminar.", fg="#5FA88A")

    def _actualizar_producto(self) -> None:
        codigo = self.var_codigo.get().strip()
        if not codigo:
            self.mensaje_productos.config(text="Cargue primero un producto por su código.", fg="#D98880")
            return

        nombre = self.var_nombre.get().strip()
        categoria = self.var_categoria.get().strip()
        if not nombre or not categoria:
            self.mensaje_productos.config(text="Complete nombre y categoría.", fg="#D98880")
            return

        datos = self._leer_precio_stock()
        if datos is None:
            return
        precio, stock = datos

        try:
            actualizado = self.restaurante_servicio.actualizar_producto(
                codigo, nombre, categoria, precio, self.var_disponible.get(), stock
            )
        except ValueError as error:
            self.mensaje_productos.config(text=str(error), fg="#D98880")
            return

        if not actualizado:
            self.mensaje_productos.config(text=f"No existe un producto con código {codigo}.", fg="#D98880")
            return

        self.mensaje_productos.config(text="Producto actualizado.", fg="#5FA88A")
        self._refrescar_tabla_productos()

    def _eliminar_producto(self) -> None:
        codigo = self.var_codigo.get().strip()
        if not codigo:
            self.mensaje_productos.config(text="Escriba el código del producto a eliminar.", fg="#D98880")
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self.mensaje_productos.config(text=f"No existe un producto con código {codigo}.", fg="#D98880")
            return

        confirmar = messagebox.askyesno(
            "Eliminar producto", f"¿Eliminar el producto '{producto.nombre}' (código {codigo})?"
        )
        if not confirmar:
            return

        self.restaurante_servicio.eliminar_producto(codigo)
        self.mensaje_productos.config(text="Producto eliminado.", fg="#5FA88A")
        self._limpiar_formulario_producto()
        self._refrescar_tabla_productos()
