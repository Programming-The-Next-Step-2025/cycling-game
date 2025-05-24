import pygame
import os
import sys
from pathlib import Path
from cycling_game.entities import *
from cycling_game.utils import *
import random

# --- Directories ---
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Resources"
FONT_PATH = ASSETS_DIR / "Font" / "PressStart2P-Regular.ttf"
HIGHSCORE_FILE = BASE_DIR / "highscore.txt"
# -------------------


# -------- Settings ---------
FRAMERATE = 60
WINDOW_SIZE = (1000, 480)
SCREEN_NAME = "Tourist Bowling"
SPEED = 4
SPAWN_POSITION = (200, 350)
SCREEN_BACKGROUND_COLOUR = (125, 125, 125)
# ---------------------------

#Defining game class
class Game:

    def __init__(self):
        
        # Basic Inits and screen creation
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(SCREEN_NAME)
        
        # -- Assets Library -- 
        self.assets = {
            "player": load_image("player.png"),
            "background": load_image("background_3.png"),
            "pothole": load_image("obstacle_rm.png"),
            "construction": load_image("construction.png")
        }

        self.bg = pygame.transform.scale(self.assets["background"], self.screen.get_size())
        self.player = PhysicsEntity(self, "player", SPAWN_POSITION, (8,15))
        self.player.scale((90, 90))
        
        #Creating Movement
        self.movement = [False, False]
        self.back_movement = [False, False]
        self.back_position = [0, 0]

        # Upper & Lower Border 
        self.up_border = pygame.Rect(0, 320, self.screen.get_width(), 10)
        self.down_border = pygame.Rect(0, (self.screen.get_height() - 2), self.screen.get_width(), 1)

        # Create the endless background animation
        self.scroll = 0
        self.speed = 2
        self.start_time = pygame.time.get_ticks()
        self.last_speed_increase_time = self.start_time

        # Spawn in Obstacles, dependent on time interval
        self.obstacles = []
        self.last_spawn = pygame.time.get_ticks()
        # Spacing between obstacles
        self.spawn_delay = 2500

        self.score = 0
        self.score_increment = 1
    

    #Creating the game loop as a function of the game class
    def run(self):

        # --- Main Game Loop ---
        while True:    
            
            self.screen.fill(SCREEN_BACKGROUND_COLOUR)

            # Endless Background Animation
            num_tiles = self.screen.get_width() // self.bg.get_width() + 2

            for i in range(num_tiles):
                x_pos = i * self.bg.get_width() + self.scroll
                if -self.bg.get_width() < x_pos < self.screen.get_width():
                    self.screen.blit(self.bg, (x_pos, 0))
                  
            self.scroll -= self.speed

            if abs(self.scroll) >= self.bg.get_width():
                self.scroll = 0
            
            
            # === Score Increment ===
            self.font = pygame.font.Font(FONT_PATH, 15)
            self.score += self.score_increment
            self.score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(self.score_text, (820, 10))



            # === DIFFICULTY MECHANICS ===

            #Increase scrolling speed & spawn delay of background
            if pygame.time.get_ticks() - self.last_speed_increase_time >= 10000:
                self.speed += 0.5
                if self.spawn_delay > 1000:
                    self.spawn_delay -= 100
                self.last_speed_increase_time = pygame.time.get_ticks()
                
            # =============================

            # Obstacle Spawning Logic
            if pygame.time.get_ticks() - self.last_spawn >= self.spawn_delay:
                
                sprite_key = random.choices(["construction", "pothole"], weights = [1, 3])[0] # 0 because random.choices returns a lsit instead of an int
                new_obstacle = Obstacle(self, sprite_key, [self.screen.get_width(), int()], (75, 75))
                if new_obstacle.sprite_key == "pothole":
                    spawn_y = random.choice([360, 405])
                    new_obstacle.pos[1] = spawn_y
                    new_obstacle.convert((80, 80), sprite_key)
                if new_obstacle.sprite_key == "construction":
                    spawn_y = 340
                    new_obstacle.pos[1] = spawn_y
                    new_obstacle.convert((150, 150), sprite_key)
                self.obstacles.append(new_obstacle)
                self.last_spawn = pygame.time.get_ticks()
                
          
            #                      === RENDERING ===
            self.player.update((0, (self.movement[1] - self.movement[0]) * SPEED))

            for obstacle in self.obstacles:
                obstacle.update((-self.speed, 0))

            # Combine player and obstacles and sort by vertical position
            
            
            renderables = self.obstacles + [self.player]
            renderables.sort(key=lambda obj: (obj.rect.bottom, id(obj)))
            for entity in renderables:
                entity.render(self.screen)

            for obstacle in self.obstacles:
                if self.player.rect.colliderect(obstacle.rect):
                    print("Collision")
            
            self.obstacles = [obs for obs in self.obstacles if obs.rect.right >= 0]

            # =================================================================


            
            # Keeping the player in bound
            if self.player.rect.colliderect(self.up_border) and self.player.rect.bottom <= (self.up_border.bottom + 10):
                self.movement[0] = False
                self.player.pos[1] += 1

            if self.player.rect.colliderect(self.down_border) and self.player.rect.bottom >= self.down_border.top:
                self.movement[1] = False
                self.player.pos[1] -= 1

            # --- Movement mechanics ---
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                    if event.key == pygame.K_RIGHT:
                        self.back_movement[0] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                    if event.key == pygame.K_RIGHT:
                        self.back_movement[0] = True
            

            #Refresh the screen and fix the framerate
            pygame.display.update()
            self.clock.tick(FRAMERATE)

Game().run()