import pilas
pilas.iniciar(ancho=800, alto=600)
pilas.reiniciar_si_cambia(__file__)


class Sombra(pilas.actores.Actor):

    def __init__(self, actor):
        pilas.actores.Actor.__init__(self)
        self.imagen = "../data/sombra.png"
        self.actor_a_seguir = actor
        self.transparencia = 50
        self.z = actor.z + 1

    def actualizar(self):
        self.x = self.actor_a_seguir.x
        self.y = self.actor_a_seguir.y - self.actor_a_seguir.altura_salto
        self.escala = 1 - (self.actor_a_seguir.altura_salto / 500.0)


class Accion:

    def iniciar(self, actor):
        pass

    def actualizar(self, actor):
        pass

    def aplicar_limites_del_escenario(self, actor):
        if actor.x < -400:
            actor.x = -400

        if actor.x > 400:
            actor.x = 400

class Caminando(Accion):

    def iniciar(self, actor):
        pass

    def actualizar(self, actor):
        velocidad = 10

        if pilas.mundo.control.izquierda:
            actor.x -= velocidad
            actor.espejado = True

        if pilas.mundo.control.derecha:
            actor.x += velocidad
            actor.espejado = False

        self.aplicar_limites_del_escenario(actor)

        if not pilas.mundo.control.izquierda and not pilas.mundo.control.derecha:
            actor.realizar_accion(Parado())

        if pilas.mundo.control.arriba:
            actor.realizar_accion(Saltando())


class Parado(Accion):

    def iniciar(self, actor):
        pass

    def actualizar(self, actor):
        if pilas.mundo.control.izquierda or pilas.mundo.control.derecha:
            actor.realizar_accion(Caminando())

        if pilas.mundo.control.arriba:
            actor.realizar_accion(Saltando())

class Saltando(Accion):

    def iniciar(self, actor):
        self.velocidad_salto = 20
        self.y = actor.y

    def actualizar(self, actor):
        velocidad = 7
        self.velocidad_salto -= 1
        actor.y += self.velocidad_salto

        if self.y > actor.y:
            actor.y = self.y
            actor.realizar_accion(Parado())

        if pilas.mundo.control.izquierda:
            actor.x -= velocidad
            actor.espejado = True

        if pilas.mundo.control.derecha:
            actor.x += velocidad
            actor.espejado = False

        actor.altura_salto = actor.y - self.y

class Protagonista(pilas.actores.Actor):

    def __init__(self):
        self.grilla = pilas.imagenes.cargar_grilla('../data/protagonista.png', 6)
        pilas.actores.Actor.__init__(self)
        self.imagen = self.grilla
        self.y = -200
        self.realizar_accion(Parado())
        self.altura_salto = 0
        self.radio_de_colision = 50

    def actualizar(self):
        self.accion.actualizar(self)

    def realizar_accion(self, accion):
        accion.iniciar(self)
        self.accion = accion

class Calabaza(pilas.actores.Actor):

    def __init__(self, x=0, y=0):
        imagen = "../data/calabaza.png"
        pilas.actores.Actor.__init__(self, imagen, x, y)
        figura = pilas.fisica.Circulo(x, y, 70)
        self.imitar(figura)
        self.radio_de_colision = 70


pilas.fondos.Fondo('../data/fondo.png')
protagonista = Protagonista()
Sombra(protagonista)
calabazas = Calabaza() * 2


def cuando_toca_calabaza(protagonista, calabaza):
    calabaza.eliminar()


pilas.mundo.colisiones.agregar(protagonista, calabazas, cuando_toca_calabaza)


pilas.ejecutar()
