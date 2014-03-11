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
        self.y = self.actor_a_seguir.y


class Accion:

    def iniciar(self, actor):
        pass
    def actualizar(self, actor):
        actor.rotacion = 130
        pass

class Caminando(Accion):

    def iniciar(self, actor):
        print "Ingresando al modo Caminando"
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

    def aplicar_limites_del_escenario(self, actor):
        if actor.x < -400:
            actor.x = -400

        if actor.x > 400:
            actor.x = 400

class Parado(Accion):

    def iniciar(self, actor):
        print "Ingresando al modo Parado"
        pass

    def actualizar(self, actor):
        if pilas.mundo.control.izquierda or pilas.mundo.control.derecha:
            actor.realizar_accion(Caminando())


class Protagonista(pilas.actores.Actor):

    def __init__(self):
        self.grilla = pilas.imagenes.cargar_grilla('../data/protagonista.png', 6)
        pilas.actores.Actor.__init__(self)
        self.imagen = self.grilla
        self.y = -200
        self.realizar_accion(Parado())

    def actualizar(self):
        self.accion.actualizar(self)

    def realizar_accion(self, accion):
        accion.iniciar(self)
        self.accion = accion


print "iniciando", Parado
pilas.fondos.Fondo('../data/fondo.png')
protagonista = Protagonista()
Sombra(protagonista)

pilas.ejecutar()
