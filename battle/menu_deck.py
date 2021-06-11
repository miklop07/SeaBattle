"""Menu module."""

import pygame
import battle.constants as constants
from battle.interface import Button
import gettext

gettext.install("battle", localedir="po")


class MenuDeck(pygame.sprite.Sprite):
    """docstring for LogDeck."""

    def __init__(self):
        """docstring."""
        super(MenuDeck, self).__init__()
        self.width = 30 * 13 * 2
        self.height = 30 * 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 30 + 30 * 13 + 60

        self.button_start = Button(
            width=30 * 8,
            height=30 * 3,
            x_pos=self.rect.x + 15 * 5,
            y_pos=self.rect.y + 30,
            color=constants.WHITE,
            text=_("New game"),
            text_color=constants.BLACK
        )

        self.button_exit = Button(
            width=30 * 8,
            height=30 * 3,
            x_pos=self.rect.x + 15 * 5 + 30 * 13,
            y_pos=self.rect.y + 30,
            color=constants.WHITE,
            text=_("Exit"),
            text_color=constants.BLACK
        )

    def draw(self, screen):
        """docstring."""
        self.button_start.draw(screen)
        self.button_exit.draw(screen)
