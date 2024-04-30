from card import Card
from random import choice
from images import *
from sprite import Sprite

class Deck:
    def __init__(self, x, y, *cards):
        self.x = x
        self.y = y
        self.cards = list(cards)
        self.back_card = Sprite(self.x, self.y, IMAGES["card_back"], self.x, self.y)
        self.selection = 0
    def right(self):
        length = len(self.cards)
        if length > 0:
            self.selection = (self.selection+1)%(length+1)
        else:
            self.selection = 0
    def left(self):
        length = len(self.cards)
        if length > 0:
            self.selection = (self.selection-1)%(length+1)
        else:
            self.selection = 0
    def draw(self, screen):
        screen.blit(IMAGES["card_back"], (self.x, self.y))
        for card in [self.back_card]+self.cards:
            card.draw(screen)
    def update(self, dt, events, gm, objects):
        for i, card in enumerate(self.cards):
            x = self.x+(i+1)*20
            y = self.y
            if i == self.selection:
                y += 6
            card.set_target(x, y)
            card.update(dt, events, gm, objects)
        # back card
        x = self.x
        y = self.y
        if self.can_draw():
            y += 6
        self.back_card.set_target(x, y)
        self.back_card.update(dt, events, gm, objects)
    def get_selected_card(self):
        return self.cards[self.selection]
    def draw_random_card(self):
        card = Card(
            choice((Card.RED, Card.YELLOW, Card.GREEN)),
            choice((Card.ATTACK, Card.ATTACK, Card.ATTACK, Card.SHIELD, Card.HEALTH)),
            choice((1, 2, 3))
        )
        card.x = self.x
        card.y = self.y+6
        self.cards.append(card)
        self.back_card.y = self.y
    def use(self, gm):
        if self.selection != len(self.cards):
            card = self.cards.pop(self.selection)
            card.use(gm)
            if self.selection >= len(self.cards):
                self.left()
            return card
    def can_be_used(self, top_card=None):
        if self.selection == len(self.cards):
            return False
        if top_card == None: return True
        card = self.get_selected_card()
        return card.color == top_card.color or card.type == top_card.type
    def can_draw(self):
        return len(self.cards) == self.selection
