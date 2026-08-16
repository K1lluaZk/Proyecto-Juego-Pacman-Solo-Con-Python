# ui.py
# Pantallas e interfaz: pantalla de inicio, HUD (puntaje/vidas), mensajes de pausa/fin.

import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, YELLOW

BUTTON_RECT = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)

CONTROL_TEXT = [
    "",
    "Clickea Iniciar Para Empezar",
    "",
    "Controles:",
    "Flecha Arriba: Mover Hacia Arriba",
    "Flecha Abajo: Mover Hacia Abajo",
    "Flecha Izquierda: Mover Hacia La Izquierda",
    "Flecha Derecha: Mover Hacia La Derecha",
    "Espacio: Reiniciar Cuando Pierda O Gane",
    "P: Para Pausar El Juego",
    "",
    "",
    "2024 Namco LTD.",
]


def pantalla_inicio(screen, timer, fps, assets):
    """Muestra la pantalla de inicio y bloquea hasta que el jugador pulse 'Iniciar'."""
    text_title = assets["font_title"].render("Pac-Man", True, YELLOW)
    text_button = assets["font_button"].render("Iniciar", True, WHITE)

    screen.fill(BLACK)
    while True:
        screen.blit(assets["image_inicio"], (0, 0))
        screen.blit(text_title, (WIDTH // 2 - text_title.get_width() // 2, HEIGHT // 4))
        pygame.draw.rect(screen, YELLOW, BUTTON_RECT)
        screen.blit(text_button, (BUTTON_RECT.x + BUTTON_RECT.width // 2 - text_button.get_width() // 2,
                                   BUTTON_RECT.y + BUTTON_RECT.height // 2 - text_button.get_height() // 2))

        for i, linea in enumerate(CONTROL_TEXT):
            text_control = assets["font_control"].render(linea, True, YELLOW)
            screen.blit(text_control, (WIDTH // 2 - text_control.get_width() // 2,
                                        BUTTON_RECT.y + BUTTON_RECT.height + 30 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON_RECT.collidepoint(event.pos):
                    return
        pygame.display.flip()
        timer.tick(fps)


def draw_misc(screen, state, assets):
    """Dibuja el puntaje, vidas, icono de powerup y mensajes de game over / victoria."""
    font = assets["font"]
    score_text = font.render(f"Puntos: {state.score}", True, "white")
    screen.blit(score_text, (10, 920))
    if state.power_up:
        screen.blit(assets["cherry_image"], (135, 915))
    for i in range(state.lives):
        screen.blit(pygame.transform.scale(assets["player_images"][0], (30, 30)), (650 + i * 40, 915))
    jugador_text = font.render("1UP", True, "white")
    screen.blit(jugador_text, (780, 920))
    vidas_text = font.render("Vidas:", True, "white")
    screen.blit(vidas_text, (580, 920))
    if state.game_over:
        pygame.draw.rect(screen, "red", [50, 200, 800, 300], 10, 20)
        pygame.draw.rect(screen, "dark gray", [70, 220, 760, 260], 10, 20)
        game_over_text = font.render("Game Over, Mala Suerte! Espacio Para Reiniciar", True, "white")
        screen.blit(game_over_text, (100, 300))
    if state.game_won:
        pygame.draw.rect(screen, "green", [50, 200, 800, 300], 10, 20)
        pygame.draw.rect(screen, "dark gray", [70, 220, 760, 260], 10, 20)
        game_won_text = font.render("Felicidades, Has Ganado! Espacio Para Reiniciar", True, "white")
        screen.blit(game_won_text, (100, 300))


def handle_pause(screen, assets):
    """Muestra el mensaje de 'juego en pausa' en pantalla."""
    pause_text = assets["font"].render("Juego en pausa. Presiona P para continuar", True, "white")
    text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(pause_text, text_rect)
    pygame.display.flip()
