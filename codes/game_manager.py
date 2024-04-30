from images import *
import pygame
import pygame.font
from sys import argv
from os import path

pygame.font.init()

class GameManager:
    def __init__(self, character_count):
        self.character_count = character_count
        self.turn = 0
        self.top_card = None
        self.played_cards = []
        self.playing_card_type = 0
        self.playing_card_level = 1
        self.select_from_enemy = False
        self.played_by_enemy = False
        self.character_selection = 0
        self.character = None
        self.enemy_count = 2
        self.hero_count = 1
        self.timer = 0
        self.state = "combat"
        self.state_changed = True
        self.dcolor = (0, 0, 0)
        self.new_level = False
        self.blend_rgba = pygame.BLEND_RGBA_SUB
        self.font = pygame.font.Font(path.join(path.dirname(path.dirname(argv[0])), "resources", "5x5monospace.ttf"), 10)
        self.end_image = pygame.Surface((11, 4), pygame.SRCALPHA)
        self.end_image.set_alpha(0)
        for x in range(11):
            for y in range(4):
                if (x, y) in ((0, 1), (0, 2),
                                        (1, 0), (1, 2), (1, 3),
                                        (2, 0), (2, 1), (2, 3),
                                        (4, 1), (4, 2), (4, 3),
                                        (5, 1),
                                        (6, 2), (6, 3),
                                        (8, 2), (8, 3),
                                        (9, 1), (9, 3),
                                        (10, 0), (10, 1), (10, 2), (10, 3)):
                    self.end_image.set_at((x, y), (0, 0, 0, 255))
        self.level = 1
    def next_turn(self):
        self.turn = (self.turn+1)%self.character_count
    def get_current_character(self, objects):
        characters = []
        for object in objects:
            if object.is_character:
                characters.append(object)
        characters.sort(key=lambda c: c.id)
        return characters[self.turn]
    def draw(self, screen):
        screen.blit(self.font.render(f"level {self.level}", True, (0, 0, 0)), (3, 3))
        screen.blit(self.font.render(f"level {self.level}", True, (0, 0, 0)), (2, 3))
        screen.blit(self.font.render(f"level {self.level}", True, (0, 0, 0)), (3, 2))
        screen.blit(self.font.render(f"level {self.level}", True, (255, 255, 255)), (2, 2))
        for card in self.played_cards:
            card.draw(screen)
        if self.character and self.character.state == "select":
            image = IMAGES["arrow"]
            x = screen.get_width()//2-image.get_width()//2
            y = 120-self.character_selection*24
            if (not self.select_from_enemy and self.hero_count == 1) \
            or (self.select_from_enemy and self.enemy_count == 1):
                y = 108
            if not self.select_from_enemy:
                x -= 32
            flip_x = not self.select_from_enemy
            image = pygame.transform.flip(image, flip_x, False)
            screen.blit(image, (x, y))
        if self.state != "combat":
            screen.fill(self.dcolor, special_flags=self.blend_rgba)
            if self.state == "end_game":
                x = screen.get_width()//2-5
                y = screen.get_height()//2-2
                screen.blit(self.end_image, (x, y))
    def set_state(self, state):
        self.state = state
        self.timer = 0
        self.state_changed = True
    def update(self, dt, events, objects):
        self.timer += dt
        enemy_count = 0
        hero_count = 0
        for object in objects:
            if object.is_character and object.is_enemy:
                enemy_count += 1
            elif object.is_character and not object.is_enemy:
                hero_count += 1
        self.enemy_count = enemy_count
        self.hero_count = hero_count
        self.character_count = enemy_count+hero_count
        if self.state == "combat":
            if self.state_changed:
                self.state_changed = False
            if self.enemy_count == 0:
                self.set_state("change_level")
            if self.hero_count == 0:
                self.set_state("end_game")
            self.character = self.get_current_character(objects)
            for card in self.played_cards:
                card.update(dt, events, self, objects)
            if len(self.played_cards) > 0:
                self.top_card = self.played_cards[-1]
            else:
                self.top_card = None
            if len(self.played_cards) > 2:
                card = self.played_cards.pop(0)
                card.delete()
        elif self.state == "change_level":
            if self.state_changed:
                self.state_changed = False
                self.blend_rgba = pygame.BLEND_RGBA_SUB
            self.new_level = False
            if self.timer < 2:
                v = min(max(255*self.timer/2, 0), 255)
            elif self.timer < 3:
                if self.timer < 2+dt:
                    self.new_level = True
                    self.turn = 0
                    self.played_cards.clear()
                v = 255
            elif self.timer < 5:
                v = min(max(255*(5-self.timer)/2, 0), 255)
            else:
                v = 0
                self.set_state("combat")
            self.dcolor = (v, v, v)
        elif self.state == "end_game":
            if self.state_changed:
                self.state_changed = False
                self.blend_rgba = pygame.BLEND_RGBA_ADD
            if self.timer < 5:
                v = min(max(255*self.timer/5, 0), 255)
            else:
                v = 255
            self.dcolor = (v, v, v)
            alpha = 255-min(max(255*(8-self.timer)/3, 0), 255)
            self.end_image.set_alpha(alpha)