import pygame
import random
import sys

pygame.init()

# Configuración para la ventana
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Fuentes
font = pygame.font.Font(None, 35)
menu_font = pygame.font.SysFont('Lucida Console', 45)
menu_font_small = pygame.font.SysFont('Lucida Console', 25)

# Imágenes
spaceImg = pygame.image.load("images/space.jpg").convert_alpha()
spaceImgIntro = pygame.image.load("images/intro.jpg").convert_alpha()


playerImg = pygame.image.load("images/ufo.png").convert_alpha()
playerSize = (110, 130)
playerImg = pygame.transform.scale(playerImg, playerSize)

enemieImg = pygame.image.load("images/enemie.png").convert_alpha()
enemieSize = (50, 80)
enemieImg = pygame.transform.scale(enemieImg, enemieSize)

# Sonidos
menu_sound = pygame.mixer.Sound('sounds/intro.wav')
click_sound = pygame.mixer.Sound('sounds/click.wav')
game_sound = pygame.mixer.Sound('sounds/game.wav')
end_sound = pygame.mixer.Sound('sounds/gameover.wav')

# Constantes del jugador y enemigos
playerHeight = 105
playerWidth = 90
player = pygame.Rect(WIDTH // 2 - playerWidth // 2, HEIGHT - playerHeight - 50, playerWidth, playerHeight)

enemieWidth = 30
enemieHeight = 35
enemies = []

# Puntuación
score = 0

# Controlar FPS
fps = pygame.time.Clock()

# Función para mostrar texto en pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Pantalla de inicio / menú principal
def show_menu():
    # -1 para que el sonido se repita
    menu_sound.play(-1) 
    while True:
        screen.fill(BLACK)
        screen.blit(spaceImgIntro, (-290,0))
        draw_text('Iniciar Juego', menu_font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        draw_text('Menú Instrucciones', menu_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Salir', menu_font, WHITE, screen, WIDTH // 2, HEIGHT // 1.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100:
                    if HEIGHT // 3 - 20 < mouse_y < HEIGHT // 3 + 20:
                        game_loop()  # Iniciar el juego
                    if HEIGHT // 2 - 20 < mouse_y < HEIGHT // 2 + 20:
                        show_how_to_play()  # Mostrar "Cómo jugar"
                    if HEIGHT // 1.5 - 20 < mouse_y < HEIGHT // 1.5 + 20:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

# Pantalla de "Cómo jugar"
def show_how_to_play():
    while True:
        screen.fill(BLACK)
        draw_text('Instrucciones de Juego', menu_font, WHITE, screen, WIDTH // 2, HEIGHT // 6)
        draw_text(' - Usa las flechas para mover la nave espacial', font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        draw_text('- Evita los obstáculos y acumula puntos', font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Presione ENTER para volver', menu_font_small, WHITE, screen, WIDTH // 2, HEIGHT // 1.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Asegúrate de verificar si una tecla fue presionada
                if event.key == pygame.K_RETURN:  # Verifica si se presiona Enter
                    click_sound.play()
                    return  # Volver al menú

        pygame.display.update()

# Bucle principal del juego
def game_loop():
    menu_sound.stop()
    game_sound.play(-1)
    global score
    score = 0  # Reinicia la puntuación al iniciar el juego
    player.x = WIDTH // 2 - playerWidth // 2
    enemies.clear()  # Limpiar los enemigos
    global level
    level = 0
    levelCalc = 0
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= levelCalc + 5
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += levelCalc + 5
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= levelCalc + 5
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += levelCalc + 5

        # Crear obstáculos
        if len(enemies) < 9:
            enemie = pygame.Rect(random.randint(0, WIDTH - enemieWidth), 0, enemieWidth, enemieHeight)
            enemies.append(enemie)


        # Mover los obstáculos
        for enemie in enemies:
            
            enemie.y += levelCalc + 5
            
            if enemie.top > HEIGHT:
                enemies.remove(enemie)
                if score > 9:
                    level = score // 9
                    levelCalc = level / 3
                    score += 1   # Incrementar la puntuación
                else:
                    score += 1   # Incrementar la puntuación

        # Detectar colisiones
        for enemie in enemies:
            if player.colliderect(enemie):
                running = False  # Termina el juego si hay colisión
                game_sound.stop()
                end_sound.play()

                pygame.time.delay(2000)

                show_menu()

        # Dibujar en pantalla
        screen.fill(BLACK)
        screen.blit(spaceImg, (0, 0))
        score_screen = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_screen, (WIDTH - WIDTH // 7, 15))
        screen.blit(playerImg, player)
        for enemie in enemies:
            screen.blit(enemieImg, enemie)

        pygame.display.flip()
        fps.tick(60)


# Iniciar el juego mostrando el menú
show_menu()
