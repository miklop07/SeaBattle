import pygame
import constants


class Border(pygame.sprite.Sprite):
    def __init__(self, distance=(10, 10), center=(0, 0), thickness=5, color=constants.BLACK):
        super(Border, self).__init__()
        self.thickness = thickness
        self.image = pygame.Surface((distance[0] + thickness, distance[1] + thickness))
        self.image.fill(color)

        self.rect = self.image.get_rect(center=center)


class Button(pygame.sprite.Sprite):
    def __init__(self, width=10, height=10, color=(constants.BLACK), x_pos=0, y_pos=0, text="", text_color=constants.WHITE):
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
            color=constants.BLACK
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
