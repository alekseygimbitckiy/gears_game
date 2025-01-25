import pygame
import math
from dataclasses import dataclass

from gear import Gear
from figure_draw import Figure_draw
from utils import *

@dataclass
class Gear_draw:
    gear: Gear
    figure_type: str
    x: int
    y: int

    d_figures: list[Figure_draw] = None

    def __post_init__(self):
        if self.d_figures is None:
            self.d_figures = [Figure_draw(figure) for figure in self.gear.figures]

    def update_d_fig(self):
        self.d_figures = [Figure_draw(figure) for figure in self.gear.figures]

    def update_fig_pos(self):
        for i, d_figure in enumerate(self.d_figures):
            d_figure.update_pos(self.x, self.y, self.gear.alpha, calc_figure_s_alpha(i, self.gear.num_figures))

    def draw_gear(self, surface):
        angle, x, y = self.gear.alpha, self.x, self.y
        hole_type = self.figure_type
        """Рисует шестерёнку с объёмным эффектом и отверстием."""
        points = []
        for i in range(0, 360, 40):
            rad = math.radians(i + angle)
            x_pos = x + GEAR_RADIUS * math.cos(rad)
            y_pos = y + GEAR_RADIUS * math.sin(rad)
            points.append((x_pos, y_pos))

        # Рисуем тень
        shadow_points = [(p[0], p[1] + GEAR_WIDTH) for p in points]
        pygame.draw.polygon(surface, GREY, shadow_points)

        # Рисуем шестерёнку
        pygame.draw.polygon(surface, WHITE, points)


        # Рисуем отверстие
        if hole_type == 'rect':  # Квадрат
            pygame.draw.rect(surface, BLACK, (x - HOLE_RADIUS, y - HOLE_RADIUS, 2 * HOLE_RADIUS, 2 * HOLE_RADIUS))
        elif hole_type == 'circle':  # Круг
            pygame.draw.circle(surface, BLACK, (int(x), int(y)), HOLE_RADIUS)
        elif hole_type == 'triangle':  # Треугольник
            triangle_points = [
                (x, y - HOLE_RADIUS),
                (x - HOLE_RADIUS, y + HOLE_RADIUS),
                (x + HOLE_RADIUS, y + HOLE_RADIUS),
            ]
            pygame.draw.polygon(surface, BLACK, triangle_points)

        return points

    def draw(self, surface):
        self.update_d_fig()
        self.update_fig_pos()
        points = self.draw_gear(surface)
        for i, d_figure in enumerate(self.d_figures):
            d_figure.draw_figure(surface)

        return points