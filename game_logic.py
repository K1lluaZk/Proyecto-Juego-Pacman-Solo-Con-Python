# game_logic.py
# Reglas de juego que no pertenecen a un personaje en particular:
# comer bolitas/powerups y calcular a donde se dirige cada fantasma.

from settings import WIDTH, HEIGHT


def check_dot_collisions(state, center_x, center_y):
    """Revisa si el jugador esta sobre una bolita o powerup y actualiza puntaje/estado."""
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < state.player_x < 870:
        cell = state.level[center_y // num1][center_x // num2]
        if cell == 1:
            state.level[center_y // num1][center_x // num2] = 0
            state.score += 10  # bolita pequeña
        if cell == 2:
            state.level[center_y // num1][center_x // num2] = 0
            state.score += 50  # bolita grande
            state.power_up = True
            state.powerup_counter = 0
            state.eaten_ghost = [False, False, False, False]


def get_targets(state, ghosts):
    """Calcula el objetivo (target) de cada fantasma segun si hay powerup activo o no."""
    blinky, inky, pinky, clyde = ghosts
    player_x, player_y = state.player_x, state.player_y
    eaten_ghost = state.eaten_ghost

    runaway_x = 900 if player_x < 450 else 0
    runaway_y = 900 if player_y < 450 else 0
    return_target = (380, 400)  # regreso a la caja central

    if state.power_up:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < state.blinky_x < 560 and 340 < state.blinky_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target

        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < state.inky_x < 560 and 340 < state.inky_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target

        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < state.pinky_x < 560 and 340 < state.pinky_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target

        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < state.clyde_x < 560 and 340 < state.clyde_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < state.blinky_x < 560 and 340 < state.blinky_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target

        if not inky.dead:
            if 340 < state.inky_x < 560 and 340 < state.inky_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target

        if not pinky.dead:
            if 340 < state.pinky_x < 560 and 340 < state.pinky_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target

        if not clyde.dead:
            if 340 < state.clyde_x < 560 and 340 < state.clyde_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target

    return [blink_target, ink_target, pink_target, clyd_target]
