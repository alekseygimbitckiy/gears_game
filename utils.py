import math
import random

WIDTH, HEIGHT = 800, 600
FPS = 60
GEAR_RADIUS = 50
GEAR_WIDTH = 20  # Ширина шестерёнки
HOLE_RADIUS = 10

FIGURE_RADIUS = 10
FIGURE_DIR_RADIUS = 30

NUM_FIGURES = 8

SWAP_DIST = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)

fig_types = ['rect', 'circle', 'triangle']

NUM_SWAPS = 10

def calc_figure_s_alpha(indx, num_figures):
    return 360 * indx/num_figures

def calculate_distance(point_A, point_B):
    return math.sqrt((point_B[0] - point_A[0]) ** 2 + (point_B[1] - point_A[1]) ** 2)

def gen_level(gears, num_swaps = 1):
    for i in range(num_swaps):
        gear_ind = random.randint(0, len(gears) - 1)
        step = random.randint(1, gears[gear_ind].num_figures)
        dirr = 2 * random.randint(0, 1) - 1 #have only left and right dirrection soon
        if gear_ind == 0:
            dirr = 1
        elif gear_ind == len(gears) - 1:
            dirr = -1
        gears[0].rotate(dirr * step)
        gears[gear_ind].swap_fig(dirr)
        print(i, ". rotated", dirr * step, "and swaped", gear_ind ,"with", ["left", "right"][(dirr + 1)//2], "gear")

def check_win(gears):
    for gear in gears:
        current_shape = gear.figures[0].shape
        for fig in gear.figures:
            if fig.shape != current_shape:
                return False
    
    return True
