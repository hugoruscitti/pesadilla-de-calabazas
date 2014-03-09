import pilas
pilas.iniciar()
pilas.reiniciar_si_cambia(__file__)

pilas.actores.Pelota() * 3
pilas.fondos.Tarde()

aceituna = pilas.actores.Aceituna()
aceituna.escala = 4

pilas.ejecutar()
