import pygame
pygame.init()
ancho = 800
alto = 600
pantalla = (ancho, alto)
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Ping Pong")
Azul = (0, 0, 200)
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    ventana.fill(Azul)
    pygame.display.flip()
    pygame.display.update()
pygame.quit()