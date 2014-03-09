import pilas
pilas.iniciar(ancho=800, alto=600)
pilas.reiniciar_si_cambia(__file__)


class Protagonista(pilas.actores.Actor):

    def __init__(self):
        self.grilla = pilas.imagenes.cargar_grilla('../data/protagonista.png', 6)
        pilas.actores.Actor.__init__(self)
        self.imagen = self.grilla
        self.y = -200

    def actualizar(self):
        velocidad = 10

        if pilas.mundo.control.izquierda:
            self.x -= velocidad

        if pilas.mundo.control.derecha:
            self.x += velocidad

        if self.x < -400:
            self.x = -400

        if self.x > 400:
            self.x = 400


Protagonista()

pilas.ejecutar()
