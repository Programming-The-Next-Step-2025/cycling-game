import pygame

def greet(user):
    print(f"Hello {user}")

def load_image(BASE_IMG_PATH, path):
    """
    Loads an image and converts it for performance increase while keeping support
    for transparent sprites

    Args:
        BASE_IMG_PATH: Normally hardcoded to the repository, for the purposes of this assignment
        an argument of the function
        Path: The filepath for the image or sprite to be loaded

    Returns: A converted pygame image object
    """
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img

def scale_screen_up(size, window_size = (640, 420)):
    """
    Scales a sprite up to the desired resolution (a multiple of the image size)

    Args:
        size: The desired multiple of the window size
        window_size: A tuple with the window size dimensions in pixels

    Returns: A tuple with the correct size to be passed to another function

    """
    scaled_size = []
    for n in window_size:
        scaled_size.append(n * size)
    return(tuple(scaled_size))