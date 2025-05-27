import os
import re
from cycling_game.cache import *
from cycling_game.utils import load_image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Resources"
BASE_IMG_PATH = ASSETS_DIR / "Images"

def get_animation_list(sprite):
    if sprite in animation_cache:
        return animation_cache[sprite]
    player_frame_dir = BASE_IMG_PATH / f"{sprite}"
    animation_list = []

    
    for file in sorted(os.listdir(player_frame_dir)):
        relative_path = f"{sprite}/{file}"  
        frame = load_image(relative_path)
        if frame is not None:
            animation_list.append(frame)
        animation_cache[sprite] = animation_list
    return animation_list


def explosion_animation_list():
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
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]


def get_blood_animation_list():
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


