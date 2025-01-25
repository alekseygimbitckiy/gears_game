import pygame
import math
from dataclasses import dataclass

from figure import Figure
from utils import *

@dataclass
class Figure_draw:
    figure: Figure
    x: int = None
    y: int = None
    dirr_angle: float = None

    def update_pos(self, g_x, g_y, g_alpha, s_alpha):
        dirr_angle = s_alpha + g_alpha
        rad = math.radians(dirr_angle)
        self.x, self.y = g_x + FIGURE_DIR_RADIUS * math.cos(rad), g_y + FIGURE_DIR_RADIUS * math.sin(rad)

    def draw_figure(self, surface):
        x, y = self.x, self.y
        hole_type = self.figure.shape

        # Рисуем отверстие
        if hole_type == 'rect':  # Квадрат
            pygame.draw.rect(surface, RED, (x - FIGURE_RADIUS, y - FIGURE_RADIUS, 2 * FIGURE_RADIUS, 2 * FIGURE_RADIUS))
        elif hole_type == 'circle':  # Круг
            pygame.draw.circle(surface, RED, (int(x), int(y)), FIGURE_RADIUS)
        elif hole_type == 'triangle':  # Треугольник
            triangle_points = [
                (x, y - FIGURE_RADIUS),
                (x - FIGURE_RADIUS, y + FIGURE_RADIUS),
                (x + FIGURE_RADIUS, y + FIGURE_RADIUS),
            ]
            pygame.draw.polygon(surface, RED, triangle_points)
