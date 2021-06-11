"""LogDeck module."""

import pygame
import battle.constants as constants


class LogDeck(pygame.sprite.Sprite):
    """docstring for LogDeck."""

    def __init__(self):
        """docstring."""
        super(LogDeck, self).__init__()
        self.width = 30 * 9
        self.height = 30 * 13
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(constants.WHITE)

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
        """Docstring for update."""
        pass

    def draw(self, screen):
        """Docstring for draw."""
        right_border = None if self.bound == 0 else -self.bound
        for position, record in enumerate(self.log_list[-self.max_records - self.bound:right_border]):
            screen.blit(
                self.font.render(record, False, constants.BLACK),
                (
                    self.rect.x + self.padding[0],
                    self.rect.y + self.padding[1] + (self.font_size / 2 + self.record_interval) * position
                )
            )

    def add_record(self, record):
        """Docstring for add_record."""
        self.log_list.append(record)
        if self.bound != 0:
            self.scroll_up()

    def scroll_up(self):
        """Docstring for scroll_up."""
        if self.max_records + self.bound < len(self.log_list):
            self.bound += 1

    def scroll_down(self):
        """Docstring for scroll_down."""
        if self.bound > 0:
            self.bound -= 1
