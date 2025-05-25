import os
from cycling_game.utils import load_image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Resources"
BASE_IMG_PATH = ASSETS_DIR / "Images"

def get_animation_list(sprite):
    
    player_frame_dir = BASE_IMG_PATH / f"{sprite}"
    animation_list = []

    for file in sorted(os.listdir(player_frame_dir)):
        frame = load_image(player_frame_dir / file)
        animation_list.append(frame)

    return animation_list

def explosion_animation_list():
    explosion_dir = BASE_IMG_PATH / "Explosion"
    explosion_list = []
    for file in sorted(os.listdir(explosion_dir)):
        frame = load_image("Explosion/" + file)
        explosion_list.append(frame)

    return explosion_list

