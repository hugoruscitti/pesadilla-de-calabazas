# -*- encoding: utf-8 -*-
import pilas


def obtener_numero_al_azar(a, b):
    """Retorna un número a azar comprendido entre
    'a' y 'b', por ejemplo:

        >>> obtener_numero_al_azar(20, 100)
        52
    """
    import random
    return random.randint(a, b)


pilas.iniciar(ancho=800, alto=600)
pilas.reiniciar_si_cambia(__file__)

#asdasd

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
        actor.definir_animacion([3, 4, 5, 4])

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
        actor.definir_animacion([2])

    def actualizar(self, actor):
        if pilas.mundo.control.izquierda or pilas.mundo.control.derecha:
            actor.realizar_accion(Caminando())

        if pilas.mundo.control.arriba:
            actor.realizar_accion(Saltando())


class Saltando(Accion):

    def iniciar(self, actor):
        self.velocidad_salto = 20
        self.y = actor.y
        actor.definir_animacion([0])
        actor.sonido_saltar.reproducir()


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
        self.aplicar_limites_del_escenario(actor)


class ProtagonistaPerdiendo(pilas.actores.Actor):

    def __init__(self, x, y, espejado):
        self.grilla = pilas.imagenes.cargar_grilla('../data/protagonista.png', 6)
        pilas.actores.Actor.__init__(self)
        self.imagen = self.grilla
        self.imagen.definir_cuadro(1)
        self.x = x
        self.y = y
        self.espejado = espejado
        self.velocidad_salto = 10
        self.rotacion = [-90], 1

    def actualizar(self):
        self.velocidad_salto -= 0.7
        self.y += self.velocidad_salto

        if self.y < -600:
            pilas.escena_actual().mostrar_escena_game_over()

class Animacion:

    def __init__(self):
        self.cuadros_animacion = [-1]

    def definir_cuadro(self, indice):
        self.imagen.definir_cuadro(indice)

    def definir_animacion(self, cuadros):
        if cuadros != self.cuadros_animacion:
            self.indice_animacion = 0
            self.cuadros_animacion = cuadros
            self.contador_animacion = 0
            self.definir_cuadro(cuadros[0])          # Define el cuadro inicial de la animación.

    def avanzar_animacion(self):
        self.contador_animacion += 1

        if self.contador_animacion > 5:
            self.contador_animacion = 0
            cuadro = self.obtener_siguiente_cuadro()
            self.definir_cuadro(cuadro)

    def obtener_siguiente_cuadro(self):
        """Retorna el siguiente numero de imagen en la grilla con respecto
        a la animación.

        Por ejemplo, si la animación es [0, 1, 2], esta función
        va a devolver los números 0, 1, 2, 0, 1, 2 ... cuantas veces se
        llame.
        """
        self.indice_animacion += 1

        if self.indice_animacion == len(self.cuadros_animacion):
            self.indice_animacion = 0

        return self.cuadros_animacion[self.indice_animacion]

class Protagonista(pilas.actores.Actor, Animacion):

    def __init__(self):
        self.grilla = pilas.imagenes.cargar_grilla('../data/protagonista.png', 6)
        pilas.actores.Actor.__init__(self)
        self.imagen = self.grilla
        self.y = -200
        Animacion.__init__(self)
        self.realizar_accion(Parado())
        self.altura_salto = 0
        self.radio_de_colision = 50
        self.figura = pilas.fisica.Circulo(self.x, self.y, 30, dinamica=False)
        self.sonido_saltar = pilas.sonidos.cargar("../data/saltar.wav")


    def actualizar(self):
        self.avanzar_animacion()
        self.accion.actualizar(self)
        self.figura.x = self.x
        self.figura.y = self.y

    def realizar_accion(self, accion):
        accion.iniciar(self)
        self.accion = accion


class Calabaza(pilas.actores.Actor):
    """Representa al protagonista de nuestro juego."""

    def __init__(self, x=0, y=0):
        imagen = "../data/calabaza.png"
        pilas.actores.Actor.__init__(self, imagen, x, y)
        figura = pilas.fisica.Circulo(x, y, 70)
        figura.rotacion = obtener_numero_al_azar(0, 360)
        self.imitar(figura)
        self.radio_de_colision = 70
        self.escala = 0.8


class CalabazaExplotando(pilas.actores.Actor):

    def __init__(self, x=0, y=0, rotacion=0):
        imagen = "../data/calabaza-gris.png"
        pilas.actores.Actor.__init__(self, imagen, x, y)
        self.rotacion = rotacion
        self.escala = 0.8
        self.escala = [0], 0.2
        self.transparencia = [100], 0.3
        self.contador = 0

    def actualizar(self):
        self.contador += 1

        if self.contador > 20:
            self.eliminar()

class EfectoGolpe(pilas.actores.Animacion):
    """Muestra un destello para representar una colisión de golpe."""

    def __init__(self, x, y):
        import random
        grilla = pilas.imagenes.cargar_grilla("golpe.png", 2)
        pilas.actores.Animacion.__init__(self, grilla, ciclica=False, velocidad=10, x=x, y=y)
        self.escala = 6.5
        self.escala = [1.5], 0.1
        self.rotacion = random.choice([0, 45, 90, 150])
        self.z = -1000


class EscenaGameOver(pilas.escena.Base):

    def iniciar(self):
        pilas.fondos.Fondo('../data/fondo.png')
        manchas = pilas.actores.Actor('../data/manchas.png')
        manchas.transparencia = 10

        pilas.actores.Texto("Tu puntaje es: %d" %(self.puntaje), magnitud=40, y=20)
        pilas.actores.Texto(u"Pulsá espacio para volver a empezar", y=-50)
        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == " ": # Si es la tecla espacio
            pilas.cambiar_escena(EscenaJuego())

    def definir_puntaje(self, puntaje):
        self.puntaje = puntaje

class EscenaJuego(pilas.escena.Base):

    def iniciar(self):
        sonido_golpe = pilas.sonidos.cargar("../data/golpe.wav")
        sonido_pisar = pilas.sonidos.cargar("../data/pisar.wav")

        pilas.fondos.Fondo('../data/fondo.png')
        protagonista = Protagonista()
        sombra = Sombra(protagonista)

        calabazas = []

        def crear_calabaza():
            x = obtener_numero_al_azar(-300, 300)
            nueva_calabaza = Calabaza(x, 350)
            calabazas.append(nueva_calabaza)
            return True              # Le indicamos a la tarea que se repita

        pilas.mundo.agregar_tarea(2, crear_calabaza)

        pilas.actores.Texto("Puntaje: ", x=-340, y=270)
        self.puntaje = pilas.actores.Puntaje(x=-290, y=270, color=pilas.colores.blanco)

        def cuando_toca_calabaza(protagonista, calabaza):

            if protagonista.y > calabaza.y + 50:
                efecto = CalabazaExplotando(calabaza.x, calabaza.y, calabaza.rotacion)
                calabaza.eliminar()
                sonido_pisar.reproducir()

                # Aumenta y realiza un efecto sobre el puntaje.
                self.puntaje.aumentar(5)
                import random
                self.puntaje.escala = 1.5
                self.puntaje.escala = [1], 0.2
                self.puntaje.rotacion = random.choice([30, 20, 10, 50, 30])
                self.puntaje.rotacion = [0], 0.25
            else:
                sonido_golpe.reproducir()
                protagonista.eliminar()
                protagonista.figura.eliminar()
                sombra.eliminar()
                ProtagonistaPerdiendo(protagonista.x, protagonista.y, protagonista.espejado)
                EfectoGolpe(protagonista.x, protagonista.y)

        pilas.mundo.colisiones.agregar(protagonista, calabazas, cuando_toca_calabaza)
        pilas.escena_actual().fisica.eliminar_techo()

    def mostrar_escena_game_over(self):
        puntaje_como_valor = self.puntaje.obtener()
        nueva_escena = EscenaGameOver()
        nueva_escena.definir_puntaje(puntaje_como_valor)
        pilas.cambiar_escena(nueva_escena)


musica = pilas.musica.cargar('data/musica.mp3')
musica.reproducir()
pilas.cambiar_escena(EscenaJuego())
pilas.ejecutar()
