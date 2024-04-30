import pygame
import os
import sys

IMAGES = {}

def load_images(path):
    path = os.path.join(os.path.dirname(sys.argv[0]), "..", path)
    for file_name in os.listdir(path):
        if not file_name.endswith(".png"): continue
        name = file_name[: -4]
        IMAGES[name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha()

        