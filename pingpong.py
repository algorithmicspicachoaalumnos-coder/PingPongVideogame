import pygame
import os

pygame.init()

ancho = 800
alto = 600
pantalla = (ancho, alto)
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Ping Pong")
Azul = (0, 0, 200)
Verde = (0, 200, 0)

clock = pygame.time.Clock()
ejecutando = True

# Paleta del jugador 1: intentamos cargar la imagen; si no existe usamos un rect como fallback
paleta_img = None
paleta2_img = None
# Márgen desde el borde derecho (px) — reduce este número para dejarla más pegada
paleta_margin = 2
# rect fallback: ancho de 10, ubicado paleta_margin px desde la derecha
paleta_rect = pygame.Rect(ancho - paleta_margin - 10, 250, 10, 100)
# Aseguramos explícitamente que su borde derecho quede a ancho - paleta_margin
paleta_rect.right = ancho - paleta_margin
paleta_speed = 5

# Paleta izquierda (jugador 2) - fallback rect
paleta2_rect = pygame.Rect(paleta_margin, 250, 10, 100)
paleta2_rect.left = paleta_margin
paleta2_speed = paleta_speed

# Buscamos la imagen en el directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
paleta_path = os.path.join(script_dir, "paleta num 1.webp")
if os.path.exists(paleta_path):
    try:
        paleta_img = pygame.image.load(paleta_path).convert_alpha()
        iw, ih = paleta_img.get_size()
        target_h = 100
        if ih != target_h and ih != 0:
            new_w = int(iw * (target_h / ih))
            paleta_img = pygame.transform.scale(paleta_img, (new_w, target_h))
        paleta_rect.size = paleta_img.get_size()
        # Colocamos la paleta de modo que su borde derecho quede a paleta_margin px del borde de la ventana
        paleta_rect.topright = (ancho - paleta_margin, 500)
    except Exception:
        paleta_img = None

# Cargamos imagen para la paleta izquierda (paleta num 2.png)
paleta2_path = os.path.join(script_dir, "paleta num 2.png")
if os.path.exists(paleta2_path):
    try:
        paleta2_img = pygame.image.load(paleta2_path).convert_alpha()
        iw2, ih2 = paleta2_img.get_size()
        target_h2 = 100
        if ih2 != target_h2 and ih2 != 0:
            new_w2 = int(iw2 * (target_h2 / ih2))
            paleta2_img = pygame.transform.scale(paleta2_img, (new_w2, target_h2))
        paleta2_rect.size = paleta2_img.get_size()
        # Colocamos la paleta izquierda a paleta_margin px del borde izquierdo
        paleta2_rect.topleft = (paleta_margin, 500)
    except Exception:
        paleta2_img = None

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Manejo de teclas para mover la paleta (Flecha arriba, Flecha abajo)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP]:
        paleta_rect.y -= paleta_speed
    if teclas[pygame.K_DOWN]:
        paleta_rect.y += paleta_speed

    # Controles para la paleta izquierda: W / S
    if teclas[pygame.K_w]:
        paleta2_rect.y -= paleta2_speed
    if teclas[pygame.K_s]:
        paleta2_rect.y += paleta2_speed

    # Limitar la paleta dentro de la ventana
    if paleta_rect.top < 0:
        paleta_rect.top = 0
    if paleta_rect.bottom > alto:
        paleta_rect.bottom = alto
    if paleta2_rect.top < 0:
        paleta2_rect.top = 0
    if paleta2_rect.bottom > alto:
        paleta2_rect.bottom = alto

    ventana.fill(Azul)

    # Dibujar borde (límite) de la ventana en verde
    border_thickness = 4
    pygame.draw.rect(ventana, Verde, ventana.get_rect(), border_thickness)

    # Dibujar paleta
    if paleta_img:
        ventana.blit(paleta_img, paleta_rect)
    else:
        pygame.draw.rect(ventana, Verde, paleta_rect)

    # Dibujar paleta izquierda
    if paleta2_img:
        ventana.blit(paleta2_img, paleta2_rect)
    else:
        pygame.draw.rect(ventana, Verde, paleta2_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()