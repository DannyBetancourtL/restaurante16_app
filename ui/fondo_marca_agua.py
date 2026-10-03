"""Canvas de fondo que muestra el logo bien tenue detras del contenido de
cada pantalla, a manera de marca de agua."""

import tkinter as tk
from pathlib import Path

RUTA_MARCA_AGUA = Path("assets/marca_agua_sabor_lojano.png")


class FondoMarcaAgua(tk.Canvas):

    def __init__(self, parent: tk.Widget, color_fondo: str = "#EAF4F3"):
        super().__init__(parent, highlightthickness=0, bg=color_fondo)
        self._imagen = None
        self._item_imagen = None
        self._item_contenido = None
        self._anclaje_contenido = "n"
        self._cargar_imagen()
        self.bind("<Configure>", self._al_redimensionar)

    def _cargar_imagen(self) -> None:
        if not RUTA_MARCA_AGUA.exists():
            return
        try:
            from PIL import Image, ImageTk

            imagen = Image.open(RUTA_MARCA_AGUA)
            self._imagen = ImageTk.PhotoImage(imagen)
            self._item_imagen = self.create_image(0, 0, image=self._imagen)
        except Exception:
            pass

    def colocar_contenido(self, contenido: tk.Widget, anclaje: str = "n") -> None:
        """Ubica el contenido encima del fondo. El contenido conserva su
        tamaño natural, no se estira, para que la marca de agua se siga
        viendo alrededor."""
        self._anclaje_contenido = anclaje
        self._item_contenido = self.create_window(0, 0, window=contenido, anchor=anclaje)

    def _al_redimensionar(self, evento: tk.Event) -> None:
        if self._item_imagen is not None:
            self.coords(self._item_imagen, evento.width // 2, evento.height // 2)

        if self._item_contenido is not None:
            if self._anclaje_contenido == "center":
                self.coords(self._item_contenido, evento.width // 2, evento.height // 2)
            else:
                self.coords(self._item_contenido, evento.width // 2, 15)
