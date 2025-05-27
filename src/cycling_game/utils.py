import pygame
from cycling_game.cache import image_cache
from pathlib import Path

#  --- Directories ---
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Resources"
BASE_IMG_PATH = ASSETS_DIR / "Images" 
HIGHSCORE_FILE = BASE_DIR / "highscore.txt"


def load_image(path):
    if path not in image_cache:
        full_path = BASE_IMG_PATH / path
        image_cache[path] = pygame.image.load(full_path).convert_alpha()
    return image_cache[path]


def scale_screen_up(size, window_size = (640, 420)):
    scaled_size = []
    for n in window_size:
        scaled_size.append(n * size)
    return(tuple(scaled_size))

def adjust_rectangle_pos(sprite_image, position, adjustment = (0, 0)):
    target_pos = [
        position[0] + sprite_image.get_width() * adjustment[0],
        position[1] + sprite_image.get_height() * adjustment[1]
        ]
    return target_pos

def get_y(obj):
    return obj.rect.bottom

def read_highscore():
    if HIGHSCORE_FILE.exists():
        try:
            highscore = int(HIGHSCORE_FILE.read_text().strip())
            return highscore
        except:
            ValueError
            return 0
    return 0

def save_highscore(score):
    HIGHSCORE_FILE.write_text(str(score))


def is_lane_empty(game, lane_y, lane_height = 80):
    lane_rect = pygame.Rect(0, lane_y, game.screen.get_width(), lane_height)
    for obs in game.obstacles:
        if obs.rect.colliderect(lane_rect) and obs.rect.right > 0:
            return False
    return True

def draw_text_with_outline(surface, text, font, pos, text_color, outline_color):
    x, y = pos
    outline_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # basic cross outline
    for dx, dy in outline_positions:
        outline_surface = font.render(text, True, outline_color)
        surface.blit(outline_surface, (x + dx, y + dy))
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (x, y))