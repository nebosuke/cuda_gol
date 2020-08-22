#!/usr/bin/env python3
import numpy
import curses
from curses import wrapper
import time

row2str = lambda row: ''.join(['O' if c != 0 else ' ' for c in row])
cell_value = lambda world, height, width, y, x: world[y % height, x % width]
cell_value_3d = lambda world, depth, height, width, z, y, x: world[z % depth, y % height, x % width]

def print_world(stdscr, world, generation, elapsed):
    depth, height, width = world.shape
    plane = world[0]
    for y in range(height):
        row = plane[y]
        stdscr.addstr(y, 0, row2str(row))
    stdscr.addstr(height, 0, "Generation: %06d, Elapsed: %.6f[sec]" % (generation, elapsed / generation), curses.A_REVERSE)
    stdscr.refresh()

def set_next_cell_value(world, next_world, depth, height, width, z, y, x):
    current_value = cell_value_3d(world, depth, height, width, z, y, x)
    next_value = current_value
    num_live = 0

    num_live += cell_value_3d(world, depth, height, width, z - 1, y - 1, x - 1)
    num_live += cell_value_3d(world, depth, height, width, z - 1, y - 1, x    )
    num_live += cell_value_3d(world, depth, height, width, z - 1, y - 1, x + 1)
    num_live += cell_value_3d(world, depth, height, width, z - 1, y    , x - 1)
    num_live += cell_value_3d(world, depth, height, width, z - 1, y    , x    )
    num_live += cell_value_3d(world, depth, height, width, z - 1, y    , x + 1)
    num_live += cell_value_3d(world, depth, height, width, z - 1, y + 1, x - 1)
    num_live += cell_value_3d(world, depth, height, width, z - 1, y + 1, x    )
    num_live += cell_value_3d(world, depth, height, width, z - 1, y + 1, x + 1)

    num_live += cell_value_3d(world, depth, height, width, z    , y - 1, x - 1)
    num_live += cell_value_3d(world, depth, height, width, z    , y - 1, x    )
    num_live += cell_value_3d(world, depth, height, width, z    , y - 1, x + 1)
    num_live += cell_value_3d(world, depth, height, width, z    , y    , x - 1)
    num_live += cell_value_3d(world, depth, height, width, z    , y    , x + 1)
    num_live += cell_value_3d(world, depth, height, width, z    , y + 1, x - 1)
    num_live += cell_value_3d(world, depth, height, width, z    , y + 1, x    )
    num_live += cell_value_3d(world, depth, height, width, z    , y + 1, x + 1)

    num_live += cell_value_3d(world, depth, height, width, z + 1, y - 1, x - 1)
    num_live += cell_value_3d(world, depth, height, width, z + 1, y - 1, x    )
    num_live += cell_value_3d(world, depth, height, width, z + 1, y - 1, x + 1)
    num_live += cell_value_3d(world, depth, height, width, z + 1, y    , x - 1)
    num_live += cell_value_3d(world, depth, height, width, z + 1, y    , x    )
    num_live += cell_value_3d(world, depth, height, width, z + 1, y    , x + 1)
    num_live += cell_value_3d(world, depth, height, width, z + 1, y + 1, x - 1)
    num_live += cell_value_3d(world, depth, height, width, z + 1, y + 1, x    )
    num_live += cell_value_3d(world, depth, height, width, z + 1, y + 1, x + 1)

    if current_value == 0 and num_live == 3:
         next_value = 1
    elif current_value == 1 and num_live in (2, 15):
         next_value = 1
    else:
         next_value = 0

    next_world[z, y, x] = next_value

def calc_next_3d_world_cpu(world, next_world):
    depth, height, width = world.shape
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                set_next_cell_value(world, next_world, depth, height, width, z, y, x)

def game_of_life(stdscr, depth, height, width):
    # 世界の初期値
    world = numpy.random.randint(2, size=(depth, height, width), dtype=numpy.int32)

    # 次の世代の世界を保持する３次元配列
    next_world = numpy.empty((depth, height, width), dtype=numpy.int32)

    elapsed = 0.0
    generation = 0
    while True:
        generation += 1
        print_world(stdscr, world, generation, elapsed)
        start_time = time.time()
        calc_next_3d_world_cpu(world, next_world)
        duration = time.time() - start_time
        elapsed += duration
        world, next_world = next_world, world

def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    scr_height, scr_width = stdscr.getmaxyx()
    game_of_life(stdscr, 10, scr_height - 1, scr_width)

if __name__ == '__main__':
    curses.wrapper(main)
