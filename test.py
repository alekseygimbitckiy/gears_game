import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
GEAR_RADIUS = 50
GEAR_WIDTH = 20  # Ширина шестерёнки
ANGLE_STEP = 5

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

# Установка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Гонки шестерёнок")

# Углы вращения шестерёнок
angles = [0, 0, 0]

def draw_gear(surface, angle, x, y, hole_type):
    """Рисует шестерёнку с объёмным эффектом и отверстием."""
    points = []
    for i in range(0, 360, 30):
        rad = math.radians(i + angle)
        x_pos = x + GEAR_RADIUS * math.cos(rad)
        y_pos = y + GEAR_RADIUS * math.sin(rad)
        points.append((x_pos, y_pos))

    # Рисуем тень
    shadow_points = [(p[0], p[1] + GEAR_WIDTH) for p in points]
    pygame.draw.polygon(surface, GREY, shadow_points)

    # Рисуем шестерёнку
    pygame.draw.polygon(surface, WHITE, points)

    # Положение отверстия
    hole_offset = 10  # Смещение для отверстий
    hole_angle = angle  # Угол вращения отверстия
    hole_x = x + hole_offset * math.cos(math.radians(hole_angle))
    hole_y = y + hole_offset * math.sin(math.radians(hole_angle))

    # Рисуем отверстие
    if hole_type == 1:  # Квадрат
        pygame.draw.rect(surface, BLACK, (hole_x - 10, hole_y - 10, 20, 20))
    elif hole_type == 2:  # Круг
        pygame.draw.circle(surface, BLACK, (int(hole_x), int(hole_y)), 10)
    elif hole_type == 3:  # Треугольник
        triangle_points = [
            (hole_x, hole_y - 10),
            (hole_x - 10, hole_y + 10),
            (hole_x + 10, hole_y + 10),
        ]
        pygame.draw.polygon(surface, BLACK, triangle_points)

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angles[0] -= ANGLE_STEP
            angles[2] -= ANGLE_STEP
            angles[1] += ANGLE_STEP
        if keys[pygame.K_RIGHT]:
            angles[0] += ANGLE_STEP
            angles[2] += ANGLE_STEP
            angles[1] -= ANGLE_STEP

        # Очистка экрана
        screen.fill(BLACK)

        # Рисуем шестерёнки с отверстиями
        draw_gear(screen, angles[0], WIDTH // 2 - 100, HEIGHT // 2, hole_type=1)  # Квадрат
        draw_gear(screen, angles[1], WIDTH // 2, HEIGHT // 2, hole_type=2)       # Круг
        draw_gear(screen, angles[2], WIDTH // 2 + 100, HEIGHT // 2, hole_type=3) # Треугольник

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()