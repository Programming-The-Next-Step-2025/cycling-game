import pygame
import sys
from cycling_game.entities import PhysicsEntity
from cycling_game.utils import *

# -------- Settings ---------
FRAMERATE = 60
WINDOW_SIZE = (1000, 480)
SCREEN_NAME = "Tourist Bowling"
SPEED = 3
SPAWN_POSITION = (200, 350)
SCREEN_BACKGROUND_COLOUR = (125, 125, 125)

# ---------------------------

#Defining game class
class Game:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        #Scale up the screen to scale the sprites
        #self.display = pygame.Surface(scale_screen_up(1, window_size = WINDOW_SIZE))

        self.clock = pygame.time.Clock()
        pygame.display.set_caption(SCREEN_NAME)
        
        # -- Assets Library -- 
        self.assets = {
            "player": load_image("player_sprite.png"),
            "background": load_image("background.png"),
            "obstacle": load_image("obstacle.png")
        }
        self.bg = pygame.transform.scale(self.assets["background"], self.screen.get_size())
        self.player = PhysicsEntity(self, "player", SPAWN_POSITION, (8,15))
        self.player.scale((70, 70))
        
        #Creating Movement
        self.movement = [False, False]
        self.back_movement = [False, False]
        self.back_position = [0, 0]

        self.up_border = pygame.Rect(0, 320, self.screen.get_width(), 10)
        self.down_border = pygame.Rect(0, (self.screen.get_height() - 2), self.screen.get_width(), 1)
       
        # Create the endless background animation
        self.scroll = 0
        self.speed = 1
        self.start_time = pygame.time.get_ticks()
        self.last_speed_increase_time = self.start_time

    #Creating the game loop as a function of the game class
    def run(self):

        # --- Main Game Loop ---
        while True:    
            
            self.screen.fill(SCREEN_BACKGROUND_COLOUR)

            num_tiles = self.screen.get_width() // self.bg.get_width() + 2

            for i in range(num_tiles):
                x_pos = i * self.bg.get_width() + self.scroll
                if -self.bg.get_width() < x_pos < self.screen.get_width():
                    self.screen.blit(self.bg, (x_pos, 0))
                
            self.scroll -= self.speed

            if abs(self.scroll) >= self.bg.get_width():
                self.scroll = 0
            
            
            if pygame.time.get_ticks() - self.last_speed_increase_time >= 10000:
                self.speed += 1
                self.last_speed_increase_time = pygame.time.get_ticks()
            # pygame.draw.rect(self.screen, (255, 0, 0), self.down_border)
            # pygame.draw.rect(self.screen, (0, 200, 0), self.player.rect)
            self.player.update((0, (self.movement[1] - self.movement[0]) * SPEED))
            self.player.render(self.screen)
            
            # Collision Mechanics
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