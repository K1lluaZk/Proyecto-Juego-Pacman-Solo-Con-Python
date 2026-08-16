# board_render.py
# Dibuja el laberinto (paredes, bolitas, powerups) a partir de la matriz `level`.

import math
import pygame
from settings import WIDTH, HEIGHT

PI = math.pi


def draw_board(screen, level, color, flicker):
    """Dibuja el laberinto completo en `screen` segun los codigos de `level`:
    1=bolita pequeña, 2=bolita grande (powerup), 3-9=distintos tramos de pared."""
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            cell = level[i][j]
            if cell == 1:
                pygame.draw.circle(screen, "white", (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if cell == 2 and not flicker:
                pygame.draw.circle(screen, "white", (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if cell == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                  (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if cell == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                  (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if cell == 5:
                pygame.draw.arc(screen, color,
                                 [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                 0, PI / 2, 3)
            if cell == 6:
                pygame.draw.arc(screen, color,
                                 [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                                 PI / 2, PI, 3)
            if cell == 7:
                pygame.draw.arc(screen, color,
                                 [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1],
                                 PI, 3 * PI / 2, 3)
            if cell == 8:
                pygame.draw.arc(screen, color,
                                 [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1],
                                 3 * PI / 2, 2 * PI, 3)
            if cell == 9:
                pygame.draw.line(screen, "white", (j * num2, i * num1 + (0.5 * num1)),
                                  (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
