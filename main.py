"""Punto de entrada. Crea la ventana principal y controla el cambio de vistas."""

import tkinter as tk
from pathlib import Path
from typing import Optional

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

RUTA_ICONO = Path("assets/icono_sabor_lojano.ico")


class Aplicacion:
    """Mantiene una unica ventana y reemplaza el frame visible (login o main)."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Restaurante Sabor Lojano")
        self.root.geometry("620x480")
        self.root.minsize(500, 400)
        self._cargar_icono()

        archivo_servicio = ArchivoServicio()
        self.restaurante_servicio = RestauranteServicio(archivo_servicio)

        self.frame_actual: Optional[tk.Frame] = None
        self.mostrar_login()

    def _cargar_icono(self) -> None:
        """Pone el logo como icono de la ventana. Si no se encuentra el
        archivo o el sistema operativo no lo soporta, la app sigue sin
        icono, sin detenerse."""
        if not RUTA_ICONO.exists():
            return
        try:
            self.root.iconbitmap(str(RUTA_ICONO))
            return
        except tk.TclError:
            pass

        # En algunos sistemas (Linux) iconbitmap no acepta .ico directamente.
        try:
            from PIL import Image, ImageTk

            imagen = Image.open(RUTA_ICONO)
            self._icono_ventana = ImageTk.PhotoImage(imagen)
            self.root.iconphoto(True, self._icono_ventana)
        except Exception:
            pass

    def _cambiar_frame(self, nuevo_frame: tk.Frame) -> None:
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = nuevo_frame
        self.frame_actual.pack(fill="both", expand=True)

    def mostrar_login(self) -> None:
        vista = LoginView(self.root, self.restaurante_servicio, self.mostrar_main)
        self._cambiar_frame(vista)

    def mostrar_main(self, usuario: Usuario) -> None:
        vista = MainView(self.root, self.restaurante_servicio, usuario, self.mostrar_login)
        self._cambiar_frame(vista)


def main() -> None:
    root = tk.Tk()
    Aplicacion(root)
    root.mainloop()


if __name__ == "__main__":
    main()
