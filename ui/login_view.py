"""LoginView: pantalla de acceso."""

import tkinter as tk
from pathlib import Path

from servicios.restaurante_servicio import RestauranteServicio
from ui.fondo_marca_agua import FondoMarcaAgua

RUTA_LOGO = Path("assets/logo_sabor_lojano.jpg")

COLOR_FONDO = "#EAF4F3"
COLOR_TARJETA = "#FFFFFF"
COLOR_BORDE = "#CDEAE7"
COLOR_TITULO = "#2F6F6B"
COLOR_TEXTO = "#4A4A4A"
COLOR_LINEA = "#BFE3DF"
COLOR_BOTON = "#6FA8DC"
COLOR_BOTON_HOVER = "#5C94C7"
COLOR_ERROR = "#D98880"


class LoginView(tk.Frame):

    def __init__(self, parent: tk.Widget, restaurante_servicio: RestauranteServicio, on_login_exitoso):
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.on_login_exitoso = on_login_exitoso

        fondo = FondoMarcaAgua(self, color_fondo=COLOR_FONDO)
        fondo.pack(fill="both", expand=True)

        borde = tk.Frame(fondo, bg=COLOR_BORDE, padx=2, pady=2)
        fondo.colocar_contenido(borde, anclaje="center")

        caja = tk.Frame(borde, bg=COLOR_TARJETA, padx=35, pady=25)
        caja.pack()

        self._mostrar_logo(caja)

        tk.Label(caja, text="Restaurante", font=("Segoe UI", 18, "bold"), bg=COLOR_TARJETA, fg=COLOR_TITULO).pack(
            pady=(12, 0)
        )
        tk.Label(caja, text="Sabor Lojano", font=("Segoe UI", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO).pack()
        tk.Label(caja, text="Inicio de sesión", font=("Segoe UI", 10), bg=COLOR_TARJETA, fg="#8a8a8a").pack(
            pady=(2, 18)
        )

        self.entry_identificacion = self._campo(caja, "Identificación")
        self.entry_contrasena = self._campo(caja, "Contraseña", oculto=True)

        self.mensaje = tk.Label(caja, text="", fg=COLOR_ERROR, bg=COLOR_TARJETA, font=("Segoe UI", 9))
        self.mensaje.pack(pady=(4, 10))

        boton = tk.Button(
            caja, text="Iniciar sesión", font=("Segoe UI", 10, "bold"),
            bg=COLOR_BOTON, fg="white", activebackground=COLOR_BOTON_HOVER, activeforeground="white",
            relief="flat", bd=0, padx=20, pady=8, cursor="hand2",
            command=self._intentar_ingresar,
        )
        boton.pack(fill="x", pady=(4, 0))

        self.entry_contrasena.bind("<Return>", lambda evento: self._intentar_ingresar())
        self.entry_identificacion.focus()

    def _campo(self, caja: tk.Widget, etiqueta: str, oculto: bool = False) -> tk.Entry:
        tk.Label(caja, text=etiqueta, font=("Segoe UI", 9, "bold"), bg=COLOR_TARJETA, fg=COLOR_TEXTO).pack(
            anchor="w", pady=(8, 2)
        )
        entrada = tk.Entry(
            caja, width=28, font=("Segoe UI", 11), relief="flat",
            bg=COLOR_TARJETA, fg="#333333", insertbackground="#333333",
            show="•" if oculto else "",
        )
        entrada.pack(fill="x", ipady=4)
        linea = tk.Frame(caja, bg=COLOR_LINEA, height=2)
        linea.pack(fill="x")

        def resaltar(evento):
            linea.config(bg=COLOR_BOTON)

        def apagar(evento):
            linea.config(bg=COLOR_LINEA)

        entrada.bind("<FocusIn>", resaltar)
        entrada.bind("<FocusOut>", apagar)
        return entrada

    def _mostrar_logo(self, caja: tk.Widget) -> None:
        if not RUTA_LOGO.exists():
            return
        try:
            from PIL import Image, ImageTk

            imagen = Image.open(RUTA_LOGO)
            imagen.thumbnail((90, 90))
            self._logo = ImageTk.PhotoImage(imagen)
            tk.Label(caja, image=self._logo, bg=COLOR_TARJETA).pack()
        except Exception:
            pass

    def _intentar_ingresar(self) -> None:
        identificacion = self.entry_identificacion.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not identificacion or not contrasena:
            self.mensaje.config(text="Ingrese identificación y contraseña.")
            return

        usuario = self.restaurante_servicio.validar_acceso(identificacion, contrasena)
        if usuario is None:
            self.mensaje.config(text="Credenciales incorrectas.")
            self.entry_contrasena.delete(0, tk.END)
            return

        self.mensaje.config(text="")
        self.on_login_exitoso(usuario)
