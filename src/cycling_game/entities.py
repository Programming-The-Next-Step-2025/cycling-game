import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) 
        self.size = size
        self.velocity = [0, 0]
        self.image = self.game.assets["player"]

        self.rect = pygame.Rect(self.pos[0], self.pos[1], size[0], size[1])
        
    def update(self, movement = (0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        self.rect.topleft = (self.pos[0] + 5, self.pos[1] + 32) # Manual adjustments to have the hitbox only over the bike

    def render(self, surf):
        surf.blit(self.image, self.pos)
        pygame.draw.rect(surf, (0,0,100), self.rect)

    def scale(self, new_size):
        self.image = pygame.transform.scale(self.game.assets["player"], new_size)
        self.rect.size = new_size[0] * 0.9, new_size[1] / 2

class Obstacle:
    def __init__(self, game, sprite_key, position, size):
        self.game = game
        self.position = list(position)
        self.size = size
        self.image = self.game.assets[sprite_key]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        
    
    def update(self, hole_movement = (0, 0)):
        frame_movement = (hole_movement[0] , hole_movement[1])

        self.position[0] += frame_movement[0]
        self.position[1] += frame_movement[1]

        self.rect.topleft = (self.position[0], self.position[1])
    
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