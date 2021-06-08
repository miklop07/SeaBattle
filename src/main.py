# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import queue
from ships import Ships

WIDTH = 1280
HEIGHT = 720
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
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
        self.image = pygame.Surface((30 * 11, 30 * 11))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.font_size = 20
        self.font = pygame.font.SysFont("Monospace", self.font_size, bold=True)
        self.draw_grid()
        self.nums_letters()
        self.flag = 2

    def draw_grid(self):
        for i in range(1, 11):
            pygame.draw.line(self.image, BLACK, (30, i * 30), (30 * 11, i * 30))
            pygame.draw.line(self.image, BLACK, (i * 30, 30), (30 * i, 11 * 30))
    
    def nums_letters(self):
        letters = ['A','B','C','D','E','F','G','H','I','J']
        for i in range (10):
            nums = self.font.render(str(i + 1), True, BLACK)
            lets = self.font.render(letters[i], True, BLACK)
            nums_width = nums.get_width()
            nums_height = nums.get_height()
            lets_width = lets.get_width()
            lets_height = lets.get_height()

            self.image.blit(nums, (5, 35 + i * 30))
            self.image.blit(lets, (40 + i * 30, 5))

    def draw_ships(self, ships_list = None):
        if self.flag:
            print("\nDRAWING\n", ships_list)
        for ship in ships_list:
            forward_ship = sorted(ship)
            if self.flag:
                print("SORTED ", forward_ship)
                self.flag -= 1
            x_0 = forward_ship[0][0]
            y_0 = forward_ship[0][1]
            ship_width = 30
            ship_height = 30
            if (len(forward_ship) != 1) and forward_ship[0][0] == forward_ship[1][0]:
                ship_height *= len(forward_ship)
            else:
                ship_width *= len(forward_ship)
            x = 30 * x_0
            y = 30 * y_0
            pygame.draw.rect(self.image, GREY, ((x, y), (ship_width, ship_height)), width=3)


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

player1_deck = PlayerDeck(120, 60)
all_sprites.add(player1_deck)

player2_deck = PlayerDeck(180 + 11 * 30, 60)
all_sprites.add(player2_deck)

log_deck = LogDeck()
all_sprites.add(log_deck)

menu_deck = MenuDeck()
all_sprites.add(menu_deck)
# all_sprites.add(player)

player1_ships = Ships()
player2_ships = Ships()

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
    player1_deck.draw_ships(player1_ships.ships_list)
    player2_deck.draw_ships(player2_ships.ships_list)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()