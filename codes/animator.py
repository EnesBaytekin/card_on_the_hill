from time import time
import pygame
import pygame.mask

class Animator:
    def __init__(self, animations, animation_index, offset_x=0, offset_y=0, flip_x=False, flip_y=False):
        self.animations = animations
        self.animation_index = animation_index
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.alpha = 255
        self.fill = False
        self.color = (255, 255, 255)
    def get_frame(self):
        now = time()
        current_animation = self.animations[self.animation_index]
        return current_animation.get_frame(now)
    def draw(self, screen, x, y):
        image = self.get_frame()
        # offset_x = image.get_width()-self.offset_x if self.flip_x else self.offset_x
        # offset_y = image.get_width()-self.offset_y if self.flip_y else self.offset_y
        offset_x = self.offset_x
        offset_y = self.offset_y
        image.set_alpha(self.alpha)
        if self.fill:
            image.fill((208, 208, 208, 0), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(pygame.transform.flip(image, self.flip_x, self.flip_y), (x-offset_x, y-offset_y))
    def start_animation_from_beginning(self, animation_index):
        now = time()
        self.animation_index = animation_index
        current_animation = self.animations[self.animation_index]
        current_animation.animation_start_time = now
    def start_animation_if_different(self, animation_index):
        if animation_index != self.animation_index:
            self.start_animation_from_beginning(animation_index)


