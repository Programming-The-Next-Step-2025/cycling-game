import pygame

BASE_IMG_PATH = "/Users/felixhofer/Documents/GitHub/cycling-game/src/cycling_game/Resources/Images/"

def load_image(path):
    """
    
    """
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img


def scale_screen_up(size, window_size = (640, 420)):
    scaled_size = []
    for n in window_size:
        scaled_size.append(n * size)
    return(tuple(scaled_size))

