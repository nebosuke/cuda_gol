#!/usr/bin/env python3
import numpy
import curses
from curses import wrapper

row2str = lambda row: ''.join(['O' if c != 0 else ' ' for c in row])
cell_value = lambda world, height, width, y, x: world[y % height, x % width]

def print_world(stdscr, world):
    height, width = world.shape
    for y in range(height):
        row = world[y]
        stdscr.addstr(y, 0, row2str(row))
    stdscr.refresh()

def set_next_cell_value(world, next_world, height, width, y, x):
    current_value = cell_value(world, height, width, y, x)
    next_value = current_value
    num_live = 0
    num_live += cell_value(world, height, width, y - 1, x - 1)
    num_live += cell_value(world, height, width, y - 1, x    )
    num_live += cell_value(world, height, width, y - 1, x + 1)
    num_live += cell_value(world, height, width, y    , x - 1)
    num_live += cell_value(world, height, width, y    , x + 1)
    num_live += cell_value(world, height, width, y + 1, x - 1)
    num_live += cell_value(world, height, width, y + 1, x    )
    num_live += cell_value(world, height, width, y + 1, x + 1)
    if current_value == 0 and num_live == 3:
        next_value = 1
    elif current_value == 1 and num_live in (2, 3):
        next_value = 1
    else:
        next_value = 0
    next_world[y, x] = next_value

def calc_next_world_cpu(world, next_world):
    height, width = world.shape
    for y in range(height):
        for x in range(width):
            set_next_cell_value(world, next_world, height, width, y, x)

def game_of_life(stdscr, height, width):
    # 世界の初期値
    world = numpy.random.randint(2, size=(height, width), dtype=numpy.int32)

    # 次の世代の世界を保持する２次元配列
    next_world = numpy.empty((height, width), dtype=numpy.int32)

    while True:
        print_world(stdscr, world)
        calc_next_world_cpu(world, next_world)
        world, next_world = next_world, world

def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    scr_height, scr_width = stdscr.getmaxyx()
    game_of_life(stdscr, scr_height - 1, scr_width)

if __name__ == '__main__':
    curses.wrapper(main)
