import pygame
import sys
import math

from gear import Gear
from figure import Figure
from gear_draw import Gear_draw
# from figure_draw import Figure_draw
from utils import *

#preraration
def draw():
    for d_gear in d_gears:
        print(d_gear.gear.figures)

def check_id():
    for i, d_gear in enumerate(d_gears):
        for j, figure in enumerate(d_gear.gear.figures):
            if id(figure) != id(gears[i].figures[j]):
                print(i, j)

# gear_0 = Gear(0, NUM_FIGURES, [Figure("rect"), Figure("rect"), Figure("rect"), Figure("rect")], 0)
# gear_1 = Gear(1, NUM_FIGURES, [Figure("circle"), Figure("circle"), Figure("circle"), Figure("circle")], 0)
# gear_2 = Gear(2, NUM_FIGURES, [Figure("triangle"), Figure("triangle"), Figure("triangle"), Figure("triangle")], 0)

gear_0 = Gear(NUM_FIGURES, 0, "circle")
gear_1 = Gear(NUM_FIGURES, 0, "circle")
gear_2 = Gear(NUM_FIGURES, 0, "triangle")
gear_3 = Gear(NUM_FIGURES, 0, "rect")

gears = [gear_0, gear_1, gear_2, gear_3]

gears_h = [gear_1, gear_2, gear_3]#TODO:generalize for all cases
gears_v = [gear_0, gear_2]
for i in range(len(gears_h) - 1):
    gears_h[i].neighbors['r'] = gears_h[i+1]

for i in range(len(gears_h) - 1, 0, -1):
    gears_h[i].neighbors['l'] = gears_h[i-1]

for i in range(len(gears_v) - 1):
    gears_v[i].neighbors['d'] = gears_v[i + 1]

for i in range(len(gears_v) - 1, 0, -1):
    gears_v[i].neighbors['u'] = gears_v[i-1]

# d_gears_c = [(WIDTH // 2 - GEAR_RADIUS, HEIGHT // 2 - GEAR_RADIUS), (WIDTH // 2 + GEAR_RADIUS, HEIGHT // 2 - GEAR_RADIUS), (WIDTH // 2 + GEAR_RADIUS, HEIGHT // 2 + GEAR_RADIUS),\
#              (WIDTH // 2 - GEAR_RADIUS, HEIGHT // 2 + GEAR_RADIUS)]
d_gears_c = []
d_gears_c.append((WIDTH // 2, HEIGHT // 2 - 2 * GEAR_RADIUS))
for i in range(len(gears)):
    d_gears_c.append((WIDTH // 2 - 2 * GEAR_RADIUS + 2 * i * GEAR_RADIUS, HEIGHT // 2))

d_gears = [Gear_draw(gears[i], d_gears_c[i][0], d_gears_c[i][1]) for i in range(len(gears))]


SWAP_POINTS = [((d_gears[i].x + d_gears[i+1].x)//2, (d_gears[i].y + d_gears[i+1].y)//2) for i in range(len(d_gears) - 1)]
# SWAP_POINTS = [((d_gears_c[i % len(gears)][0] + d_gears_c[(i + 1)%len(gears)][0])//2, (d_gears_c[i % len(gears)][1] + d_gears_c[(i + 1)%len(gears)][1])//2) for i in range(len(gears) - 1)]
SWAP_POINTS[2] = [(d_gears[0].x + d_gears[2].x)//2, (d_gears[0].y + d_gears[2].y)//2]
points_gears = {}
points_swap_dir = {}
for i, s_p in enumerate(SWAP_POINTS):
    points_gears[i] = []
    for j, d_g in enumerate(d_gears):
        if s_p[0] == d_g.x:
            points_gears[i].append(j)
    points_swap_dir[i] = 'v'
    if len(points_gears[i]) == 0:
        for j, d_g in enumerate(d_gears):
            if s_p[1] == d_g.y:
                points_gears[i].append(j)
        points_swap_dir[i] = 'h'
print(points_gears)
print(points_swap_dir)

gen_level(gears, NUM_SWAPS)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Гонки шестерёнок")

def main():
    mouse_presed = False
    left_presed = False
    right_presed = False
    down_presed = False
    up_presed = False
    #end preparation

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_presed = True
            elif event.key == pygame.K_RIGHT:
                right_presed = True
            elif event.key == pygame.K_DOWN:
                down_presed = True
            elif event.key == pygame.K_UP:
                up_presed = True

        if event.type == pygame.KEYUP:
            if left_presed and event.key == pygame.K_LEFT:
                gears[1].rotate(-1)
                left_presed = False
            elif right_presed and event.key == pygame.K_RIGHT:
                gears[1].rotate(1)
                right_presed = False
            elif up_presed and event.key == pygame.K_UP:
                gears[0].rotate(1)
                up_presed = False
            elif down_presed and event.key == pygame.K_DOWN:
                gears[0].rotate(-1)
                down_presed = False


        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     gears[0].rotate(-1)
        # if keys[pygame.K_RIGHT]:
        #     gears[0].rotate(1)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presed = True
            
        if mouse_presed and event.type == pygame.MOUSEBUTTONUP:#swap figures if on one line
            mouse_presed = False
            mouse_position = pygame.mouse.get_pos()
            for i, s_p in enumerate(SWAP_POINTS):
                if calculate_distance(mouse_position, s_p) < SWAP_DIST:
                    d = None
                    if points_swap_dir[i] == 'h':
                        d = 'r'
                    elif points_swap_dir[i] == 'v':
                        d = 'd'
                    for d_g_ind in points_gears[i][:-1]:
                        d_gears[d_g_ind].gear.swap_fig(d)#in this case we need to enumerate gears from left to right and from up to down
                    break


        screen.fill(BLACK)

        for d_gear in d_gears:
            d_gear.draw(screen)

        if check_win(gears):
            print("YOU WIN")
            break

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
