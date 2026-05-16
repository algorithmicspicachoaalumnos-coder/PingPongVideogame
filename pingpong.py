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

# Velocidad dinámica de la pelota: constantes configurables
# incremento por segundo (por ejemplo 0.05 = +5% cada segundo)
SPEED_INCREASE_PER_SECOND = 0.05
# multiplicador máximo para evitar que sea imposible
MAX_SPEED_MULTIPLIER = 3.0

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

    # modificaciones a la pelota y puntuación
    try:
        ball_rect
    except NameError:
        ball_img = None
        ball_path = os.path.join(script_dir, "PING PONG BALL.png")
        if os.path.exists(ball_path):
            try:
                ball_img = pygame.image.load(ball_path).convert_alpha()
                bw, bh = ball_img.get_size()
                target_hb = 32
                if bh != target_hb and bh != 0:
                    new_wb = int(bw * (target_hb / bh))
                    ball_img = pygame.transform.scale(ball_img, (new_wb, target_hb))
                ball_rect = ball_img.get_rect()
            except Exception:
                ball_img = None

        if ball_img is None:
            ball_rect = pygame.Rect(ancho//2 - 8, alto//2 - 8, 16, 16)
        else:
            ball_rect.center = (ancho//2, alto//2)

        # ball_vel actúa como la velocidad base (dirección y magnitud relativa)
        ball_vel = [3, 2]
        # posición en float para aplicar multiplicadores sin perder precisión
        ball_pos = [float(ball_rect.x), float(ball_rect.y)]
        # marca del tiempo (ms) de la última salida/servicio; usada para aumentar velocidad
        last_serve_time = pygame.time.get_ticks()
        # multiplicador actual (se calcula dinámicamente cada frame)
        ball_speed_multiplier = 1.0
        score1 = 0
        score2 = 0
        font = pygame.font.SysFont(None, 36)

    # Calcular multiplicador basado en tiempo desde el último servicio
    elapsed_ms = pygame.time.get_ticks() - last_serve_time
    elapsed_s = elapsed_ms / 1000.0
    ball_speed_multiplier = min(MAX_SPEED_MULTIPLIER, 1.0 + SPEED_INCREASE_PER_SECOND * elapsed_s)

    # Move ball usando posición en float para suavizar incrementos pequeños
    ball_pos[0] += ball_vel[0] * ball_speed_multiplier
    ball_pos[1] += ball_vel[1] * ball_speed_multiplier
    ball_rect.x = int(ball_pos[0])
    ball_rect.y = int(ball_pos[1])

    # Bounce on top/bottom
    if ball_rect.top <= 0:
        ball_rect.top = 0
        ball_vel[1] = -ball_vel[1]
        # mantener coherencia con ball_pos
        ball_pos[1] = float(ball_rect.y)
    if ball_rect.bottom >= alto:
        ball_rect.bottom = alto
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] = float(ball_rect.y)

    # Collisions with paddles
    if ball_rect.colliderect(paleta_rect):
        # place ball to the left of the right paddle and reflect
        ball_rect.right = paleta_rect.left
        ball_vel[0] = -abs(ball_vel[0])
        # tweak vertical velocity based on hit position
        rel = (ball_rect.centery - paleta_rect.centery) / (paleta_rect.height / 2)
        ball_vel[1] += int(rel * 2)
        # ajustar posición flotante tras la colisión
        ball_pos[0] = float(ball_rect.x)
        ball_pos[1] = float(ball_rect.y)

    if ball_rect.colliderect(paleta2_rect):
        ball_rect.left = paleta2_rect.right
        ball_vel[0] = abs(ball_vel[0])
        rel2 = (ball_rect.centery - paleta2_rect.centery) / (paleta2_rect.height / 2)
        ball_vel[1] += int(rel2 * 2)
        ball_pos[0] = float(ball_rect.x)
        ball_pos[1] = float(ball_rect.y)

    # Check left/right for score (loss)
    if ball_rect.left <= 0:
        # right player scores
        score1 += 1
        # reset ball toward the player who missed
        ball_rect.center = (ancho//2, alto//2)
        ball_vel = [3, 2]
        # resetamos la posición float y el temporizador para que la velocidad vuelva a iniciar
        ball_pos = [float(ball_rect.x), float(ball_rect.y)]
        last_serve_time = pygame.time.get_ticks()

    if ball_rect.right >= ancho:
        score2 += 1
        ball_rect.center = (ancho//2, alto//2)
        ball_vel = [-3, -2]
        ball_pos = [float(ball_rect.x), float(ball_rect.y)]
        last_serve_time = pygame.time.get_ticks()

    # Draw ball
    if 'ball_img' in locals() and ball_img:
        ventana.blit(ball_img, ball_rect)
    else:
        pygame.draw.ellipse(ventana, (255, 255, 255), ball_rect)

    # Mostrar multiplicador de velocidad en pantalla
    mult_surf = font.render(f"Velocidad x{ball_speed_multiplier:.2f}", True, (255, 255, 255))
    ventana.blit(mult_surf, (ancho//2 - mult_surf.get_width()//2, 10))

    # Draw scores
    score_surf = font.render(f"P1: {score1}", True, (255, 255, 255))
    score_surf2 = font.render(f"P2: {score2}", True, (255, 255, 255))
    ventana.blit(score_surf, (ancho - 120, 10))
    ventana.blit(score_surf2, (20, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()