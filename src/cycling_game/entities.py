import pygame
from cycling_game.animation import get_animation_list
from cycling_game.animation import explosion_animation_list
from cycling_game.animation import get_blood_animation_list
from cycling_game.utils import *

class PhysicsEntity:
    """
    A class representing the player-controlled physics entity.

    Handles animation, explosion effects, movement, and rendering.

    Attributes:
        game: The main game instance.
        type (str): Type of the entity (e.g., 'player').
        pos (list): Position [x, y] of the entity.
        size (tuple): Size (width, height) of the entity.
        velocity (list): Movement velocity [vx, vy].
        animation (list): List of animation frames.
        image (Surface): The current image to display.
        rect (Rect): Pygame rectangle for collisions.
        exploding (bool): If the entity is currently exploding.
        explosion_done (bool): If the explosion animation is finished.
    """
    def __init__(self, game, e_type, pos, size):
        """
        Initializes a PhysicsEntity object.

        Args:
            game: The main game instance.
            e_type (str): The type of the entity.
            pos (tuple): The initial position.
            size (tuple): The size of the entity.
        """
        self.game = game
        self.type = e_type
        self.pos = list(pos) 
        self.size = size
        self.velocity = [0, 0]
       
        # Load player animation frames
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
        # Resize explosion frames to match player scale
        self.explosion_frames = [pygame.transform.scale(f, (130, 130)) for f in self.explosion_frames]
        

    def update(self, movement = (0, 0)):
        """
        Updates the entity’s animation and position.

        Args:
            movement (tuple, optional): Additional movement applied this frame.
        """
        # Get current time for frame update checks
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
        """
        Renders the entity on the given surface.

        Args:
            surf (Surface): The surface to render the entity on.
        """
        surf.blit(self.image, self.pos)
        # Comment next line for testing
        #pygame.draw.rect(surf, (0,0,100), self.rect, border_radius = 10)

    def scale(self, new_size):
        """
        Scales the entity's animation and adjusts the collision box.

        Args:
            new_size (tuple): The new width and height.
        """
        self.animation = [pygame.transform.scale(frame, new_size) for frame in self.animation]
        
        self.image = pygame.transform.scale(self.game.assets["player"], new_size)
        self.rect.size = new_size[0] * 0.72, new_size[1] * 0.2

class Obstacle:
    """
    A class representing static or animated obstacles in the game.

    Handles animation, movement logic, explosion effects, and rendering.

    Attributes vary depending on the obstacle type.
    """
    def __init__(self, game, sprite_key, pos, size):
        """
        Initializes an Obstacle instance.

        Args:
            game: The main game instance.
            sprite_key (str): The key used to fetch the sprite or animation.
            pos (tuple): The position of the obstacle.
            size (tuple): The size of the obstacle.
        """
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.image = self.game.assets[sprite_key]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.layer = str()
        self.sprite_key = sprite_key
        self.stopped = False
        self.last_update = pygame.time.get_ticks()
        self.framerate = 60
        
        if sprite_key == "local":
            self.animation = get_animation_list("Local")
            self.current_frame = 0
            self.image = self.animation[self.current_frame]

            self.exploding = False
            self.explosion_done = False
            self.explosion_index = 0
            self.explosion_frames = get_blood_animation_list()

        if sprite_key == "local_right":
            self.animation = [pygame.transform.flip(frame, True, False) for frame in get_animation_list("Local")]
            self.current_frame = 0
            self.image = self.animation[self.current_frame]

            self.exploding = False
            self.explosion_done = False
            self.explosion_index = 0
            self.explosion_frames = [pygame.transform.flip(frame, True, False) for frame in get_blood_animation_list()]

        if sprite_key == "tourist":
            self.animation = get_animation_list("Tourist")
            self.current_frame = 0
            self.image = self.animation[self.current_frame]
            self.exploding = False
            self.explosion_done = False
            self.explosion_index = 0
            self.explosion_frames = get_blood_animation_list()

        if sprite_key == "escooter":
            self.image = self.game.assets["escooter"]
            self.exploding = False
            self.explosion_done = False
            self.explosion_index = 0
            self.explosion_frames = get_blood_animation_list()
    def update(self, hole_movement = (0, 0)):
        """
        Updates the obstacle’s animation, explosion, and position based on type.

        Args:
            hole_movement (tuple): The movement vector to apply.
        """

        # Update logic for construction and pothole obstacles (movement only)
        if self.sprite_key in ["construction", "pothole"]:
            frame_movement = (hole_movement[0] , hole_movement[1])

            self.pos[0] += frame_movement[0]
            self.pos[1] += frame_movement[1]

        # Update logic for tourist obstacle (animation, movement, explosion)
        if self.sprite_key == "tourist":
            if self.explosion_done:
                return

            now = pygame.time.get_ticks()
            if self.exploding:
                if now - self.last_update > self.framerate:
                    self.last_update = now
                    if self.explosion_index < len(self.explosion_frames):
                        self.image = self.explosion_frames[self.explosion_index]
                        self.explosion_index += 1
                    else:
                        self.exploding = False
                        self.explosion_done = True
                        self.image = pygame.Surface((0, 0))  
            else:
                if now - self.last_update > self.framerate:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.animation)
                    self.image = self.animation[self.current_frame]

                if not self.stopped:
                    self.pos[0] -= (self.game.speed) * 0.6
                if self.stopped:
                    self.pos[0] += self.game.speed
            if not self.stopped:
                self.pos[0] -= (self.game.speed) * 0.6
            if self.stopped:
                self.pos[0] -= self.game.speed

        # Update logic for escooter obstacle
        if self.sprite_key == "escooter":

            if self.explosion_done:
                return

            now = pygame.time.get_ticks()
            if self.exploding:
                if now - self.last_update > self.framerate:
                    self.last_update = now
                    if self.explosion_index < len(self.explosion_frames):
                        self.image = self.explosion_frames[self.explosion_index]
                        self.explosion_index += 1
                    else:
                        self.exploding = False
                        self.explosion_done = True
                        self.image = pygame.Surface((0, 0))  
            else:
                if now - self.last_update > self.framerate:
                    self.last_update = now

                if not self.stopped:
                    self.pos[0] -= (self.game.speed) * 1.1
                if self.stopped:
                    self.pos[0] -= self.game.speed 
                    
            if not self.stopped:
                self.pos[0] -= (self.game.speed) * 1.1
            if self.stopped:
                self.pos[0] -= self.game.speed

        # Update logic for local (right-moving) obstacle
        if self.sprite_key == "local":
            if self.explosion_done:
                return

            now = pygame.time.get_ticks()
            if self.exploding:
                now = pygame.time.get_ticks()
                if self.exploding:
                    if now - self.last_update > self.framerate:
                        self.last_update = now
                        if self.explosion_index < len(self.explosion_frames):
                            self.image = self.explosion_frames[self.explosion_index]
                            self.explosion_index += 1
                        else:
                            self.exploding = False
                            self.explosion_done = True
                            self.image = pygame.Surface((0, 0))  # Hide local after explosion
            else:
                if now - self.last_update > self.framerate:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.animation)
                    self.image = self.animation[self.current_frame]

                if not self.stopped:
                    self.pos[0] += (self.game.speed) * 0.4
                if self.stopped:
                    self.pos[0] -= self.game.speed
            
            if not self.stopped:
                self.pos[0] += (self.game.speed) * 0.4
            if self.stopped:
                self.pos[0] -= self.game.speed

        # Update logic for local_right (left-moving) obstacle
        if self.sprite_key == "local_right":
            if self.explosion_done:
                return

            now = pygame.time.get_ticks()
            if self.exploding:
                if now - self.last_update > self.framerate:
                    self.last_update = now
                    if self.explosion_index < len(self.explosion_frames):
                        self.image = self.explosion_frames[self.explosion_index]
                        self.explosion_index += 1
                    else:
                        self.exploding = False
                        self.explosion_done = True
                        self.image = pygame.Surface((0, 0))  # Hide after explosion
            else:
                if now - self.last_update > self.framerate:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.animation)
                    self.image = self.animation[self.current_frame]

                if not self.stopped:
                    self.pos[0] -= (self.game.speed) * 1.2
                if self.stopped:
                    self.pos[0] += self.game.speed



        # Update logic for static bikestand obstacle
        if self.sprite_key == "bikestand":
            self.pos[0] += hole_movement[0]
            self.pos[1] += hole_movement[1]
            self.rect.midbottom = (
                self.pos[0] + self.image.get_width() * 0.5,
                self.pos[1] + (self.image.get_height() - 50)
            )
        # Default rect update for all other obstacles
        else:
            self.rect.midbottom = (
                self.pos[0] + self.image.get_width() * 0.5,
                self.pos[1] + (self.image.get_height() - 5)
            )
        
    def render(self, surf, collision = False, rect = False):
        """
        Renders the obstacle to the screen, optionally highlighting collisions.

        Args:
            surf (Surface): Surface to render on.
            collision (bool): If True, draws a red collision rectangle.
            rect (bool): If True, draws a green debug rectangle.
        """
        surf.blit(self.image, self.pos)
        #if rect == True:
        #pygame.draw.rect(surf, (0,255,0), self.rect, border_radius = 10)
        if collision == True:
            pygame.draw.rect(surf, (255, 0, 0), self.rect)

    def convert(self, new_size, sprite_key):
        """
        Adjusts the image and rect of the obstacle to a new size based on type.

        Args:
            new_size (tuple): The new size for the sprite.
            sprite_key (str): The key identifying the obstacle type.
        """
        # Adjust rect size and rescale image/animation depending on obstacle type
        self.image = pygame.transform.scale(self.game.assets[sprite_key], new_size)
        self.rect.size = new_size
        if sprite_key == "pothole":
            self.rect.size = new_size[0] * 0.9, new_size[1] * 0.4
        if sprite_key == "construction":
            self.rect.size = new_size[0] * 0.8, new_size[1] * 0.55
        if sprite_key == "tourist":
            self.animation = [pygame.transform.scale(frame, new_size) for frame in self.animation]
            self.rect.size = new_size[0] * 0.8, new_size[1] * 0.6
            self.image = self.animation[self.current_frame]
        if sprite_key == "bikestand":
            self.rect.size = new_size[0] * 0.9, new_size[1] * 0.4
            
        if sprite_key == "local":
            self.animation = [pygame.transform.scale(frame, new_size) for frame in self.animation]
            self.rect.size = new_size[0] * 0.8, new_size[1] * 0.2
            self.image = self.animation[self.current_frame]
        
        if sprite_key == "escooter":
            self.rect.size = new_size[0] * 0.8, new_size[1] * 0.6
   
