import os
from cycling_game.utils import load_image


def get_animation_list(sprite):
    
    player_frame_dir = f"/Users/felixhofer/Documents/GitHub/cycling-game/src/cycling_game/Resources/Images/{sprite}"
    
    animation_list = []

    for file in sorted(os.listdir(player_frame_dir)):
        frame = load_image(f"{sprite}/" + file)
        animation_list.append(frame)

    return animation_list

def explosion_animation_list():
    explosion_dir = "/Users/felixhofer/Documents/GitHub/cycling-game/src/cycling_game/Resources/Images/Explosion/"
    explosion_list = []
    for file in sorted(os.listdir(explosion_dir)):
        frame = load_image("Explosion/" + file)
        explosion_list.append(frame)

    return explosion_list

