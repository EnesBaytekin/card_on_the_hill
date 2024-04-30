from images import *
from sprite import Sprite

class Card(Sprite):
    ATTACK = 0
    SHIELD = 1
    HEALTH = 2
    RED    = 0
    GREEN  = 1
    YELLOW = 2
    def __init__(self, color, type, level=1):
        self.color = color
        self.type = type
        self.level = level
        t = ("sword", "shield", "health")[self.type]
        c = ("red", "green", "yellow")[self.color]
        image = IMAGES[f"card_{c}_{t}"].copy()
        if self.color == self.RED   : color = (213, 181, 181)
        if self.color == self.YELLOW: color = (230, 224, 179)
        if self.color == self.GREEN : color = (189, 217, 162)
        for i in range(self.level):
            image.set_at((2+2*i, 2), color)
            # card.set_at((2+2*i, 18), color)
            # card.set_at((12-2*i, 2), color)
            image.set_at((12-2*i, 18), color)
        x = 112
        y = 47
        super().__init__(x, y, image, x, y)
    # def draw(self, screen, x, y):
    #     screen.blit(card, (x, y))
    def use(self, gm):
        # print(f"type: {self.type}, level: {self.level}")
        gm.playing_card_type = self.type
        gm.playing_card_level = self.level
        gm.select_from_enemy = not (
            (gm.played_by_enemy and self.type == Card.ATTACK) or
            (not gm.played_by_enemy and self.type != Card.ATTACK)
        )
