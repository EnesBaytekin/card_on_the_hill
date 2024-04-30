import pygame
from game import Game
from images import *
from sys import argv
from os import path

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.SCALED|pygame.FULLSCREEN)
        print(path.join(path.dirname(argv[0]), "resources", "card_on_the_hill.png"))
        pygame.display.set_caption("Card on the Hill")
        pygame.display.set_icon(pygame.image.load(path.join(path.dirname(path.dirname(argv[0])), "resources", "card_on_the_hill.png")).convert_alpha())
        load_images(path.join(path.dirname(path.dirname(argv[0])), "resources"))
        self.game = Game()
        self.running = False
        self.fullscreen = True
    def switch_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen: pygame.display.set_mode((self.width, self.height), pygame.SCALED|pygame.FULLSCREEN)
        else:               pygame.display.set_mode((self.width, self.height), pygame.SCALED)
    def mainloop(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60)/1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.switch_fullscreen()
            self.game.update(dt, events)
            self.screen.fill((128, 128, 128))
            self.game.draw(self.screen)
            pygame.display.flip()
