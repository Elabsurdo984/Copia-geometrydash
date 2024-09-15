import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Variables del jugador
player_width = 40
player_height = 60
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 10
player_velocity_y = 0
is_jumping = False
gravity = 1

# Lista de obstáculos (diferentes tamaños y colores)
obstacles = [
    {'width': 20, 'height': 40, 'color': RED, 'speed': -6},
    {'width': 30, 'height': 50, 'color': BLUE, 'speed': -7},
    {'width': 15, 'height': 30, 'color': GREEN, 'speed': -5}
]

# Inicializar el primer obstáculo
current_obstacle = random.choice(obstacles)
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - current_obstacle['height'] - 10

# Reloj para controlar el FPS
clock = pygame.time.Clock()

# Fuente para el puntaje
font = pygame.font.SysFont(None, 55)

# Función para mostrar texto en pantalla
def show_score(score):
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, [10, 10])

# Función para reiniciar un nuevo obstáculo aleatorio
def reset_obstacle():
    global current_obstacle
    current_obstacle = random.choice(obstacles)  # Elegir un obstáculo aleatorio
    return SCREEN_WIDTH, SCREEN_HEIGHT - current_obstacle['height'] - 10

# Función principal del juego
def game_loop():
    global player_y, player_velocity_y, is_jumping, obstacle_x, obstacle_y, current_obstacle
    score = 0
    running = True
    
    while running:
        screen.fill(WHITE)

        # Eventos de teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    player_velocity_y = -15
                    is_jumping = True

        # Gravedad y salto
        if is_jumping:
            player_y += player_velocity_y
            player_velocity_y += gravity

            # Limitar el salto a que no suba indefinidamente
            if player_y >= SCREEN_HEIGHT - player_height - 10:
                player_y = SCREEN_HEIGHT - player_height - 10
                is_jumping = False
                player_velocity_y = 0

        # Mover el obstáculo
        obstacle_x += current_obstacle['speed']

        # Verificar si el obstáculo sale de la pantalla y resetear
        if obstacle_x < -current_obstacle['width']:
            obstacle_x, obstacle_y = reset_obstacle()  # Reiniciar la posición del obstáculo
            score += 1  # Incrementar el puntaje cuando se pasa un obstáculo

        # Dibuja el jugador y el obstáculo
        pygame.draw.rect(screen, BLACK, [player_x, player_y, player_width, player_height])
        pygame.draw.rect(screen, current_obstacle['color'], [obstacle_x, obstacle_y, current_obstacle['width'], current_obstacle['height']])

        # Mostrar el puntaje
        show_score(score)

        # Detectar colisiones
        if (player_x + player_width > obstacle_x and player_x < obstacle_x + current_obstacle['width']) and \
           (player_y + player_height > obstacle_y):
            running = False  # Termina el juego si hay colisión

        # Actualizar la pantalla y el reloj
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Ejecutar el juego
game_loop()
