import os
from cycling_game.utils import load_image


def get_animation_list():
    
    player_frame_dir = "/Users/felixhofer/Documents/GitHub/cycling-game/src/cycling_game/Resources/Images/Player"

    animation_list = []

    for file in sorted(os.listdir(player_frame_dir)):
        frame = load_image("Player/" + file)
        animation_list.append(frame)

    return animation_list