# player.py
# Logica del jugador (Pacman): deteccion de giros permitidos, movimiento y dibujo.

import pygame
from settings import WIDTH, HEIGHT


def check_position(state, centerx, centery):
    """Determina hacia que direcciones puede girar el jugador desde su posicion actual."""
    level = state.level
    direction = state.direction
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15

    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][(centerx // num2)] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns


def move_player(state):
    """Devuelve la nueva posicion (x, y) del jugador segun su direccion y velocidad."""
    play_x, play_y = state.player_x, state.player_y
    direction = state.direction
    turns_allowed = state.turns_allowed
    if direction == 0 and turns_allowed[0]:
        play_x += state.player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= state.player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= state.player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += state.player_speed
    return play_x, play_y


def draw_player(screen, state, assets):
    """Dibuja a Pacman con la rotacion/reflejo correspondiente a su direccion actual."""
    # 0-Derecha, 1-Izquierda, 2-Arriba, 3-Abajo
    img = assets["player_images"][state.counter // 5]
    if state.direction == 0:
        screen.blit(img, (state.player_x, state.player_y))
    elif state.direction == 1:
        screen.blit(pygame.transform.flip(img, True, False), (state.player_x, state.player_y))
    elif state.direction == 2:
        screen.blit(pygame.transform.rotate(img, 90), (state.player_x, state.player_y))
    elif state.direction == 3:
        screen.blit(pygame.transform.rotate(img, 270), (state.player_x, state.player_y))
