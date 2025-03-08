import pygame
import sys
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Simplificado")

# Cores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configurações do labirinto
tile_size = 20
maze = [
    "####################",
    "#..................#",
    "#.###.###..###.###.#",
    "#.#...#......#...#.#",
    "#.#.###.####.###.#.#",
    "#.#................#",
    "#.###.###..###.###.#",
    "#...#......#.......#",
    "###.#.###..###.#.###",
    "#...#..........#...#",
    "#.###.###..###.###.#",
    "#..................#",
    "####################",
]

# Função para desenhar o labirinto
def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "#":
                pygame.draw.rect(screen, WHITE, (col * tile_size, row * tile_size, tile_size, tile_size))
            elif maze[row][col] == ".":
                pygame.draw.circle(screen, WHITE, (col * tile_size + tile_size // 2, row * tile_size + tile_size // 2), 3)

# Classe do Pac-Man
class PacMan:
    def __init__(self):
        self.x = 1 * tile_size
        self.y = 1 * tile_size
        self.speed = tile_size
        self.mouth_angle = 0
        self.mouth_direction = 1

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Verifica colisão com paredes
        row = new_y // tile_size
        col = new_x // tile_size
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != "#":
            self.x = new_x
            self.y = new_y

    def draw(self):
        self.mouth_angle += self.mouth_direction * 5
        if self.mouth_angle > 45 or self.mouth_angle < 0:
            self.mouth_direction *= -1
        pygame.draw.arc(screen, YELLOW, (self.x, self.y, tile_size, tile_size), 
                        self.mouth_angle * 0.0174533, (360 - self.mouth_angle) * 0.0174533, tile_size // 2)

# Classe dos Fantasmas
class Ghost:
    def __init__(self, color):
        # Gera uma posição inicial válida (onde não há paredes)
        while True:
            self.x = random.randint(0, WIDTH // tile_size - 1) * tile_size
            self.y = random.randint(0, HEIGHT // tile_size - 1) * tile_size
            row = self.y // tile_size
            col = self.x // tile_size
            if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != "#":
                break
        self.color = color
        self.speed = tile_size // 2

    def move(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        dx, dy = random.choice(directions)
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Verifica colisão com paredes e limites do labirinto
        row = new_y // tile_size
        col = new_x // tile_size
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != "#":
            self.x = new_x
            self.y = new_y

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + tile_size // 2, self.y + tile_size // 2), tile_size // 2)

# Cria o Pac-Man e os fantasmas (apenas 2 fantasmas)
pacman = PacMan()
ghosts = [Ghost(RED) for _ in range(2)]  # Alterado para 2 fantasmas

# Pontuação
score = 0

# Fonte para exibir a pontuação e mensagens
font = pygame.font.Font(None, 36)

# Função para verificar se todas as bolinhas foram comidas
def todas_bolinhas_comidas():
    for row in maze:
        if "." in row:
            return False
    return True

# Loop principal do jogo
clock = pygame.time.Clock()
game_over = False
victory = False
while True:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not victory:
        # Movimentação do Pac-Man
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.move(0, -1)
        if keys[pygame.K_DOWN]:
            pacman.move(0, 1)
        if keys[pygame.K_LEFT]:
            pacman.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            pacman.move(1, 0)

        # Movimentação dos fantasmas
        for ghost in ghosts:
            ghost.move()

        # Verifica colisão com pontos
        row = pacman.y // tile_size
        col = pacman.x // tile_size
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == ".":
            maze[row] = maze[row][:col] + " " + maze[row][col+1:]
            score += 10

        # Verifica se todas as bolinhas foram comidas
        if todas_bolinhas_comidas():
            victory = True

        # Verifica colisão com fantasmas
        for ghost in ghosts:
            if pacman.x == ghost.x and pacman.y == ghost.y:
                game_over = True

    # Desenha o labirinto, o Pac-Man e os fantasmas
    screen.fill(BLACK)
    draw_maze()
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()

    # Exibe a pontuação
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Tela de Game Over
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 20))

    # Tela de Vitória
    if victory:
        victory_text = font.render("VICTORY!", True, WHITE)
        screen.blit(victory_text, (WIDTH // 2 - 70, HEIGHT // 2 - 20))

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(10)  # Controla a taxa de atualização