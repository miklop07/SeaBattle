import pygame

WIDTH = 1280
HEIGHT = 720
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


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
    """docstring for LogDeck"""
    def __init__(self):
        super(LogDeck, self).__init__()
        self.width = 30 * 9
        self.height = 30 * 13
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = 30 * 13 * 2 + 90 + 30
        self.rect.y = 30

        self.log_list = []
        self.max_records = 12
        self.bound = 0

        self.font_size = 30
        self.font = pygame.font.SysFont("Monospace", self.font_size, bold=True)

        self.padding = 20, 15
        self.record_interval = 15

    def update(self):
        pass

    def draw(self, screen):
        right_border = None if self.bound == 0 else -self.bound
        for position, record in enumerate(self.log_list[-self.max_records - self.bound:right_border]):
            screen.blit(
                self.font.render(record, False, BLACK),
                (
                    self.rect.x + self.padding[0],
                    self.rect.y + self.padding[1] + (self.font_size / 2 + self.record_interval) * position
                )
            )

    def add_record(self, record):
        self.log_list.append(record)
        if self.bound != 0:
            self.scroll_up()

    def scroll_up(self):
        if self.max_records + self.bound < len(self.log_list):
            self.bound += 1

    def scroll_down(self):
        if self.bound > 0:
            self.bound -= 1


class Border(pygame.sprite.Sprite):
    def __init__(self, distance=(10, 10), center=(0, 0), thickness=5, color=BLACK):
        super(Border, self).__init__()
        self.thickness = thickness
        self.image = pygame.Surface((distance[0] + thickness, distance[1] + thickness))
        self.image.fill(color)

        self.rect = self.image.get_rect(center=center)


class Button(pygame.sprite.Sprite):
    def __init__(self, width=10, height=10, color=(BLACK), x_pos=0, y_pos=0, text="", text_color=WHITE):
        super(Button, self).__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

        self.font_size = 30
        self.font = pygame.font.SysFont("Monospace", self.font_size, bold=True)
        self.text = self.font.render(text, False, text_color)

        self.padding = (width - len(text) * width // 13) // 2

        self.border = Border(
            distance=(self.width, self.height),
            center=self.rect.center,
            thickness=10,
            color=BLACK
        )

    def draw(self, screen):
        screen.blit(self.text, (self.rect.x + self.padding, self.rect.y + self.font_size))

    def is_mouse_on_button(self):
        m_x, m_y = pygame.mouse.get_pos()
        if m_x >= self.rect.x and m_x <= self.rect.x + self.width and \
           m_y >= self.rect.y and m_y <= self.rect.y + self.height:
            return True
        else:
            return False


class MenuDeck(pygame.sprite.Sprite):
    def __init__(self):
        super(MenuDeck, self).__init__()
        self.width = 30 * 13 * 2
        self.height = 30 * 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 30 + 30 * 13 + 60

        self.button_start = Button(
            width=30 * 8,
            height=30 * 3,
            x_pos=self.rect.x + 15 * 5,
            y_pos=self.rect.y + 30,
            color=WHITE,
            text="New game",
            text_color=BLACK
        )

        self.button_exit = Button(
            width=30 * 8,
            height=30 * 3,
            x_pos=self.rect.x + 15 * 5 + 30 * 13,
            y_pos=self.rect.y + 30,
            color=WHITE,
            text="Exit",
            text_color=BLACK
        )

    def draw(self, screen):
        self.button_start.draw(screen)
        self.button_exit.draw(screen)


def main():
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
    all_sprites.add(menu_deck.button_start.border)
    all_sprites.add(menu_deck.button_start)
    all_sprites.add(menu_deck.button_exit.border)
    all_sprites.add(menu_deck.button_exit)

    pygame.font.init()

    debug_var = 0

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    log_deck.scroll_up()
                elif event.key == pygame.K_DOWN:
                    log_deck.scroll_down()
                elif event.key == pygame.K_a:
                    log_deck.add_record(f"Player1 A{debug_var} +")
                    debug_var += 1
                elif event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_deck.button_exit.is_mouse_on_button():
                    running = False

        # Обновление
        all_sprites.update()

        # Отрисовка
        screen.fill(WHITE)
        all_sprites.draw(screen)

        log_deck.draw(screen)
        menu_deck.draw(screen)

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
