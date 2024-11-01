# Mi proyecto de pacman
# Mario Suero

import copy
from board import boards
import pygame
import math


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(f"Proyecto PM/Pacman Music.wav")

pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.5)

# Configuraciones basicas del juego

# Tamaño de pixeles del juego
width = 900
height = 950

screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)

White = (255, 255, 255)
Black = (0, 0, 0)
Yellow = (255, 255, 0)
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 36)
font_control = pygame.font.Font(None, 28)  

text_title = font_title.render("Pac-Man", True, Yellow)
text_button = font_button.render("Iniciar", True, White)

imageninicio = pygame.image.load(f"Proyecto PM/Maquinainicio.jpg")
imageninicio = pygame.transform.scale(imageninicio, (900, 1000))

button_rect = pygame.Rect(width // 2 - 50, height // 2, 100, 50)

control_text = [
    "Controles:",
    "Flecha Arriba: Mover Hacia Arriba",
    "Flecha Abajo: Mover Hacia Abajo",
    "Flecha Izquierda: Mover Hacia La Izquierda",
    "Flecha Derecha: Mover Hacia La Derecha",
    "Espacio: Reiniciar Cuando Pierda O Gane",
]

# Función de pantalla de inicio
def pantalla_inicio():
    screen.fill(Black)
    while True:
        screen.blit(imageninicio, (0, 0))
        screen.blit(text_title, (width // 2 - text_title.get_width() // 2, height // 4))
        pygame.draw.rect(screen, Yellow, button_rect)
        screen.blit(text_button, (button_rect.x + button_rect.width // 2 - text_button.get_width() // 2, 
                                  button_rect.y + button_rect.height // 2 - text_button.get_height() // 2))
        
        for i, linea in enumerate(control_text):
            text_control = font_control.render(linea, True, Yellow)
            screen.blit(text_control, (width // 2 - text_control.get_width() // 2, 
                                        button_rect.y + button_rect.height + 30 + i * 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  
        pygame.display.flip()
        timer.tick(fps)

pantalla_inicio()

level = copy.deepcopy(boards)
color = "blue"
pi = math.pi
player_images = []
for i in range(1, 5):
# Imagenes De Jugador 1 Y Enemigos
      player_images.append(pygame.transform.scale(pygame.image.load(f"Proyecto PM/player_images/{i}.png"), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load(f"Proyecto PM/ghost_images/red.png"), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f"Proyecto PM/ghost_images/pink.png"), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f"Proyecto PM/ghost_images/blue.png"), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f"Proyecto PM/ghost_images/orange.png"), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f"Proyecto PM/ghost_images/powerup.png"), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f"Proyecto PM/ghost_images/dead.png"), (45, 45))
# Coordenadas De Personajes
# Coordenadas Donde Se Encuentra El Jugador Y Los Enemigos
# Jugador 1
player_x = 450
player_y = 663
direction = 0
# Fantasma blinky(Rojo)
blinky_x = 56
blinky_y = 58
blinky_direction = 0
# Fantasma inky (Azul)
inky_x = 440
inky_y = 388
inky_direction = 2
# Fantasma pinky (Rosa)
pinky_x = 440 
pinky_y = 438
pinky_direction = 0
# Fantasma clyde (Naranja)
clyde_x = 440
clyde_y = 438
clyde_direction = 0

counter = 0
flicker = False
# Derecha, Arriba, Izquierda, Abajo
turns_allowed = [False, False, False, False]
direction_command = 0
# Velocidad de jugador
player_speed = 2
# Puntos
score = 0
# Powerup, conteo de powerup y fantasmas comidos
power_up = False
powerup_counter = 0
eaten_ghost = [False, False, False, False]
# Objetivos De Los Enemigos (Fantasmas)
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
# Muertes De Enemigos (Fantasmas)
blinky_dead = False
pinky_dead = False
inky_dead = False
clyde_dead = False
# Fantasmas En La Caja De Inicio
blinky_box = False
pinky_box = False
inky_box = False
clyde_box = False

moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
# Vidas Del Pacman (Jugador 1)
lives = 3
game_over = False
game_won = False


#Declarando Clase Para Los Fantasmas
class Ghost:
   def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
      self.x_pos = x_coord
      self.y_pos = y_coord
      self.center_x = self.x_pos + 22
      self.center_y = self.y_pos + 22
      self.target = target
      self.speed = speed
      self.img = img
      self.direction = direct
      self.dead = dead
      self.in_box = box
      self.id = id
      self.turns, self.in_box = self.check_collisions()
      self.rect = self.draw()
            
# Definiendo La Logica De Los Fantasmas Comidos Y El Efecto Powerup
   def draw(self):
      if (not power_up and not self.dead) or (eaten_ghost[self.id] and power_up and not self.dead):
         screen.blit(self.img, (self.x_pos, self.y_pos))
      elif power_up and not self.dead and not eaten_ghost[self.id]:
         screen.blit(spooked_img, (self.x_pos, self.y_pos))
      else:
         screen.blit(dead_img, (self.x_pos, self.y_pos))
      ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
      return ghost_rect
   
   
#Check Collision Para enemigos (Fantasmas)
#Colision De Fantasmas, Paredes Y Caja   
   def check_collisions(self):
# Derecha, Arriba, Izquierda, Abajo
     num1 = ((height - 50) // 32)
     num2 = (width // 30)
     num3 = 15
     self.turns = [False, False, False, False]
     if 0 < self.center_x // 30 < 29:
         if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
         if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
         if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
         if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
         if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

         if self.direction == 2 or self.direction == 3:
            if 12 <= self.center_x % num2 <= 18:
               if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
               if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
               if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
               if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
     else:
            self.turns[0] = True
            self.turns[1] = True
     if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
     else:
            self.in_box = False
     return self.turns, self.in_box
   
#Declarando Movimientos O Giros De Clyde (Fantasma Naranja)
   def move_clyde(self):
# Derecha, Arriba, Izquierda, Abajo
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
#Declarando Movimientos O Giros De Blinky (Fantasma Rojo)   
   def move_blinky(self):
#Blinky Se Va Moviendo Libre Rodeando Las Paredes Y Continuando Donde No Hay Colision
# Derecha, Arriba, Izquierda, Abajo
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
               self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                  self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                  self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
         
    #Declarando Movimientos O Giros De Clyde (Fantasma naranja)
#Declarando Movimientos O Giros De Inky (Fantasma Azul) 
   def move_inky(self):
# Derecha, Arriba, Izquierda, Abajo
# Inky Se Movera Libremente Girando Hacia Arriba Y Hacia Abajo Pero Girara Hacia La 
# Izquierda Y Derecha Solo, Si Hay Colision

        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                  self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction     
#Declarando Movimientos O Giros De Pinky (Fantasma Rosa)
   def move_pinky(self):
# Derecha, Arriba, Izquierda, Abajo
# Inky Girara Hacia La Derecha O Izquierda Buscando Ventaja Contra El Jugador Y Solo Girara Hacia 
# Arriba O Abajo Cuando Sienta Colision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

      
def draw_misc():
      score_text = font.render(f"Puntos: {score}", True, "white" )
      screen.blit(score_text, (10, 920))
      if power_up:
         pygame.draw.circle(screen, "blue", (140, 930), 15)
      for i in range(lives):
         screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
      if game_over:
         pygame.draw.rect(screen,"white", [50, 200, 800, 300],0, 10)
         pygame.draw.rect(screen,"dark gray", [70, 220, 760, 260],0, 10)
         game_over_text = font.render("Game Over, Mala Suerte! Espacio Para Reiniciar!", True, "red")
         screen.blit(game_over_text, ( 100, 300))
      if game_won:
         pygame.draw.rect(screen,"white", [50, 200, 800, 300],0, 10)
         pygame.draw.rect(screen,"dark gray", [70, 220, 760, 260],0, 10)
         game_won_text = font.render("Felicidades, Has Ganado! Espacio Para Reiniciar!", True, "green")
         screen.blit(game_won_text, ( 100, 300))
   
            
            
            
#Check collision para jugador
#Puntos y colision de bolitas que dan puntos tambien
def check_collisions(Score, powerup, powerup_count, eaten_ghosts):
   num1 = (height - 50) // 32
   num2 = width//30
   if 0 < player_x < 870:
      if level[center_y // num1][center_x // num2] == 1:
         level[center_y // num1][center_x // num2] = 0
         #valor de bolitas pequeñas
         Score += 10
      if level[center_y // num1][center_x // num2] == 2:
         level[center_y // num1][center_x // num2] = 0
         #valor de bolitas grandes
         Score += 50
         #powerup y valor del powerup
         powerup = True
         powerup_count = 0
         #Fantasmas comidos
         eaten_ghosts = [False, False, False, False]

   return Score, powerup, powerup_count, eaten_ghosts

#Diseño de nivel
def draw_board(lvl):
  num1 = ((height - 50) // 32)
  num2 = (width // 30)
  for i in range(len(lvl)):
     for j in range(len(level[i])):
       if level[i][j] == 1:
        pygame.draw.circle(screen, "white", (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
       if level[i][j] == 2 and not flicker:
        pygame.draw.circle(screen, "white", (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 10)
       if level[i][j] == 3:
        pygame.draw.line(screen, color, (j * num2 + (0.5* num2), i*num1), 
                         (j * num2 + (0.5 * num2), i*num1+ num1), 3)
       if level[i][j] == 4:
        pygame.draw.line(screen, color, (j * num2, i*num1 + (0.5*num1)),
                         (j * num2 + num2, i*num1 + (0.5*num1)), 3)
       if level[i][j] == 5:
         pygame.draw.arc(screen, color, [(j*num2 - (num2*0.4)) - 2, (i * num1 + (0.5*num1)), num2, num1], 0, pi/2, 3)
       if level[i][j] == 6:
         pygame.draw.arc(screen, color, 
                         [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], pi/2, pi, 3)
       if level[i][j] == 7:
         pygame.draw.arc(screen, color, [(j*num2 + (num2*0.5)), (i * num1 - (0.4*num1)), num2, num1], pi, 3*pi/2, 3)
       if level[i][j] == 8:
         pygame.draw.arc(screen, color, 
                         [(j * num2 - (num2 * 0.4)) - 2,  (i * num1 - (0.4 * num1)), num2, num1], 3*pi/2, 2*pi, 3)
       if level[i][j] == 9:
         pygame.draw.line(screen, "white",(j * num2, i*num1 + (0.5*num1)),
                       (j * num2 + num2, i*num1 + (0.5*num1)), 3)
      
#Diseño de jugador
def draw_player():
  #  0- Derecha, 1- izquierda, 2- arriba, 3- abajo
      if direction == 0:
         screen.blit(player_images[counter // 5], (player_x, player_y))
      elif direction == 1:
         screen.blit(pygame.transform.flip(player_images[counter // 5],True, False), (player_x, player_y))
      elif direction == 2:
         screen.blit(pygame.transform.rotate(player_images[counter // 5], 90,), (player_x, player_y))
      elif direction == 3:
         screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

#Validaciones de posiciones y giros    
def check_position(centerx, centery):
   turns = [False, False, False, False]
   num1 = (height - 50)//32
   num2 = (width // 30)
   num3 = 15
   # revisar colision basada en centro de x y centro del jugador +/- numero falso
   if centerx // 30 < 29:
      if direction == 0:
         if level[centery // num1][(centerx - num3) // num2] < 3:
            turns[1] = True
      if direction == 1:
         if level[centery // num1][(centerx + num3) // num2] < 3:
            turns[0] = True
      if direction == 2:
         if level[(centery + num3) //num1][centerx // num2] < 3:
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
 
# Movimiento de jugador uno (Pacman)
def move_player(play_x, play_y):
# 0 - derecha, 1 - izquierda, 2 - arriba, 3 - abajo
   if direction == 0 and turns_allowed[0]:
      play_x += player_speed
   elif direction == 1 and turns_allowed[1]:
      play_x -= player_speed
   if direction == 2 and turns_allowed[2]:
      play_y -= player_speed
   elif direction == 3 and turns_allowed[3]:
      play_y += player_speed 
   return play_x, play_y

 
def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if power_up:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

 
 
 
      
run = True
while run:
   timer.tick(fps)
   if counter < 19:
      counter += 1
      if counter > 3:
         flicker = False
   
   else:
      counter = 0
      flicker = True
   if power_up and powerup_counter < 600:
      powerup_counter += 1
   elif power_up and powerup_counter >= 600:
      powerup_counter = 0
      power_up = False
      eaten_ghost = [False, False, False, False]
   if startup_counter < 180 and not game_over and not game_won:
      moving = False
      startup_counter += 1
   else: 
      moving = True
      
   screen.fill("black")
   draw_board(level)
   # Centro De Jugador 1 (Pacman)
   center_x = player_x + 23
   center_y = player_y + 24
   if power_up: 
      ghost_speeds = [1, 1, 1, 1]
   else: 
      ghost_speeds = [2, 2, 2, 2]
   if eaten_ghost[0]:
      ghost_speeds[0] = 2
   if eaten_ghost[1]:
      ghost_speeds[1] = 2
   if eaten_ghost[2]:
      ghost_speeds[2] = 2  
   if eaten_ghost[3]:
      ghost_speeds[3] = 2
   if blinky_dead:
      ghost_speeds[0] = 4
   if inky_dead:
      ghost_speeds[1] = 4
   if pinky_dead:
      ghost_speeds[2] = 4
   if clyde_dead:
      ghost_speeds[3] = 4
      
   game_won = True 
   for i in range(len(level)):
      if 1 in level[i] or 2 in level[i]:
         game_won = False
         
         
   player_circle = pygame.draw.circle(screen, "black", (center_x, center_y), 20, 2)
   draw_player()
   # Declarando Los Enemigos (Fantasmas)
   blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                  blinky_box, 0)
   inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                  inky_box, 1)
   pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                  pinky_box, 2)
   clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                  clyde_box, 3)
   draw_misc()
   targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
   
   pygame.draw.circle(screen, "white", (center_x, center_y), 2)
   
   turns_allowed = check_position(center_x, center_y)
   if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
   score, power_up, powerup_counter, eaten_ghost = check_collisions(score, power_up, powerup_counter, eaten_ghost)
   if not power_up:
       if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
          (player_circle.colliderect(inky.rect) and not inky.dead) or \
          (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
          (player_circle.colliderect(clyde.rect) and not clyde.dead):
          if lives > 0:
             lives -= 1
             startup_counter = 0
             power_up = False
             powerup_counter = 0
             player_x = 450
             player_y = 663
             direction = 0
             direction_command = 0
             blinky_x = 56
             blinky_y = 58
             blinky_direction = 0
             inky_x = 440
             inky_y = 388
             inky_direction = 2
             pinky_x = 440 
             pinky_y = 438
             pinky_direction = 0
             clyde_x = 440
             clyde_y = 438
             clyde_direction = 0
             eaten_ghost = [False, False, False, False]
             blinky_dead = False
             pinky_dead = False
             inky_dead = False
             clyde_dead = False
          else: 
             game_over = True
             moving = False
             startup_counter = 0
   if power_up and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
          if lives > 0:
             lives -= 1
             startup_counter = 0
             power_up = False
             powerup_counter = 0
             player_x = 450
             player_y = 663
             direction = 0
             direction_command = 0
             blinky_x = 56
             blinky_y = 58
             blinky_direction = 0
             inky_x = 440
             inky_y = 388
             inky_direction = 2
             pinky_x = 440 
             pinky_y = 438
             pinky_direction = 0
             clyde_x = 440
             clyde_y = 438
             clyde_direction = 0
             eaten_ghost = [False, False, False, False]
             blinky_dead = False
             pinky_dead = False
             inky_dead = False
             clyde_dead = False
   if power_up and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
          if lives > 0:
             lives -= 1
             startup_counter = 0
             power_up = False
             powerup_counter = 0
             player_x = 450
             player_y = 663
             direction = 0
             direction_command = 0
             blinky_x = 56
             blinky_y = 58
             blinky_direction = 0
             inky_x = 440
             inky_y = 388
             inky_direction = 2
             pinky_x = 440 
             pinky_y = 438
             pinky_direction = 0
             clyde_x = 440
             clyde_y = 438
             clyde_direction = 0
             eaten_ghost = [False, False, False, False]
             blinky_dead = False
             pinky_dead = False
             inky_dead = False
             clyde_dead = False
          else: 
             game_over = True
             moving = False
             startup_counter = 0
   if power_up and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:     
          if lives > 0:
             lives -= 1
             startup_counter = 0
             power_up = False
             powerup_counter = 0
             player_x = 450
             player_y = 663
             direction = 0
             direction_command = 0
             blinky_x = 56
             blinky_y = 58
             blinky_direction = 0
             inky_x = 440
             inky_y = 388
             inky_direction = 2
             pinky_x = 440 
             pinky_y = 438
             pinky_direction = 0
             clyde_x = 440
             clyde_y = 438
             clyde_direction = 0
             eaten_ghost = [False, False, False, False]
             blinky_dead = False
             pinky_dead = False
             inky_dead = False
             clyde_dead = False
          else: 
             game_over = True
             moving = False
             startup_counter = 0
   if power_up and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
          if lives > 0:
             lives -= 1
             startup_counter = 0
             power_up = False
             powerup_counter = 0
             player_x = 450
             player_y = 663
             direction = 0
             direction_command = 0
             blinky_x = 56
             blinky_y = 58
             blinky_direction = 0
             inky_x = 440
             inky_y = 388
             inky_direction = 2
             pinky_x = 440 
             pinky_y = 438
             pinky_direction = 0
             clyde_x = 440
             clyde_y = 438
             clyde_direction = 0
             eaten_ghost = [False, False, False, False]
             blinky_dead = False
             pinky_dead = False
             inky_dead = False
             clyde_dead = False
          else: 
             game_over = True
             moving = False
             startup_counter = 0
   if power_up and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]: 
      blinky_dead = True
      eaten_ghost[0] = True
      score += (2 ** eaten_ghost.count(True)) * 100
   if power_up and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]: 
      inky_dead = True
      eaten_ghost[1] = True
      score += (2 ** eaten_ghost.count(True)) * 100
   if power_up and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]: 
      pinky_dead = True
      eaten_ghost[2] = True
      score += (2 ** eaten_ghost.count(True)) * 100
   if power_up and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
      clyde_dead = True
      eaten_ghost[3] = True 
      score += (2 ** eaten_ghost.count(True)) * 100
  

   
# Declaracion De Las Teclas Y Direcciones
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
       run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
       direction_command = 0
      if event.key == pygame.K_LEFT:
       direction_command = 1
      if event.key == pygame.K_UP:
       direction_command = 2
      if event.key == pygame.K_DOWN:
       direction_command = 3
      if event.key == pygame.K_SPACE and (game_over or game_won):
             lives -= 1
             startup_counter = 0
             power_up = False
             powerup_counter = 0
             player_x = 450
             player_y = 663
             direction = 0
             direction_command = 0
             blinky_x = 56
             blinky_y = 58
             blinky_direction = 0
             inky_x = 440
             inky_y = 388
             inky_direction = 2
             pinky_x = 440 
             pinky_y = 438
             pinky_direction = 0
             clyde_x = 440
             clyde_y = 438
             clyde_direction = 0
             eaten_ghost = [False, False, False, False]
             blinky_dead = False
             pinky_dead = False
             inky_dead = False
             clyde_dead = False
             score = 0
             lives = 3
             level = copy.deepcopy(boards)
             game_over = False
             game_won = False
             
             
    if event.type == pygame.KEYUP:
       if event.key == pygame.K_RIGHT and direction_command ==  0:
         direction_command = direction
       if event.key == pygame.K_LEFT and direction_command == 1:
          direction_command = direction
       if event.key == pygame.K_UP  and direction_command == 2:
          direction_command = direction
       if event.key == pygame.K_DOWN and direction_command == 3:
          direction_command = direction
       
   #for i in range(4):    
   for i in range(4):
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
     
   
   if player_x > 900:
      player_x = -47
   elif player_x < -50:
      player_x = 897
   
   
   if blinky.in_box and blinky_dead:
        blinky_dead = False
   if inky.in_box and inky_dead:
        inky_dead = False
   if pinky.in_box and pinky_dead:
        pinky_dead = False
   if clyde.in_box and clyde_dead:
        clyde_dead = False
   
         

   pygame.display.flip()
pygame.quit()



