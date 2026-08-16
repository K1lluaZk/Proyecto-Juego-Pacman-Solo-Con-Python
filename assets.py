# assets.py
# Carga de todas las imagenes, fuentes y sonidos del juego.
# load_assets() debe llamarse DESPUES de pygame.display.set_mode(),
# ya que algunas cargas de imagen dependen de tener una superficie activa.

import pygame

def load_music():
    """Carga y reproduce la musica de fondo en bucle."""
    pygame.mixer.music.load("Pacman Music.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)


def load_assets():
    """Carga todas las imagenes y fuentes usadas en el juego y las devuelve en un dict."""
    assets = {
        "font": pygame.font.Font("freesansbold.ttf", 20),
        "font_title": pygame.font.Font(None, 74),
        "font_button": pygame.font.Font(None, 36),
        "font_control": pygame.font.Font(None, 28),
    }

    # Imagenes del jugador (animacion de Pacman)
    assets["player_images"] = [
        pygame.transform.scale(
            pygame.image.load(f"player_images/{i}.png"), (45, 45)
        )
        for i in range(1, 5)
    ]

    # Imagenes de los fantasmas
    assets["blinky_img"] = pygame.transform.scale(
        pygame.image.load("ghost_images/red.png"), (45, 45)
    )
    assets["pinky_img"] = pygame.transform.scale(
        pygame.image.load("ghost_images/pink.png"), (45, 45)
    )
    assets["inky_img"] = pygame.transform.scale(
        pygame.image.load("ghost_images/blue.png"), (45, 45)
    )
    assets["clyde_img"] = pygame.transform.scale(
        pygame.image.load("ghost_images/orange.png"), (45, 45)
    )
    assets["spooked_img"] = pygame.transform.scale(
        pygame.image.load("ghost_images/powerup.png"), (45, 45)
    )
    assets["dead_img"] = pygame.transform.scale(
        pygame.image.load("ghost_images/dead.png"), (45, 45)
    )

    # Otras imagenes
    assets["cherry_image"] = pygame.transform.scale(
        pygame.image.load("cherry.png"), (35, 35)
    )
    assets["image_inicio"] = pygame.transform.scale(
        pygame.image.load("Maquinainicio.jpg"), (900, 1000)
    )

    return assets
