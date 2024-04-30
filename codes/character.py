import pygame
import pygame.draw
from object import Object
from animation import Animation
from animator import Animator
from images import *
from deck import Deck
from card import Card
from random import randrange

class Character(Object):
    def __init__(self, id, type, x, y, health, shield, is_enemy):
        self.id = id
        self.type = type
        if self.type == 0:
            animations = [
                Animation(IMAGES["character0"], 8, 8),
            ]
            animator = Animator(animations, 0, offset_x=17, offset_y=40)
        elif self.type == 1:
            animations = [
                Animation(IMAGES["character1"], 8, 8),
            ]
            animator = Animator(animations, 0, offset_x=25, offset_y=56)
        elif self.type == 2:
            animations = [
                Animation(IMAGES["character2"], 8, 14),
            ]
            animator = Animator(animations, 0, offset_x=21, offset_y=44)
        super().__init__(x, y, animator, is_character=True)
        self.health = health
        self.max_health = health
        self.shield = 0
        self.max_shield = shield
        self.is_enemy = is_enemy
        if self.is_enemy:
            self.animator.flip_x = True
        self.dead = False
        self.state = "idle"
        self.state_timer = 0
        self.state_changed = True
        self.deck = Deck(
            16, 16
        )
        for _ in range(4):
            self.deck.draw_random_card()
        self.selected = False
    def draw(self, screen):
        super().draw(screen)
        # draw health bar
        if self.health > 0:
            w = 24
            h = 1
            x = self.x-w//2
            y = self.y-self.animator.get_frame().get_height()
            if self.is_enemy: color = (192, 64, 64)
            else:             color = (64, 192, 64)
            pygame.draw.rect(screen, (16, 16, 16), (x-1, y-1-h, w+2, h*2+2))
            pygame.draw.rect(screen, color, (x, y-h, w*self.health/self.max_health, h))
            pygame.draw.rect(screen, (192, 192, 64), (x, y,   w*self.shield/self.max_shield, h))
    def take_damage(self, damage):
        self.shield -= damage
        if self.shield < 0:
            self.health += self.shield
            self.shield = 0
            if self.health <= 0:
                self.die()
        self.set_state("take_damage")
    def add_shield(self, shield):
        self.shield += shield
        if self.shield > self.max_shield:
            self.shield = self.max_shield
    def heal(self, health):
        self.health += health
        if self.health > self.max_health:
            self.health = self.max_health
    def die(self):
        self.dead = True
        self.set_state("dead")
    def attack(self):
        self.set_state("attack")
    def set_state(self, state):
        self.state = state
        self.state_changed = True
        self.state_timer = 0
    def update(self, dt, events, gm, objects):
        self.deck.update(dt, events, gm, objects)
        my_turn = gm.get_current_character(objects) is self
        # check keys
        key_select = False
        key_right = False
        key_left = False
        key_down = False
        key_up = False
        if not self.is_enemy:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if   event.key == pygame.K_SPACE: key_select = True
                    elif event.key == pygame.K_RIGHT: key_right  = True
                    elif event.key == pygame.K_LEFT:  key_left   = True
                    elif event.key == pygame.K_DOWN:  key_down   = True
                    elif event.key == pygame.K_UP:    key_up     = True
        # update timer
        self.state_timer += dt
        # check states
        ## IDLE ########################################
        if self.state == "idle":
            if self.state_changed:
                self.state_changed = False
                self.selected = False
                if len(self.deck.cards) >= 10:
                    self.selected = True
            if self.health <= 0:
                self.set_state("dead")
                return
            if self.is_enemy:
                if my_turn:
                    if self.state_timer > 1:
                        self.deck.selection = 0
                        for _ in range(len(self.deck.cards)):
                            if self.deck.can_be_used(gm.top_card):
                                card = self.deck.get_selected_card()
                                card.x = self.x-7
                                card.y = self.y-18
                                card.set_target(112, 47)
                                gm.played_by_enemy = True
                                self.deck.use(gm)
                                gm.played_cards.append(card)
                                self.set_state("select")
                                break
                            self.deck.right()
                        else:
                            self.deck.selection = len(self.deck.cards)
                            if self.deck.can_draw():
                                self.deck.draw_random_card()
                            self.attack()
            else: # is player
                if key_select:
                    if my_turn:
                        if self.deck.can_be_used(gm.top_card):
                            card = self.deck.get_selected_card()
                            card.set_target(112, 47)
                            gm.played_by_enemy = False
                            self.deck.use(gm)
                            gm.played_cards.append(card)
                            self.set_state("select")
                        elif self.deck.can_draw():
                            if not self.selected:
                                self.deck.draw_random_card()
                                self.selected = True
                            else:
                                self.attack()
                if key_right:
                    self.deck.right()
                if key_left:
                    self.deck.left()
        ## ATTACK ######################################
        elif self.state == "attack":
            if self.state_changed:
                self.state_changed = False
            # move
            dx = -1 if self.is_enemy else 1
            if self.state_timer < 0.25:
                self.x += dx*32*dt
            elif self.state_timer < 0.75:
                pass
            elif self.state_timer < 1:
                self.x -= dx*32*dt
            else:
                gm.next_turn()
                self.set_state("idle")
        ## SELECT ######################################
        elif self.state == "select":
            if self.state_changed:
                self.state_changed = False
                enemies = []
                heroes = []
                for object in objects:
                    if object.is_character and object.is_enemy:
                        enemies.append(object)
                    elif object.is_character and not object.is_enemy:
                        heroes.append(object)
                if self.is_enemy:
                    if gm.select_from_enemy:
                        gm.character_selection = randrange(len(enemies))
                    else:
                        gm.character_selection = randrange(len(heroes))
                else:
                    gm.character_selection = 0
            enemies = []
            heroes = []
            for object in objects:
                if object.is_character and object.is_enemy:
                    enemies.append(object)
                elif object.is_character and not object.is_enemy:
                    heroes.append(object)
            if self.is_enemy:
                if self.state_timer > 1:
                    if gm.select_from_enemy:
                        character = enemies[gm.character_selection]
                    else:
                        character = heroes[gm.character_selection]
                    level = gm.playing_card_level
                    if gm.playing_card_type == Card.ATTACK:
                        character.take_damage(level*2)
                    elif gm.playing_card_type == Card.SHIELD:
                        character.add_shield(level+1)
                    elif gm.playing_card_type == Card.HEALTH:
                        character.heal(level+3)
                    self.attack()
            else: # is player
                if key_down or key_up:
                    dir = key_down-key_up
                    if gm.select_from_enemy:
                        gm.character_selection = (gm.character_selection+dir)%len(enemies)
                    else:
                        gm.character_selection = (gm.character_selection+dir)%len(heroes)
                if key_select:# or (gm.select_from_enemy and len(enemies) == 1) or (not gm.select_from_enemy and len(heroes) == 1):
                    if gm.select_from_enemy:
                        character = enemies[gm.character_selection]
                    else:
                        character = heroes[gm.character_selection]
                    level = gm.playing_card_level
                    if gm.playing_card_type == Card.ATTACK:
                        character.take_damage(level*2+2)
                    elif gm.playing_card_type == Card.SHIELD:
                        character.add_shield(level+2)
                    elif gm.playing_card_type == Card.HEALTH:
                        character.heal(level+4)
                    self.attack()
        ## DEAD ########################################
        elif self.state == "dead":
            if self.state_changed:
                self.state_changed = False
            self.animator.alpha = max(0, self.animator.alpha-dt*128)
            if self.state_timer > 3:
                gm.character_count -= 1
                gm.turn = gm.turn%gm.character_count
                self.delete()
        ## TAKE DAMAGE #################################
        elif self.state == "take_damage":
            if self.state_changed:
                self.state_changed = False
                self.animator.fill = True
            if self.state_timer > 0.5:
                self.animator.fill = False
                self.set_state("idle")
        ################################################
