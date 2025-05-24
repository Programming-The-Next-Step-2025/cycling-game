import pygame
from cycling_game.animation import get_animation_list
from cycling_game.utils import *

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) 
        self.size = size
        self.velocity = [0, 0]

        self.animation = get_animation_list()
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.framerate = 60

        self.image = self.animation[self.current_frame]
        
        self.rect = pygame.Rect(self.pos[0], self.pos[1], size[0], size[1])
        
    def update(self, movement = (0, 0)):
        # Update the animation frame
        now = pygame.time.get_ticks()
        if now - self.last_update > self.framerate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation)
            self.image = self.animation[self.current_frame]

        # Update the player movement
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        self.rect.topleft = adjust_rectangle_pos(self.image, self.pos, (0.15, 0.6))

    def render(self, surf):
        surf.blit(self.image, self.pos)
        # Comment next line for testing
        #pygame.draw.rect(surf, (0,0,100), self.rect)

    def scale(self, new_size):
        self.animation = [pygame.transform.scale(frame, new_size) for frame in self.animation]
        
        self.image = pygame.transform.scale(self.game.assets["player"], new_size)
        self.rect.size = new_size[0] * 0.72, new_size[1] * 0.35

class Obstacle:
    def __init__(self, game, sprite_key, position, size):
        self.game = game
        self.position = list(position)
        self.size = size
        self.image = self.game.assets[sprite_key]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.layer = str()
    
    def update(self, hole_movement = (0, 0)):
        frame_movement = (hole_movement[0] , hole_movement[1])

        self.position[0] += frame_movement[0]
        self.position[1] += frame_movement[1]

        self.rect.topleft = adjust_rectangle_pos(self.image, self.position, adjustment = (0.05, 0.45))

        
    def render(self, surf, collision = False, rect = False):
        surf.blit(self.image, self.position)
        if rect == True:
            pygame.draw.rect(surf, (0,255,0), self.rect)
            if collision == True:
                pygame.draw.rect(surf, (255, 0, 0), self.rect)
    
    def convert(self, new_size, sprite_key, colour_key):
        self.image = pygame.transform.scale(self.game.assets[sprite_key], new_size)
        self.rect.size = new_size
        self.image.set_colorkey(colour_key)
        self.rect.size = new_size[0] * 0.9, new_size[1] * 0.4

    
