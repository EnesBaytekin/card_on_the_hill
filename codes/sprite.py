from object import Object
from animation import Animation
from animator import Animator
from images import *

class Sprite(Object):
    def __init__(self, x, y, image, target_x, target_y):
        animations = [
            Animation(image, 0, 1)
        ]
        animator = Animator(animations, 0)
        super().__init__(x, y, animator, is_character=False)
        self.target_x = target_x
        self.target_y = target_y
    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y
    def update(self, dt, events, gm, objects):
        self.x += (self.target_x-self.x)*0.09
        self.y += (self.target_y-self.y)*0.09