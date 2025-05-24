import pygame
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Resources"
BASE_IMG_PATH = ASSETS_DIR / "Images" 

def load_image(path):
    """
    
    """
    img = pygame.image.load(BASE_IMG_PATH / path).convert_alpha()
    return img


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


    
