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

gear_0 = Gear(0, NUM_FIGURES, 0, "rect")
gear_1 = Gear(1, NUM_FIGURES, 0, "circle")
gear_2 = Gear(2, NUM_FIGURES, 0, "triangle")
gear_3 = Gear(2, NUM_FIGURES, 0, "circle")

gears = [gear_0, gear_1, gear_2, gear_3]
for i in range(len(gears) - 1):
    gears[i].neighbor_r = gears[i+1]

for i in range(len(gears) - 1, 0, -1):
    gears[i].neighbor_l = gears[i-1]

# d_gears_c = [(WIDTH // 2 - GEAR_RADIUS, HEIGHT // 2 - GEAR_RADIUS), (WIDTH // 2 + GEAR_RADIUS, HEIGHT // 2 - GEAR_RADIUS), (WIDTH // 2 + GEAR_RADIUS, HEIGHT // 2 + GEAR_RADIUS),\
#              (WIDTH // 2 - GEAR_RADIUS, HEIGHT // 2 + GEAR_RADIUS)]
d_gears_c = [(WIDTH // 2 - 2 * GEAR_RADIUS + 2 * i * GEAR_RADIUS, HEIGHT // 2) for i in range(len(gears))]
d_gears = [Gear_draw(gears[i], gears[i].figure_type, d_gears_c[i][0], d_gears_c[i][1]) for i in range(len(gears))]


# SWAP_POINTS = [((d_gears[i].x + d_gears[i+1].x)//2, (d_gears[i].y + d_gears[i+1].y)//2) for i in range(len(d_gears) - 1)]
SWAP_POINTS = [((d_gears_c[i % len(gears)][0] + d_gears_c[(i + 1)%len(gears)][0])//2, (d_gears_c[i % len(gears)][1] + d_gears_c[(i + 1)%len(gears)][1])//2) for i in range(len(gears) - 1)]

gen_level(gears, NUM_SWAPS)



# draw()
# print()
# gear_1.swap_fig(1)
# draw()
# print()
# gear_0.rotate(1)
# draw()
# print()

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Гонки шестерёнок")

def main():
    mouse_presed = False
    left_presed = False
    right_presed = False
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

        if event.type == pygame.KEYUP:
            if left_presed and event.key == pygame.K_LEFT:
                gears[0].rotate(-1)
                left_presed = False
            elif right_presed and event.key == pygame.K_RIGHT:
                gears[0].rotate(1)
                right_presed = False


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
            print(mouse_position)
            for i, s_p in enumerate(SWAP_POINTS):
                if calculate_distance(mouse_position, s_p) < SWAP_DIST:
                    print('swap with', i)
                    d_gears[i].gear.swap_fig(1)##########################################
                    draw()
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
