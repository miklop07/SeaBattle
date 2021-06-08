import random

class Ships:
    def __init__(self):
        self.available_blocks = set((x, y) for x in range (1, 11) for y in range (1, 11))
        self.ships = set()
        self.ships_list = self.create_all_ships()

    def choose_start(self, available_blocks):
        is_vetrical = random.randint(0, 1)
        direction = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, is_vetrical, direction

    def add_block_to_ship(self, pos, direction, is_vetrical, coords):
        if (pos <= 1 and direction == -1) or (pos >= 10 and direction == 1):
            direction *= -1 
            return direction, coords[0][is_vetrical] + direction
        else:
            return direction, coords[-1][is_vetrical] + direction

    def add_to_set(self, ship):
        for block in ship:
            self.ships.add(block)

    def close_near_position(self, ship):
        for block in ship:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = min(10, max(1, block[0] + i))
                    y = min(10, max(1, block[1] + j))
                    # print("delete", (x, y))
                    self.available_blocks.discard((x, y))

    def create_one_ship(self, length_of_ship, available_blocks):
        coords = []
        x, y, is_vetrical, direction = self.choose_start(available_blocks)
        for _ in range(length_of_ship):
            coords.append((x, y))
            if not is_vetrical:
                direction, x = self.add_block_to_ship(x, direction, is_vetrical, coords)
            else:
                direction, y = self.add_block_to_ship(y, direction, is_vetrical, coords)
        if self.is_free_place(coords):
            return coords
        else:
            return self.create_one_ship(length_of_ship, available_blocks)

    def create_all_ships(self):
        ships_coords_list = []
        # reverse order of sizes because big ships are harder to set
        for length_of_ship in range(4, 0, -1):
            amount_of_ships = 5 - length_of_ship
            for _ in range(amount_of_ships):
                ship = self.create_one_ship(length_of_ship, self.available_blocks)
                ships_coords_list.append(ship)
                self.add_to_set(ship)
                self.close_near_position(ship)
        return(ships_coords_list)

    def is_free_place(self, coords):
        set_coords = set(coords)
        return set_coords.issubset(self.available_blocks)

