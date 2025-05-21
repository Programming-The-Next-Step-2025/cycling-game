import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) 
        self.size = size
        self.velocity = [0, 0]
        self.image = self.game.assets["player"]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


    def update(self, movement = (0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        self.rect.topleft = (self.pos[0], self.pos[1])

    def render(self, surf):
        surf.blit(self.image, self.pos)

    def scale(self, new_size):
        self.image = pygame.transform.scale(self.game.assets["player"], new_size)
        self.rect.size = new_size

class Obstacle:
    def __init__(self, size, position, image):
        self.position = list(position)
        self.image = self.game.assets["obstacle"]
        self.rect = pygame.Rect(self.position[0], self.pos[1], self.size[0], self.size[1])
        self.size = size
    
    def update(self, hole_movement = (0, 0)):
        frame_movement = (hole_movement[0] , hole_movement[1])

        self.position[0] += frame_movement[0]
        self.position[1] += frame_movement[1]

        self.rect.topleft = (self.position[0], self.position[1])
    
    def render(self, surf):
        surf.blit(self.image, self.position)