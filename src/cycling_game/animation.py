import os
import re
from cycling_game.cache import *
from cycling_game.utils import load_image
from pathlib import Path
from cycling_game.utils import get_base_dir

BASE_DIR = get_base_dir()
ASSETS_DIR = BASE_DIR / "Resources"
BASE_IMG_PATH = ASSETS_DIR / "Images"

def get_animation_list(sprite):
    """
    Loads a list of animation frames for a given sprite.
    Caches the frames after loading for faster access.

    Args:
        sprite (str): The name of the sprite (also the subfolder name in the image directory).

    Returns:
        list: A list of loaded pygame.Surface objects representing the animation frames.
    """
    if sprite in animation_cache:
        return animation_cache[sprite]
    player_frame_dir = BASE_IMG_PATH / sprite
    animation_list = []

    if not player_frame_dir.exists():
        raise FileNotFoundError(f"Animation folder for '{sprite}' not found at: {player_frame_dir}")

    for file in sorted(os.listdir(player_frame_dir)):
        relative_path = f"{sprite}/{file}"  
        frame = load_image(relative_path)
        if frame is not None:
            animation_list.append(frame)

    animation_cache[sprite] = animation_list
    return animation_list


def explosion_animation_list():
    """
    Loads and returns a list of explosion animation frames.

    Caches the result for reuse.

    Returns:
        list: A list of loaded objects for the explosion animation.
    """

    if "Explosion" in animation_cache:
        return animation_cache["Explosion"]

    explosion_dir = BASE_IMG_PATH / "Explosion"
    explosion_list = []
    for file in sorted(os.listdir(explosion_dir)):
        relative_path = f"Explosion/{file}"
        frame = load_image(relative_path)
        if frame is not None:
            explosion_list.append(frame)

    animation_cache["Explosion"] = explosion_list
    return explosion_list

def natural_key(filename):
    """
    Generates a natural sort key for filenames containing numbers.
    Splits the filename into digit and non-digit parts.

    Args:
        filename (str): The filename to convert into a sort key.

    Returns:
        list: A list of strings and integers used for sorting.
    """
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]


def get_blood_animation_list():
    """
    Loads and returns a list of blood animation frames, sorted naturally.
    Filters for .png files and caches the result for reuse.
    Returns:
        list: A list of loaded pygame.Surface objects for the blood animation.
    """
    if "Blood" in animation_cache:
        return animation_cache["Blood"]
    blood_dir = BASE_IMG_PATH / "Blood"
    blood_animation_list = []
    for file in sorted(os.listdir(blood_dir), key=natural_key):
        if file.endswith(".png"):  
            relative_path = f"Blood/{file}"
            frame = load_image(relative_path)
            if frame is not None:
                blood_animation_list.append(frame)

    animation_cache["Blood"] = blood_animation_list
    return blood_animation_list


