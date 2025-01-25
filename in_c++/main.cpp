#include "raylib.h"
#include <cmath>

const float GEAR_RADIUS = 50.0f;
const float GEAR_WIDTH = 10.0f;
const float GEAR_OFFSET = 120.0f; // Расстояние между шестеренками

void DrawGear(Vector2 position, float angle); // Объявление функции

int main() {
    // Инициализация окна
    InitWindow(800, 600, "Gear Simulation");
    SetTargetFPS(60);

    // Угол поворота шестеренок
    float centralGearAngle = 0.0f;
    float leftGearAngle = 0.0f;
    float rightGearAngle = 0.0f;

    bool isDragging = false; // Флаг для отслеживания перетаскивания
    float lastAngle = 0.0f;  // Последний угол при перетаскивании

    while (!WindowShouldClose()) {
        // Получение позиции мыши
        Vector2 mousePos = GetMousePosition();

        // Проверка нажатия кнопки мыши
        if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
            // Проверка, попадает ли курсор в одну из шестеренок
            if (CheckCollisionPointCircle(mousePos, { GetScreenWidth() / 2 - GEAR_OFFSET, GetScreenHeight() / 2 }, GEAR_RADIUS) ||
                CheckCollisionPointCircle(mousePos, { GetScreenWidth() / 2, GetScreenHeight() / 2 }, GEAR_RADIUS) ||
                CheckCollisionPointCircle(mousePos, { GetScreenWidth() / 2 + GEAR_OFFSET, GetScreenHeight() / 2 }, GEAR_RADIUS)) {
                isDragging = true;
                lastAngle = atan2(mousePos.y - GetScreenHeight() / 2, mousePos.x - GetScreenWidth() / 2);
            }
        }

        // Обработка перетаскивания
        if (isDragging) {
            Vector2 newMousePos = GetMousePosition();
            float newAngle = atan2(newMousePos.y - GetScreenHeight() / 2, newMousePos.x - GetScreenWidth() / 2);
            float angleDelta = newAngle - lastAngle;

            // Обновление углов шестеренок
            centralGearAngle += angleDelta;
            leftGearAngle += angleDelta;
            rightGearAngle -= angleDelta;

            lastAngle = newAngle; // Обновление последнего угла
        }

        // Проверка на отпускание кнопки мыши
        if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON)) {
            isDragging = false;
        }

        // Начало рисования
        BeginDrawing();
        ClearBackground(RAYWHITE);

        // Рисование шестеренок
        Vector2 centralGearPos = { GetScreenWidth() / 2, GetScreenHeight() / 2 };
        Vector2 leftGearPos = { centralGearPos.x - GEAR_OFFSET, centralGearPos.y };
        Vector2 rightGearPos = { centralGearPos.x + GEAR_OFFSET, centralGearPos.y };

        DrawGear(leftGearPos, leftGearAngle);
        DrawGear(centralGearPos, centralGearAngle);
        DrawGear(rightGearPos, rightGearAngle);

        // Конец рисования
        EndDrawing();
    }

    // Закрытие окна
    CloseWindow();
    return 0;
}

void DrawGear(Vector2 position, float angle) {
    // Рисование шестеренки
    DrawCircleV(position, GEAR_RADIUS, DARKGRAY);
    
    // Рисуем зубья шестеренки
    int toothCount = 12; // Количество зубьев
    for (int i = 0; i < toothCount; i++) {
        float toothAngle = (2 * PI / toothCount) * i + angle;
        Vector2 toothStart = { position.x + cos(toothAngle) * (GEAR_RADIUS - 5), 
                               position.y + sin(toothAngle) * (GEAR_RADIUS - 5) };
        Vector2 toothEnd = { position.x + cos(toothAngle) * GEAR_RADIUS, 
                             position.y + sin(toothAngle) * GEAR_RADIUS };
        DrawLineV(toothStart, toothEnd, RED);
    }
}//g++ main.cpp -lraylib -lm -lpthread -ldl -lrt