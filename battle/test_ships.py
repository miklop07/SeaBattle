import pygame
from battle.ships import Ships

def test_ships_empty():
    ships = Ships(no_ships=True)
    assert ships.ships_list == []

def test_ships_start():
    ships = Ships(no_ships=False)
    x, y, is_vertical, direction = ships.choose_start(ships.available_blocks)
    assert 0 < x < 11 and 0 < y < 11

def test_add():
    ships = Ships(no_ships=False)
    direction, x = ships.add_block_to_ship(10, 1, 0, [(10, 5)])
    assert direction == -1
    assert x == 9

def test_ships_create():
    ships = Ships(no_ships=False)
    x, y, is_vertical, direction = ships.choose_start(ships.available_blocks)
    coords = ships.create_one_ship(4, ships.available_blocks)

    assert len(coords) == 4
    coords = sorted(coords)
    dif1 = abs(coords[1][0] - coords[2][0])
    dif2 = abs(coords[1][1] - coords[2][1])
    assert (dif1 == 0 and dif2 == 1) or (dif1 == 1 and dif2 == 0) 

