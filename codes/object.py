

class Object:
    def __init__(self, x, y, animator, is_character=False):
        self.is_character = is_character
        self.x = x
        self.y = y
        self.animator = animator
        self.objects_to_spawn = []
        self.will_be_deleted = False
    def delete(self):
        self.will_be_deleted = True
    def spawn(self, object):
        self.objects_to_spawn.append(object)
    def draw(self, screen):
        self.animator.draw(screen, self.x, self.y)
    def update(self, dt, events, gm, objects):
        pass
