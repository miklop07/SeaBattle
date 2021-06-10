import pygame
import constants
from log_deck import LogDeck
from menu_deck import MenuDeck


class PlayerDeck(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super(PlayerDeck, self).__init__()
        self.image = pygame.Surface((30 * 10, 30 * 10))
        self.image.fill(constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos


class GameDeck(pygame.sprite.Sprite):
    """docstring for GameDeck"""
    def __init__(self):
        super(GameDeck, self).__init__()
        self.image = pygame.Surface((30 * 13 * 2, 30 * 13))
        self.image.fill(constants.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 30
        # self.rect.center = (WIDTH / 2, HEIGHT / 2)


def main():
    # Создаем игру и окно
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
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
    all_sprites.add(log_deck.border)
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
        clock.tick(constants.FPS)
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
        screen.fill(constants.WHITE)
        all_sprites.draw(screen)

        log_deck.draw(screen)
        menu_deck.draw(screen)

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
