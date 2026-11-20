from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox


class Personaje(ABC):
    def __init__(self, nombre: str, vida_max: int):
        self._nombre = nombre
        self._vida_max = vida_max
        self._vida = vida_max

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, valor: int) -> None:
        self._vida = max(0, min(self._vida_max, int(valor)))

    def curar(self, cantidad: int) -> int:
        if cantidad <= 0:
            raise ValueError("La curación debe ser mayor que 0.")
        self.vida = self._vida + cantidad
        return self._vida

    @abstractmethod
    def actuar(self) -> tuple[str, int]:
        pass


class Guerrero(Personaje):
    def __init__(self, nombre: str = "Guerrero"):
        super().__init__(nombre, vida_max=100)

    def actuar(self) -> tuple[str, int]:
        return ("Golpe firme", 18)


class Mago(Personaje):
    def __init__(self, nombre: str = "Mago"):
        super().__init__(nombre, vida_max=80)

    def actuar(self) -> tuple[str, int]:
        return ("Chispa arcana", 24)


class AppPOO:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mini Juego POO - Parcial")
        self.root.geometry("420x260")

        self.heroe = Guerrero("Campeón")
        self.rival = Mago("Rival")
        self.puntos = 0

        self.lbl_estado = tk.Label(root, text="", font=("Arial", 11))
        self.lbl_estado.pack(pady=15)

        self.lbl_log = tk.Label(root, text="Elige una acción para empezar.", wraplength=380)
        self.lbl_log.pack(pady=10)

        tk.Button(root, text="1. Atacar rival", command=self.atacar).pack(fill="x", padx=60, pady=3)
        tk.Button(root, text="2. Curar héroe (+15)", command=self.curar_heroe).pack(fill="x", padx=60, pady=3)
        tk.Button(root, text="3. Reiniciar partida", command=self.reiniciar).pack(fill="x", padx=60, pady=3)

        self.actualizar_texto()

    def actualizar_texto(self) -> None:
        self.lbl_estado.config(
            text=f"{self.heroe.nombre}: {self.heroe.vida} HP  |  {self.rival.nombre}: {self.rival.vida} HP  |  Pts: {self.puntos}"
        )

    def atacar(self) -> None:
        if self.rival.vida <= 0:
            messagebox.showinfo("Partida terminada", "¡Ya ganaste! Reinicia para jugar otra vez.")
            return
        nombre_ataque, dano = self.heroe.actuar()
        self.rival.vida = self.rival.vida - dano
        self.puntos += 10
        mensaje = f"{self.heroe.nombre} usó {nombre_ataque} (-{dano} HP al rival)."
        if self.rival.vida == 0:
            mensaje += " ¡Rival derrotado!"
        self.lbl_log.config(text=mensaje)
        self.actualizar_texto()

    def curar_heroe(self) -> None:
        try:
            nueva_vida = self.heroe.curar(15)
            self.lbl_log.config(text=f"{self.heroe.nombre} se curó. Vida actual: {nueva_vida} HP.")
            self.actualizar_texto()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def reiniciar(self) -> None:
        self.heroe.vida = 100
        self.rival.vida = 80
        self.puntos = 0
        self.lbl_log.config(text="Partida reiniciada.")
        self.actualizar_texto()


if __name__ == "__main__":
    ventana = tk.Tk()
    AppPOO(ventana)
    ventana.mainloop()
