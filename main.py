# main.py
# Mi proyecto de pacman
# Mario Suero
#
# Punto de entrada del juego. Inicializa pygame, carga assets,
# muestra la pantalla de inicio y corre el loop principal.

import sys
import pygame

from settings import WIDTH, HEIGHT, FPS, WALL_COLOR
from state import GameState
from assets import load_assets, load_music
from ghost import Ghost
from draw_board import draw_board
from player import check_position, move_player, draw_player
from game_logic import check_dot_collisions, get_targets
from ui import pantalla_inicio, draw_misc, handle_pause


def handle_ghost_collision(state):
    """Se llama cuando un fantasma atrapa al jugador: resta una vida y reubica
    a todos, o termina la partida si ya no quedan vidas."""
    if state.lives > 0:
        state.lives -= 1
        state.respawn_after_death()
    else:
        state.game_over = True
        state.moving = False
        state.startup_counter = 0


def create_ghosts(screen, state, assets):
    """Crea (y dibuja) los 4 fantasmas para el frame actual, usando la posicion
    y objetivo guardados en el estado."""
    blinky = Ghost(state.blinky_x, state.blinky_y, state.targets[0], state.ghost_speeds[0],
                    assets["blinky_img"], state.blinky_direction, state.blinky_dead, state.blinky_box, 0,
                    screen, state, assets)
    inky = Ghost(state.inky_x, state.inky_y, state.targets[1], state.ghost_speeds[1],
                 assets["inky_img"], state.inky_direction, state.inky_dead, state.inky_box, 1,
                 screen, state, assets)
    pinky = Ghost(state.pinky_x, state.pinky_y, state.targets[2], state.ghost_speeds[2],
                  assets["pinky_img"], state.pinky_direction, state.pinky_dead, state.pinky_box, 2,
                  screen, state, assets)
    clyde = Ghost(state.clyde_x, state.clyde_y, state.targets[3], state.ghost_speeds[3],
                  assets["clyde_img"], state.clyde_direction, state.clyde_dead, state.clyde_box, 3,
                  screen, state, assets)
    return blinky, inky, pinky, clyde


def update_ghost_speeds(state):
    """Actualiza la velocidad de cada fantasma segun powerup / comido / muerto."""
    if state.power_up:
        state.ghost_speeds = [1, 1, 1, 1]
    else:
        state.ghost_speeds = [2, 2, 2, 2]
    for i in range(4):
        if state.eaten_ghost[i]:
            state.ghost_speeds[i] = 2
    if state.blinky_dead:
        state.ghost_speeds[0] = 4
    if state.inky_dead:
        state.ghost_speeds[1] = 4
    if state.pinky_dead:
        state.ghost_speeds[2] = 4
    if state.clyde_dead:
        state.ghost_speeds[3] = 4


def check_win_condition(state):
    """El jugador gana cuando ya no quedan bolitas (1) ni powerups (2) en el nivel."""
    state.game_won = True
    for row in state.level:
        if 1 in row or 2 in row:
            state.game_won = False
            break


def move_ghosts(state, blinky, inky, pinky, clyde):
    """Mueve a cada fantasma con su IA propia, salvo que este muerto o en la caja,
    en cuyo caso usa el movimiento 'de vuelta a casa' (move_clyde)."""
    if not state.blinky_dead and not blinky.in_box:
        state.blinky_x, state.blinky_y, state.blinky_direction = blinky.move_blinky()
    else:
        state.blinky_x, state.blinky_y, state.blinky_direction = blinky.move_clyde()

    if not state.pinky_dead and not pinky.in_box:
        state.pinky_x, state.pinky_y, state.pinky_direction = pinky.move_pinky()
    else:
        state.pinky_x, state.pinky_y, state.pinky_direction = pinky.move_clyde()

    if not state.inky_dead and not inky.in_box:
        state.inky_x, state.inky_y, state.inky_direction = inky.move_inky()
    else:
        state.inky_x, state.inky_y, state.inky_direction = inky.move_clyde()

    state.clyde_x, state.clyde_y, state.clyde_direction = clyde.move_clyde()


def check_ghost_collisions(state, player_circle, blinky, inky, pinky, clyde):
    """Revisa todas las colisiones jugador-fantasma: perder una vida o comerse
    a un fantasma asustado."""
    if not state.power_up:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
           (player_circle.colliderect(inky.rect) and not inky.dead) or \
           (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
           (player_circle.colliderect(clyde.rect) and not clyde.dead):
            handle_ghost_collision(state)

    if state.power_up and player_circle.colliderect(blinky.rect) and state.eaten_ghost[0] and not blinky.dead:
        handle_ghost_collision(state)
    if state.power_up and player_circle.colliderect(inky.rect) and state.eaten_ghost[1] and not inky.dead:
        handle_ghost_collision(state)
    if state.power_up and player_circle.colliderect(pinky.rect) and state.eaten_ghost[2] and not pinky.dead:
        handle_ghost_collision(state)
    if state.power_up and player_circle.colliderect(clyde.rect) and state.eaten_ghost[3] and not clyde.dead:
        handle_ghost_collision(state)

    if state.power_up and player_circle.colliderect(blinky.rect) and not blinky.dead and not state.eaten_ghost[0]:
        state.blinky_dead = True
        state.eaten_ghost[0] = True
        state.score += (2 ** state.eaten_ghost.count(True)) * 100
    if state.power_up and player_circle.colliderect(inky.rect) and not inky.dead and not state.eaten_ghost[1]:
        state.inky_dead = True
        state.eaten_ghost[1] = True
        state.score += (2 ** state.eaten_ghost.count(True)) * 100
    if state.power_up and player_circle.colliderect(pinky.rect) and not pinky.dead and not state.eaten_ghost[2]:
        state.pinky_dead = True
        state.eaten_ghost[2] = True
        state.score += (2 ** state.eaten_ghost.count(True)) * 100
    if state.power_up and player_circle.colliderect(clyde.rect) and not clyde.dead and not state.eaten_ghost[3]:
        state.clyde_dead = True
        state.eaten_ghost[3] = True
        state.score += (2 ** state.eaten_ghost.count(True)) * 100


def handle_events(state):
    """Procesa teclado/mouse. Devuelve False si el usuario cerró la ventana."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                state.paused = not state.paused

            elif event.key == pygame.K_RIGHT:
                state.direction_command = 0

            elif event.key == pygame.K_LEFT:
                state.direction_command = 1

            elif event.key == pygame.K_UP:
                state.direction_command = 2

            elif event.key == pygame.K_DOWN:
                state.direction_command = 3

            elif event.key == pygame.K_SPACE and (state.game_over or state.game_won):
                state.reset()

    return True


def apply_direction_command(state):
    """Aplica el giro pedido por el jugador si el laberinto lo permite en ese punto."""
    if state.direction_command == 0 and state.turns_allowed[0]:
        state.direction = 0
    if state.direction_command == 1 and state.turns_allowed[1]:
        state.direction = 1
    if state.direction_command == 2 and state.turns_allowed[2]:
        state.direction = 2
    if state.direction_command == 3 and state.turns_allowed[3]:
        state.direction = 3


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    timer = pygame.time.Clock()

    load_music()
    assets = load_assets()

    pantalla_inicio(screen, timer, FPS, assets)

    state = GameState()
    run = True

    while run:
        timer.tick(FPS)
        
        if not handle_events(state):
            run = False
            continue

        if state.game_over or state.game_won:
            screen.fill("black")
            draw_misc(screen, state, assets)
            pygame.display.flip()
            timer.tick(FPS)
            draw_player(screen, state, assets)
            continue

        if state.paused:
            handle_pause(screen, assets)
            while state.paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        state.paused = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        state.paused = False
            continue

        # --- Animacion (parpadeo de bolitas / frames de Pacman) ---
        if state.counter < 19:
            state.counter += 1
            if state.counter > 3:
                state.flicker = False
        else:
            state.counter = 0
            state.flicker = True

        # --- Duracion del powerup ---
        if state.power_up and state.powerup_counter < 600:
            state.powerup_counter += 1
        elif state.power_up and state.powerup_counter >= 600:
            state.powerup_counter = 0
            state.power_up = False
            state.eaten_ghost = [False, False, False, False]

        # --- Cuenta regresiva antes de empezar a mover a los personajes ---
        if state.startup_counter < 180 and not state.game_over and not state.game_won:
            state.moving = False
            state.startup_counter += 1
        else:
            state.moving = True

        screen.fill("black")
        draw_board(screen, state.level, WALL_COLOR, state.flicker)

        center_x = state.player_x + 23
        center_y = state.player_y + 24

        update_ghost_speeds(state)
        check_win_condition(state)

        player_circle = pygame.draw.circle(screen, "black", (center_x, center_y), 20, 2)
        draw_player(screen, state, assets)

        blinky, inky, pinky, clyde = create_ghosts(screen, state, assets)

        draw_misc(screen, state, assets)
        state.targets = get_targets(state, (blinky, inky, pinky, clyde))

        pygame.draw.circle(screen, "white", (center_x, center_y), 2)

        state.turns_allowed = check_position(state, center_x, center_y)
        if state.moving:
            state.player_x, state.player_y = move_player(state)
            move_ghosts(state, blinky, inky, pinky, clyde)

        check_dot_collisions(state, center_x, center_y)
        check_ghost_collisions(state, player_circle, blinky, inky, pinky, clyde)

        if not handle_events(state):
            run = False

        apply_direction_command(state)

        # --- Wrap-around del jugador (tunel lateral) ---
        if state.player_x > 900:
            state.player_x = -47
        elif state.player_x < -50:
            state.player_x = 897

        # --- Los fantasmas revive al llegar a la caja ---
        if blinky.in_box and state.blinky_dead:
            state.blinky_dead = False
        if inky.in_box and state.inky_dead:
            state.inky_dead = False
        if pinky.in_box and state.pinky_dead:
            state.pinky_dead = False
        if clyde.in_box and state.clyde_dead:
            state.clyde_dead = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
