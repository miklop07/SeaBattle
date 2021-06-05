# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import queue

WIDTH = 1280
HEIGHT = 720
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((50, 50))
#         self.image.fill(GREEN)
#         self.rect = self.image.get_rect()
#         self.rect.center = (WIDTH / 2, HEIGHT / 2)

#     def update(self):
#         self.rect.x += 5
#         if self.rect.left > WIDTH:
#             self.rect.right = 0

class PlayerDeck(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super(PlayerDeck, self).__init__()
        self.image = pygame.Surface((30 * 10, 30 * 10))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

class GameDeck(pygame.sprite.Sprite):
    """docstring for GameDeck"""
    def __init__(self):
        super(GameDeck, self).__init__()
        self.image = pygame.Surface((30 * 13 * 2, 30 * 13))
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 30
        # self.rect.center = (WIDTH / 2, HEIGHT / 2)

class LogDeck(pygame.sprite.Sprite):
    """docstring for GameDeck"""
    def __init__(self):
        super(LogDeck, self).__init__()
        self.image = pygame.Surface((30 * 7, 30 * 13))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = 30 * 13 * 2 + 90 + 30
        self.rect.y = 30

        self.log_list = queue.Queue()
        # self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        if not self.log_list.empty():
            self.draw_record(self.log_list.get())

    def draw_record(self):
        pass

    def add_record(self, record):
        log_list.put(record)

class MenuDeck(pygame.sprite.Sprite):
    def __init__(self):
        super(MenuDeck, self).__init__()
        self.image = pygame.Surface((30 * 13 * 2, 30 * 5))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 30 + 30 * 13 + 60

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# player = Player()
game_deck = GameDeck()
all_sprites.add(game_deck)

player1_deck = PlayerDeck(150, 90)
all_sprites.add(player1_deck)

player2_deck = PlayerDeck(210 + 11 * 30, 90)
all_sprites.add(player2_deck)

log_deck = LogDeck()
all_sprites.add(log_deck)

menu_deck = MenuDeck()
all_sprites.add(menu_deck)
# all_sprites.add(player)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()