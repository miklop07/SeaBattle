import copy
from ships import Ships


class ForPlayer():
    def __init__(self, random_mode):
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
        self.opponent_ships = copy.deepcopy(ships)

    def add_ships(self):
        self.ships = Ships()

    def random_fire(self):
        # short delay just to see the moment of shooting
        pygame.time.delay(500)
        if self.near_blocks:
            choose_from = self.near_blocks
        else:
            choose_from = self.all_blocks
        fired_block = random.choice(tuple(choose_from))
        self.all_blocks.discard(fired_block)
        return perform_fire(fired_block)

    def find_fired_block(self, x, y):
        left = 180 + 12 * 30
        up = 90
        if (left <= x <= left + 10 * 30) and (up <= y <= up + 10 * 30):
            block_to_fire = ((x - left) // 30 + 1, (y - up) // 30 + 1)
            print("ok", block_to_fire)
            return block_to_fire

    def update_sets(self, fired_block, is_killed):
        self.all_blocks.discard(fired_block)
        self.hit_blocks.add(fired_block)
        print("HITTED ", self.hit_blocks)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (is_killed and (i or j)) or (is_killed and i and j):
                    x = min(10, max(1, fired_block[0] + i))
                    y = min(10, max(1, fired_block[1] + j))
                    self.empty_blocks.add((x, y))

    def update_last_hit(self, fired_block, is_killed):
        pass

    def put_dot(self, block):
        print("EMPTY ", block)
        self.empty_blocks.add(block)

    def perform_fire(self, block):
        print("fire ", block)
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
                print("SHIP ", ship)
                if self.random_mode:
                    self.last_hit_list.append(block)
                    self.update_last_hit()
                if ship == []:
                    if self.random_mode:
                        self.last_hit_list.clear()
                        self.near_blocks.clear()
                    is_killed = True

        if not is_hit:
            self.put_dot(block)
        if self.random_mode:
            self.update_last_hit(block)
        return is_hit, is_killed, ind




