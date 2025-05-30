import pygame
import sys
from cycling_game.cache import image_cache
from pathlib import Path


def get_base_dir():
    """
    Either returns a temporary directory (when being used from the .exe file),
    or returns the directory containing this script

    Returns:
        Path: The base directory path.
    """
    try:
        return Path(sys._MEIPASS)  
    except AttributeError:
        return Path(__file__).resolve().parent  


#  --- Directories ---
BASE_DIR = get_base_dir()
ASSETS_DIR = BASE_DIR / "Resources"
BASE_IMG_PATH = ASSETS_DIR / "Images"
HIGHSCORE_FILE = Path.home() / ".tourist_bowling_highscore.txt"


def load_image(path):
    """
    Loads an image from the disk, converts it for faster blitting with transparency, and caches it.

    Args:
        path (str or Path): The relative path to the image within the BASE_IMG_PATH directory.

    Returns:
        pygame.Surface: The loaded and cached image surface.
    """
    if path not in image_cache:
        full_path = BASE_IMG_PATH / path
        image_cache[path] = pygame.image.load(full_path).convert_alpha()
    return image_cache[path]


def scale_screen_up(size, window_size = (640, 420)):
    """
    Scales a base resolution tuple by a given multiplier.

    Args:
        size (int): The scaling factor.
        window_size (tuple, optional): The original window size. Defaults to (640, 420).

    Returns:
        tuple: The scaled (width, height) dimensions.
    """
    scaled_size = []
    for n in window_size:
        scaled_size.append(n * size)
    return(tuple(scaled_size))

def adjust_rectangle_pos(sprite_image, position, adjustment = (0, 0)):
    """
    Adjusts the position of a sprite based on its image size and a given offset ratio.

    Args:
        sprite_image (pygame.Surface): The image whose dimensions determine the offset.
        position (tuple): The initial (x, y) position.
        adjustment (tuple, optional): The ratio of width and height for offset. Defaults to (0, 0).

    Returns:
        list: The adjusted (x, y) position.
    """
    target_pos = [
        position[0] + sprite_image.get_width() * adjustment[0],
        position[1] + sprite_image.get_height() * adjustment[1]
        ]
    return target_pos

def get_y(obj):
    """
    Gets the bottom y-coordinate of an object with a rect attribute.

    Args:
        obj: Any object with a `rect` attribute that has a `bottom` property.

    Returns:
        int: The y-coordinate of the bottom edge of the rect.
    """
    return obj.rect.bottom

def read_highscore():
    """
    Reads the highscore from the highscore file.

    Returns:
        int: The highscore, or 0 if reading fails or the file doesn't exist.
    """
    if HIGHSCORE_FILE.exists():
        try:
            highscore = int(HIGHSCORE_FILE.read_text().strip())
            return highscore
        except:
            ValueError
            return 0
    return 0

def save_highscore(score):
    """
    Saves a score to the highscore file.

    Args:
        score (int): The score to be saved.
    """
    HIGHSCORE_FILE.write_text(str(score))


def is_lane_empty(game, lane_y, lane_height = 80):
    """
    Checks whether a given lane is free of obstacles.

    Args:
        game: The game instance containing the screen and obstacles.
        lane_y (int): The vertical position of the lane.
        lane_height (int, optional): The height of the lane area. Defaults to 80.

    Returns:
        bool: True if the lane is empty, False otherwise.
    """
    lane_rect = pygame.Rect(0, lane_y, game.screen.get_width(), lane_height)
    for obs in game.obstacles:
        if obs.rect.colliderect(lane_rect) and obs.rect.right > 0:
            return False
    return True

def draw_text_with_outline(surface, text, font, pos, text_color, outline_color):
    """
    Draws text on a surface with a simple four-direction outline.

    Args:
        surface (pygame.Surface): The surface to draw the text on.
        text (str): The text to display.
        font (pygame.font.Font): The font to use.
        pos (tuple): The (x, y) position of the text.
        text_color (tuple): The color of the main text.
        outline_color (tuple): The color of the outline.
    """
    x, y = pos
    outline_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # basic cross outline
    for dx, dy in outline_positions:
        outline_surface = font.render(text, True, outline_color)
        surface.blit(outline_surface, (x + dx, y + dy))
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (x, y))