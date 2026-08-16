# state.py
# Guarda TODO el estado mutable del juego en un solo objeto (GameState).
# Esto reemplaza a las ~40 variables globales que tenia el script original,
# y permite pasar el estado entre modulos sin usar "global".

import copy
from board import boards


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia el juego por completo (nueva partida)."""
        self.level = copy.deepcopy(boards)

        # Jugador (Pacman)
        self.player_x = 450
        self.player_y = 663
        self.direction = 0
        self.direction_command = 0
        self.player_speed = 3
        self.counter = 0
        self.flicker = False
        self.turns_allowed = [False, False, False, False]

        # Posiciones y direcciones de los fantasmas
        self.blinky_x, self.blinky_y, self.blinky_direction = 56, 58, 0
        self.inky_x, self.inky_y, self.inky_direction = 440, 388, 2
        self.pinky_x, self.pinky_y, self.pinky_direction = 440, 438, 0
        self.clyde_x, self.clyde_y, self.clyde_direction = 440, 438, 0

        self.ghost_speeds = [3, 3, 3, 3]

        # Estado de "muerto" y "en la caja" de cada fantasma
        self.blinky_dead = self.pinky_dead = self.inky_dead = self.clyde_dead = False
        self.blinky_box = self.pinky_box = self.inky_box = self.clyde_box = False

        # Objetivo (target) de cada fantasma
        self.targets = [(self.player_x, self.player_y)] * 4

        # Powerup
        self.power_up = False
        self.powerup_counter = 0
        self.eaten_ghost = [False, False, False, False]

        # Puntaje y vidas
        self.score = 0
        self.lives = 3

        # Estado general de la partida
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.moving = False
        self.startup_counter = 0

    def respawn_after_death(self):
        """Reubica al jugador y a los fantasmas en su posicion inicial
        tras perder una vida, SIN tocar el puntaje ni las vidas restantes."""
        self.startup_counter = 0
        self.power_up = False
        self.powerup_counter = 0

        self.player_x = 450
        self.player_y = 663
        self.direction = 0
        self.direction_command = 0

        self.blinky_x, self.blinky_y, self.blinky_direction = 56, 58, 0
        self.inky_x, self.inky_y, self.inky_direction = 440, 388, 2
        self.pinky_x, self.pinky_y, self.pinky_direction = 440, 438, 0
        self.clyde_x, self.clyde_y, self.clyde_direction = 440, 438, 0

        self.eaten_ghost = [False, False, False, False]
        self.blinky_dead = self.pinky_dead = self.inky_dead = self.clyde_dead = False
