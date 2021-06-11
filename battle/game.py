import pygame
import battle.constants as constants
from battle.log_deck import LogDeck
from battle.menu_deck import MenuDeck
from battle.gamelogic import ForPlayer


class PlayerDeck(pygame.sprite.Sprite):
    """Class for player's game fields were all ships are shown"""
    def __init__(self, x_pos, y_pos):
        super(PlayerDeck, self).__init__()
        self.image = pygame.Surface((30 * 11, 30 * 11))
        self.image.fill(constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.font_size = 20
        self.font = pygame.font.SysFont("Monospace", self.font_size, bold=True)
        self.draw_grid()
        self.nums_letters()

    def draw_grid(self):
        for i in range(1, 11):
            pygame.draw.line(self.image, constants.BLACK, (30, i * 30), (30 * 11, i * 30))
            pygame.draw.line(self.image, constants.BLACK, (i * 30, 30), (30 * i, 11 * 30))

    def nums_letters(self):
        letters = "ABCDEFGHIJ"
        for i in range(10):
            nums = self.font.render(str(i + 1), True, constants.BLACK)
            lets = self.font.render(letters[i], True, constants.BLACK)

            self.image.blit(nums, (5, 35 + i * 30))
            self.image.blit(lets, (40 + i * 30, 5))

    def draw_ships(self, ships_list=None, killed_ships=[], show=True):
        if not ships_list:
            return
        for ship in ships_list:
            forward_ship = sorted(ship)
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
            color = constants.GREY
            if ship in killed_ships:
                color = constants.RED
            if show or color == constants.RED:
                pygame.draw.rect(self.image, color, ((x, y), (ship_width, ship_height)), width=3)

    def draw_dots(self, dot_set=set()):
        """To mark all empry cells on the field"""
        for dot in dot_set:
            x_pos = 30 * (dot[0]) + 15
            y_pos = 30 * (dot[1]) + 15
            pygame.draw.circle(self.image, constants.BLACK, (x_pos, y_pos), 5)

    def draw_killed(self, kill_set=set()):
        """To mark ships which were hit"""
        for block in kill_set:
            x = block[0] * 30
            y = block[1] * 30
            pygame.draw.line(self.image, constants.BLACK, (x, y), (x + 30, y + 30), 5)
            pygame.draw.line(self.image, constants.BLACK, (x + 30, y), (x, y + 30), 5)

    def renew(self):
        self.image.fill(constants.WHITE)
        self.draw_grid()
        self.nums_letters()


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
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
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

    comp = ForPlayer(random_mode=True)
    pl = ForPlayer(random_mode=False)

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
                elif menu_deck.button_start.is_mouse_on_button():
                    player1_deck.renew()
                    player2_deck.renew()
                    comp = ForPlayer(random_mode=True)
                    comp.add_ships()
                    pl = ForPlayer(random_mode=False)
                    pl.add_ships()
                    comp.add_opponent_list(pl.ships.ships_list)
                    pl.add_opponent_list(comp.ships.ships_list)
                    player1_deck.draw_ships(pl.ships.ships_list)
                    player2_deck.draw_ships(comp.ships.ships_list, show=False)
                else:
                    if not comp.turn:
                        x, y = event.pos
                        block_to_fire = pl.find_fired_block(x, y)
                        if block_to_fire is not None:
                            is_hit, killed, ind = pl.perform_fire(block_to_fire)
                            if is_hit:
                                comp.ships.ships.discard(block_to_fire)
                                if killed:
                                    comp.killed.append(comp.ships.ships_list[ind])
                            else:
                                comp.turn = True
                            letter = "ABCDEFGHIJ"[block_to_fire[0] - 1]
                            digit = block_to_fire[1]
                            res = '-'
                            if is_hit:
                                res = "+"
                                if killed:
                                    res = "++"
                            log_deck.add_record(f"Player1 {letter}{digit}{res}")

        # Обновление
        all_sprites.update()

        # Отрисовка
        screen.fill(constants.WHITE)
        all_sprites.draw(screen)
        log_deck.draw(screen)
        menu_deck.draw(screen)

        player2_deck.draw_dots(pl.empty_blocks)
        player1_deck.draw_dots(comp.empty_blocks)
        player2_deck.draw_killed(pl.hit_blocks)
        player1_deck.draw_killed(comp.hit_blocks)
        player1_deck.draw_ships(pl.ships.ships_list, pl.killed)
        player2_deck.draw_ships(comp.ships.ships_list, comp.killed, show=False)

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

        if comp.turn:
            block_to_fire = comp.random_fire()
            is_hit, killed, ind = comp.perform_fire(block_to_fire)
            if is_hit:
                pl.ships.ships.discard(block_to_fire)
                if killed:
                    pl.killed.append(pl.ships.ships_list[ind])
            else:
                comp.turn = False
            letter = "ABCDEFGHIJ"[block_to_fire[0] - 1]
            digit = block_to_fire[1]
            res = '-'
            if is_hit:
                res = "+"
                if killed:
                    res = "++"
            log_deck.add_record(f"Player2 {letter}{digit}{res}")

    pygame.quit()
