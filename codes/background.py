from images import *

class Background:
    def __init__(self):
        self.clouds_x = 0
    def draw(self, screen):
        screen.blit(IMAGES["background"], (0, 0))
        screen.blit(IMAGES["clouds"], (self.clouds_x, 0))
        screen.blit(IMAGES["clouds"], (self.clouds_x-screen.get_width(), 0))
        screen.blit(IMAGES["mountain"], (0, 0))
        # screen.blit(IMAGES["card_play_area"], (112, 47))
    def update(self, dt):
        self.clouds_x = (self.clouds_x+dt)%240
