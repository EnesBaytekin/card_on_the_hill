import pygame

class Animation:
    def __init__(self, images, speed, sprite_sheet_frame_count=0):
        if sprite_sheet_frame_count == 0:
            self.images = images
        else:
            self.images = []
            width = images.get_width()//sprite_sheet_frame_count
            height = images.get_height()
            for i in range(sprite_sheet_frame_count):
                image = pygame.Surface((width, height), pygame.SRCALPHA)
                image.blit(images, (0, 0), (i*width, 0, width, height))
                self.images.append(image)
        self.speed = speed # frame per second
        self.animation_start_time = 0
    def get_frame(self, now):
        image_count = len(self.images)
        passed_time = now-self.animation_start_time
        current_image_index = int(passed_time*self.speed)%image_count
        current_frame = self.images[current_image_index]
        return current_frame.copy()
