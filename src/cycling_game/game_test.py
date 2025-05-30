import pygame
import os
import sys
from pathlib import Path
from cycling_game.entities import *
from cycling_game.utils import *
from cycling_game.animation import *
from cycling_game.utils import get_base_dir
import random

def run():
    """
    Entry point for the game. Initializes and starts the main game logic by creating a Game instance,
    showing the loading screen and main menu, and starting the game loop.
    """
    # --- Directories ---
    BASE_DIR = get_base_dir()
    print(BASE_DIR)
    ASSETS_DIR = BASE_DIR / "Resources"
    FONT_PATH = ASSETS_DIR / "Font" / "PressStart2P-Regular.ttf"
    SOUND_DIR = ASSETS_DIR / "Sounds"
    # -------------------

    # -------- Settings ---------
    FRAMERATE = 60
    WINDOW_SIZE = (1000, 480)
    SCREEN_NAME = "Tourist Bowling"
    SPEED = 4
    SCROLL_SPEED = 10
    SPAWN_POSITION = (200, 350)
    SCREEN_BACKGROUND_COLOUR = (125, 125, 125)
    # ---------------------------

    #Defining game class
    class Game:

        def __init__(self):
            """
            Initializes the game state, loads assets, sets up the display, background, player, 
            obstacle management, scoring, and background music.
            """
            # Basic Inits and screen creation
            pygame.init()
            pygame.font.init()
            pygame.mixer.init()
            # Fix screen tearing with doublebuffer + vsync
            self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED, vsync=1)
            self.clock = pygame.time.Clock()
            pygame.display.set_caption(SCREEN_NAME)
            
            # -- Assets Library -- 
            self.assets = {
                "player": load_image("Player.png"),
                "steer_l": load_image("player_r.png"),
                "background": load_image("Background.png"),
                "pothole": load_image("obstacle_rm.png"),
                "construction": load_image("construction.png"),
                "tourist": load_image("tourist.png"),
                "bikestand": load_image("bikestand.png"),
                "local": load_image("local.png"),
                "local_right": load_image("local.png"),
                "go_background": load_image("back_dark.png"),
                "back2": load_image("back.png"),
                "escooter": load_image("scooter.png")
            }
            self.sounds = {
                "game_sound": pygame.mixer.music.load(str(ASSETS_DIR / "Sounds" / "music.mp3"))
            }

            #self.bg = pygame.transform.scale(self.assets["background"], self.screen.get_size())
            self.bg = self.assets["back2"]

            self.player = PhysicsEntity(self, "player", SPAWN_POSITION, (8,15))
            self.player.scale((90, 90))
            
            #Creating Movement
            self.movement = [False, False]
            self.back_movement = [False, False]
            self.back_position = [0, 0]
            self.steering_up = False

            # Upper & Lower Border 
            self.up_border = pygame.Rect(0, 320, self.screen.get_width(), 10)
            self.down_border = pygame.Rect(0, (self.screen.get_height() - 2), self.screen.get_width(), 1)

            # Create the endless background animation
            self.scroll = 0
            self.speed = SCROLL_SPEED
            self.speed_increase = 0.8
            self.start_time = pygame.time.get_ticks()
            self.last_speed_increase_time = self.start_time

            # Spawn in Obstacles, dependent on time interval
            self.obstacles = []
            self.spawn = False
            self.last_spawn = pygame.time.get_ticks()
            # Spacing between obstacles
            self.spawn_delay = random.randint(500, 700)
            #Tourist Spawning
            self.tourist_spawn = pygame.time.get_ticks()


            # Scores
            self.score = 0
            self.highscore = read_highscore()
            self.score_increment = 1

            # Game Over
            self.game_over = False

            #Loading and Playing Music
            pygame.mixer.music.load(ASSETS_DIR / "Sounds" / "music.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)  # -1 loops forever
        #Creating the game loop as a function of the game class
        def run(self):
            """
            The main game loop that handles rendering, user input, background scrolling, obstacle spawning,
            collision detection, score management, and game-over behavior.
            """
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
                draw_text_with_outline(self.screen, f"Score: {self.score}", self.font, (720, 10), (255, 255, 255), (0, 0, 0))
                draw_text_with_outline(self.screen, f"Highscore: {self.highscore}", self.font, (720, 25), (255, 255, 255), (0, 0, 0))

                if self.score > self.highscore:
                    self.highscore = self.score
                    save_highscore(self.score)
                        

                # === DIFFICULTY MECHANICS ===

                #Increase scrolling speed & spawn delay of background
                if pygame.time.get_ticks() - self.last_speed_increase_time >= 10000:
                    self.speed += self.speed_increase
                    if self.spawn_delay > 1000:
                        self.spawn_delay -= 100
                    self.last_speed_increase_time = pygame.time.get_ticks()
                    
            

                #  === Obstacle Spawning Logic ====
                if pygame.time.get_ticks() - self.last_spawn >= self.spawn_delay and not self.game_over:
                    self.spawn = True

                if self.spawn == True:
                    if self.score < 1000:
                        weights = [ 5, 3, 4, 4, 4, 2]
                    else:
                        weights = [ 4, 1, 7, 6, 7, 5]

                    sprite_key = random.choices(["pothole", "tourist", "local", "bikestand", "local_right", "escooter"], weights = weights)[0]
                    lanes = [350, 340, 400]
                    new_obstacle = Obstacle(self, sprite_key, [self.screen.get_width(), 0], (75, 75))

                    if sprite_key == "pothole":
                        spawn_y = random.choice([360, 405])
                        new_obstacle.pos[1] = spawn_y
                        new_obstacle.convert((80, 80), sprite_key)
                        self.obstacles.append(new_obstacle)

                    elif sprite_key == "construction":
                        spawn_y = 340
                        new_obstacle.pos[1] = spawn_y
                        new_obstacle.convert((150, 150), sprite_key)
                        self.obstacles.append(new_obstacle)

                    elif sprite_key == "tourist":
                        spawn_y = 300
                        new_obstacle.pos[1] = spawn_y
                        new_obstacle.convert((85, 85), sprite_key)
                        self.obstacles.append(new_obstacle)

                    elif sprite_key == "bikestand":
                        spawn_y = 300
                        new_obstacle.pos[1] = spawn_y
                        new_obstacle.convert((130, 130), sprite_key)
                        self.obstacles.append(new_obstacle)

                    elif sprite_key == "local":
                        possible_lanes = [y for y in lanes if is_lane_empty(self, y)]
                        if possible_lanes:
                            spawn_y = random.choice(possible_lanes)
                            spawn_x = -70
                            new_obstacle.pos[1] = spawn_y
                            new_obstacle.pos[0] = spawn_x
                            new_obstacle.convert((80, 80), sprite_key)
                            self.obstacles.append(new_obstacle)

                    elif sprite_key == "local_right":
                        possible_lanes = [y for y in lanes if is_lane_empty(self, y)]
                        if possible_lanes:
                            spawn_y = random.choice(possible_lanes)
                            spawn_x = self.screen.get_width() + 70
                            new_obstacle.pos[1] = spawn_y
                            new_obstacle.pos[0] = spawn_x
                            new_obstacle.convert((80, 80), "local")
                            self.obstacles.append(new_obstacle)

                    elif sprite_key == "escooter":
                        spawn_y = 300
                        new_obstacle.pos[1] = spawn_y
                        new_obstacle.convert((100, 100), sprite_key)
                        self.obstacles.append(new_obstacle)

                    self.last_spawn = pygame.time.get_ticks()
                    self.spawn = False
                    
                    
                #                      === RENDERING ===
                if not self.player.explosion_done:
                    self.player.update((0, (self.movement[1] - self.movement[0]) * SPEED))

                for obstacle in self.obstacles:
                    obstacle.update((-self.speed, 0))

                # Combine player and obstacles and sort by vertical position
                renderables = self.obstacles + [self.player]
                renderables.sort(key=lambda obj: (obj.rect.bottom, id(obj)))
                for entity in renderables:
                    entity.render(self.screen)

                # New collision logic for locals hitting potholes or construction
                for local in [o for o in self.obstacles if o.sprite_key in ["local", "local_right", "escooter"]]:
                    for other in self.obstacles:
                        if other.sprite_key in ["pothole", "construction", "bikestand"] and local.rect.colliderect(other.rect):
                            local.stopped = True
                            local.exploding = True

                #Collision Logic so tourist can be run over
                for tourist in [o for o in self.obstacles if o.sprite_key in ["tourist"]]:
                    for other in self.obstacles:
                        if other.sprite_key in ["escooter"] and tourist.rect.colliderect(other.rect):
                            tourist.stopped = True
                            tourist.exploding = True

                # for tourist in [o for o in self.obstacles if o.sprite_key in ["tourist"]]:
                #     if tourist.rect.colliderect(self.player.rect):
                #         tourist.stopped = True
                #         tourist.exploding = True

                for obstacle in self.obstacles:
                    if self.player.rect.colliderect(obstacle.rect):
                        self.player.exploding = True
                        self.speed = 0
                        self.speed_increase = 0
                        self.game_over = True
                        
                
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
                            #self.steering_up = True
                        if event.key == pygame.K_DOWN:
                            self.movement[1] = True
                        if event.key == pygame.K_RIGHT:
                            self.back_movement[0] = True
                        if event.key == pygame.K_SPACE and self.game_over:
                            self.restart()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.movement[0] = False
                            #self.steering_up = False
                        if event.key == pygame.K_DOWN:
                            self.movement[1] = False
                        if event.key == pygame.K_RIGHT:
                            self.back_movement[0] = True
                
                if self.game_over:
                    self.score_increment = 0
                    game_over_font = pygame.font.Font(FONT_PATH, 30)
                    info_font = pygame.font.Font(FONT_PATH, 10)
                    # Prepare rects for positioning
                    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
                    info_text = info_font.render("Press Space to Restart", True, (255, 0, 0))
                    info_text_rect = info_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.5))
                    go_text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
                    self.bg = self.assets["go_background"]
                    draw_text_with_outline(self.screen, "GAME OVER", game_over_font, go_text_rect.topleft, (255, 0, 0), (0, 0, 0))
                    draw_text_with_outline(self.screen, "Press Space to Restart", info_font, info_text_rect.topleft, (255, 0, 0), (0, 0, 0))
                #Refresh the screen and fix the framerate
                pygame.display.update()
                self.clock.tick(FRAMERATE)
        
       
        def restart(self):
            """
            Restarts the game by reinitializing the Game class and re-entering the game loop.
            """
            self.__init__()
            self.run()
        

        def main_menu(self):
            """
            Displays the main menu with the game title, highscore, and prompt to start the game.
            Waits for the user to press SPACE to begin.
            """
            font = pygame.font.Font(FONT_PATH, 30)
            info_font = pygame.font.Font(FONT_PATH, 10)
            highscore_font = pygame.font.Font(FONT_PATH, 10)
            title_text = font.render("TOURIST BOWLING", True, (255, 0, 0))
            start_text = info_font.render("Press SPACE to Start", True, (255, 255, 255))
            highscore_text = highscore_font.render(f"Highscore: {self.highscore}", True, (255, 0, 0))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
            start_rect = start_text.get_rect(center=(self.screen.get_width() // 2, int(self.screen.get_height() // 2.2)))
            highscore_rect = highscore_text.get_rect(center=(self.screen.get_width() // 2, int(self.screen.get_height() // 2)))
            while True:
                bg = self.assets["back2"]
                bg_width = bg.get_width()
                bg_height = bg.get_height()

                # Tile the image across the full screen
                for x in range(0, self.screen.get_width(), bg_width):
                    for y in range(0, self.screen.get_height(), bg_height):
                        self.screen.blit(bg, (x, y))
                draw_text_with_outline(self.screen, "TOURIST BOWLING", font, title_rect.topleft, (255, 0, 0), (0, 0, 0))
                draw_text_with_outline(self.screen, "Press SPACE to Start", info_font, start_rect.topleft, (255, 255, 255), (0, 0, 0))
                draw_text_with_outline(self.screen, f"Highscore: {self.highscore}", highscore_font, highscore_rect.topleft, (255, 0, 0), (0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return
                pygame.display.update()
        def loading_screen(self):
            """
            Displays a temporary loading screen with a 'LOADING...' message before transitioning to the main menu.
            """
            loading_font = pygame.font.Font(FONT_PATH, 20)
            loading_text = loading_font.render("LOADING...", True, (255, 255, 255))
            text_rect = loading_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            
            self.screen.fill(SCREEN_BACKGROUND_COLOUR)
            self.screen.blit(loading_text, text_rect)
            pygame.display.update()

            
            pygame.time.delay(1500)  
            
    game = Game()
    game.loading_screen()
    game.main_menu()
    game.run()