import pygame
from cycling_game.animation import get_animation_list
from cycling_game.animation import explosion_animation_list
from cycling_game.utils import *

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) 
        self.size = size
        self.velocity = [0, 0]

        self.animation = get_animation_list("Player")
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.framerate = 60

        self.image = self.animation[self.current_frame]
        
        self.rect = pygame.Rect(self.pos[0], self.pos[1], size[0], size[1])
        
        self.exploding = False
        self.explosion_done = False
        self.explosion_index = 0
        self.explosion_timer = 0
        self.explosion_frames = explosion_animation_list()
        self.explosion_frames = [pygame.transform.scale(f, (130, 130)) for f in self.explosion_frames]
        

    def update(self, movement = (0, 0)):
        # Update the animation frame
        now = pygame.time.get_ticks()
        
        if now - self.last_update > self.framerate and self.exploding == False:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation)
            self.image = self.animation[self.current_frame]
        if now - self.last_update > self.framerate and self.exploding:
            if self.explosion_index < len(self.explosion_frames):
                self.image = self.explosion_frames[self.explosion_index]
                self.explosion_index += 1
                
            else:
                self.exploding = False
                self.explosion_done = True
                self.image = pygame.Surface((0, 0))  # Hide player after explosion


        # Update the player movement
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        self.rect.midbottom = (
            self.pos[0] + self.image.get_width() * 0.5,
            self.pos[1] + self.image.get_height() * 0.95
        )

    def render(self, surf):
        surf.blit(self.image, self.pos)
        # Comment next line for testing
        #pygame.draw.rect(surf, (0,0,100), self.rect, border_radius = 10)

    def scale(self, new_size):
        self.animation = [pygame.transform.scale(frame, new_size) for frame in self.animation]
        
        self.image = pygame.transform.scale(self.game.assets["player"], new_size)
        self.rect.size = new_size[0] * 0.72, new_size[1] * 0.2

class Obstacle:
    def __init__(self, game, sprite_key, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.image = self.game.assets[sprite_key]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.layer = str()
        self.sprite_key = sprite_key

        if sprite_key == "local":
            self.animation = get_animation_list("Local")
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()
            self.framerate = 60
            self.image = self.animation[self.current_frame]

    def update(self, hole_movement = (0, 0)):

        if self.sprite_key in ["construction", "pothole"]:
            frame_movement = (hole_movement[0] , hole_movement[1])

            self.pos[0] += frame_movement[0]
            self.pos[1] += frame_movement[1]

        if self.sprite_key == "tourist":
            self.pos[0] -= 4

        if self.sprite_key == "local":
            now = pygame.time.get_ticks()
        
            if now - self.last_update > self.framerate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animation)
                self.image = self.animation[self.current_frame]
            self.pos[0] += (self.game.speed + 1)

        self.rect.midbottom = (
                self.pos[0] + self.image.get_width() * 0.5,
                self.pos[1] + (self.image.get_height()- 5) 
            )

        
    def render(self, surf, collision = False, rect = False):
        surf.blit(self.image, self.pos)
        #if rect == True:
        #pygame.draw.rect(surf, (0,255,0), self.rect, border_radius = 10)
        if collision == True:
            pygame.draw.rect(surf, (255, 0, 0), self.rect)

    def convert(self, new_size, sprite_key):
        self.image = pygame.transform.scale(self.game.assets[sprite_key], new_size)
        self.rect.size = new_size
        if sprite_key == "pothole":
            self.rect.size = new_size[0] * 0.9, new_size[1] * 0.4
        if sprite_key == "construction":
            self.rect.size = new_size[0] * 0.8, new_size[1] * 0.6
        if sprite_key == "tourist":
            self.rect.size = new_size[0] * 0.8, new_size[1] * 0.6
        if sprite_key == "local":
            self.animation = [pygame.transform.scale(frame, new_size) for frame in self.animation]
            self.rect.size = new_size[0] * 0.8, new_size[1] * 0.2
            self.image = self.animation[self.current_frame]

