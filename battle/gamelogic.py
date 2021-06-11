"""Logic module."""
import copy
import pygame
import random
from battle.ships import Ships


class ForPlayer():
    """Class with all neccessary player's info."""

    def __init__(self, random_mode):
        """docstring."""
        self.all_blocks = set((a, b) for a in range(1, 11) for b in range(1, 11))
        self.turn = False
        self.random_mode = random_mode
        self.near_blocks = set()
        self.empty_blocks = set()
        self.hit_blocks = set()
        self.last_hit_list = list()
        self.killed = list()
        self.ships = Ships(True)
        self.opponent_ships = None

    def add_opponent_list(self, ships):
        """docstring."""
        self.opponent_ships = copy.deepcopy(ships)

    def add_ships(self):
        """docstring."""
        self.ships = Ships()

    def random_fire(self):
        """Choose block to shoot randomly."""
        # short delay just to see the moment of shooting
        pygame.time.delay(500)
        if self.near_blocks:
            choose_from = self.near_blocks
        else:
            choose_from = self.all_blocks
        fired_block = random.choice(tuple(choose_from))
        self.all_blocks.discard(fired_block)
        return fired_block

    def find_fired_block(self, x, y):
        """docstring."""
        left = 180 + 12 * 30
        up = 90
        if (left <= x <= left + 10 * 30) and (up <= y <= up + 10 * 30):
            block_to_fire = ((x - left) // 30 + 1, (y - up) // 30 + 1)
            return block_to_fire

    def update_sets(self, fired_block, is_killed):
        """Update sets of known empty cells, hit places and possible blocks to shoot."""
        self.all_blocks.discard(fired_block)
        self.hit_blocks.add(fired_block)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i and j):
                    x = fired_block[0] + i
                    y = fired_block[1] + j
                    if (0 < x < 11) and (0 < y < 11):
                        self.empty_blocks.add((x, y))
                        self.all_blocks.discard((x, y))
                elif is_killed:
                    if i or j:
                        x = fired_block[0] + i
                        y = fired_block[1] + j
                        while (x, y) in self.hit_blocks:
                            x += i
                            y += j
                        if (0 < x < 11) and (0 < y < 11):
                            self.empty_blocks.add((x, y))
                            self.all_blocks.discard((x, y))

    def update_last_hit(self, fired_block, missed):
        """For computer player, to fire near previous place is there was hit."""
        if missed:
            self.near_blocks.discard(fired_block)
            return
        near = []
        shift = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for i in range(4):
            near.append((fired_block[0] + shift[i][0], fired_block[1] + shift[i][1]))
        if not self.near_blocks:
            for n in near:
                if (0 < n[0] < 11) and (0 < n[1] < 11):
                    if n not in self.empty_blocks and n not in self.hit_blocks:
                        self.near_blocks.add(n)
            return
        self.near_blocks.clear()
        for i in range(4):
            if near[i] in self.hit_blocks:
                x = near[i][0]
                y = near[i][1]
                while (x, y) in self.hit_blocks:
                    x += shift[i][0]
                    y += shift[i][1]
                if (0 < x < 11) and (0 < y < 11) and (x, y) not in self.empty_blocks:
                    self.near_blocks.add((x, y))
                x = near[i][0]
                y = near[i][1]
                while (x, y) in self.hit_blocks:
                    x -= shift[i][0]
                    y -= shift[i][1]
                if (0 < x < 11) and (0 < y < 11) and (x, y) not in self.empty_blocks:
                    self.near_blocks.add((x, y))
                break

    def put_dot(self, block):
        """docstring."""
        self.empty_blocks.add(block)

    def perform_fire(self, block):
        """docstring."""
        is_hit = False
        ind = -1
        is_killed = False
        for ship in self.opponent_ships:
            if block in ship:
                is_hit = True
                self.update_sets(block, is_killed=False)
                if len(ship) == 1:
                    self.update_sets(block, is_killed=True)
                ind = self.opponent_ships.index(ship)
                ship.remove(block)
                if ship == []:
                    if self.random_mode:
                        self.last_hit_list.clear()
                        self.near_blocks.clear()
                    is_killed = True
                else:
                    if self.random_mode:
                        self.last_hit_list.append(block)
                        self.update_last_hit(block, missed=False)

        if not is_hit:
            self.put_dot(block)
            if self.random_mode:
                self.update_last_hit(block, missed=True)
        return is_hit, is_killed, ind
