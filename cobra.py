import pygame
import random

# Inicializar variáveis
vx = 0
vy = 0

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Cobrinhaaaaa!!!!")

# Inicializar posição do jogador
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

snake_body = [player_pos.copy()]  # Lista para armazenar o corpo da cobra

apple_image = pygame.image.load("apple.png")
apple_size = 55
apple_image= pygame.transform.scale(apple_image, (apple_size , apple_size))
snake_head_image = pygame.image.load("head.png")
snake_head_image = pygame.transform.scale(snake_head_image, (35, 35))

# Função para gerar nova posição da maçã
def new_apple_position():
    return pygame.Vector2(
        random.randint(0, screen.get_width() // apple_size - 1) * apple_size,
        random.randint(0, screen.get_height() // apple_size - 1) * apple_size
    )

# Inicializar posição da maçã
apple_pos = new_apple_position()

while running:
    # Verificar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verificar teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and vy == 0:
        vx = 0
        vy = -35
    if keys[pygame.K_s] and vy == 0:
        vx = 0
        vy = 35
    if keys[pygame.K_a] and vx == 0:
        vx = -35
        vy = 0
    if keys[pygame.K_d] and vx == 0:
        vx = 35
        vy = 0

    # Atualizar posição do jogador
    if vx != 0 or vy != 0:
        new_head = player_pos + pygame.Vector2(vx, vy)
        snake_body.insert(0, new_head)
        player_pos = new_head.copy()

        # Verificar colisão com a maçã
        if pygame.Rect(player_pos.x, player_pos.y, 35, 35).colliderect(pygame.Rect(apple_pos.x, apple_pos.y, apple_size, apple_size)):
            apple_pos = new_apple_position()  # Gerar nova posição para a maçã
        else:
            snake_body.pop()  # Remover a cauda se não comer maçã

        # Verificar colisão com o próprio corpo
        for segment in snake_body[1:]:
            if player_pos == segment:
                running = False  # Encerrar o jogo se a cabeça colidir com o corpo

        # Verificar se a cabeça está fora dos limites da tela
        if (player_pos.x < 0 or player_pos.x >= screen.get_width() or
            player_pos.y < 0 or player_pos.y >= screen.get_height()):
            running = False  # Encerrar o jogo se a cabeça sair da área do jogo

    # Preencher a tela com uma cor
    image = pygame.image.load("grass.png")
    image = pygame.transform.scale(image, (700, 700))
    screen.blit(image, (0, 0))

    # Desenhar a cobra
    for segment in snake_body:
        pygame.draw.rect(screen, "green", (segment.x, segment.y, 35, 35))

    # Desenhar a maçã
    screen.blit(apple_image, (apple_pos.x, apple_pos.y))
    screen.blit(snake_head_image, (snake_body[0].x, snake_body[0].y))

    # Atualizar a tela
    pygame.display.flip()

    # Limitar FPS a 10 para movimento da cobra
    dt = clock.tick(12) / 1000

pygame.quit()
