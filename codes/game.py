from character import Character
from images import *
from random import randrange
from background import Background
from game_manager import GameManager

class Game:
    def __init__(self):
        self.objects = [
            Character(0, 0, 48, 120, 30, 20, False),
            Character(1, randrange(2)+1, 184, 128, 10, 4, True),
            Character(2, randrange(2)+1, 152, 112, 10, 4, True),
        ]
        self.background = Background()
        self.game_manager = GameManager(len(self.objects))
    def draw(self, screen):
        self.background.draw(screen)
        for object in sorted([object for object in self.objects if object.is_character], key=(lambda c: c.y))+[object for object in self.objects if not object.is_character]:
            object.draw(screen)
        self.objects[0].deck.draw(screen)
        self.game_manager.draw(screen)
    def update(self, dt, events):
        self.game_manager.update(dt, events, self.objects)
        if self.game_manager.new_level:
            self.objects[0].heal(15)
            self.game_manager.level += 1
            level = self.game_manager.level
            if randrange(2):
                self.objects.append(Character(1, randrange(2)+1, 184, 128, 8+level*3, 4+level*2, True))
                self.objects.append(Character(2, randrange(2)+1, 152, 112, 8+level*3, 4+level*2, True))
            else:
                self.objects.append(Character(1, randrange(2)+1, 184, 120, 8+level*3, 4+level*2, True))
        self.background.update(dt)
        if self.game_manager.state == "combat":
            objects_to_spawn = []
            objects_to_delete = []
            for object in self.objects:
                object.update(dt, events, self.game_manager, self.objects)
                objects_to_spawn.extend(object.objects_to_spawn)
                if object.will_be_deleted:
                    objects_to_delete.append(object)
            for object in objects_to_delete:
                self.objects.remove(object)
            self.objects.extend(objects_to_spawn)
