from helper import can_interact_default, overlap
from objects import InteractiveObject

class Wall(InteractiveObject):
    def __init__(self, x, y):
        super().__init__(num_stages=0)
        self.position = [x, y]
        self.width, self.height = 0.5, 0.5

        
    def __str__(self):
        return "a wall"
        
    def can_interact(self, player):
        return False
           
    def collision(self, obj, x_position, y_position):
        if overlap(self.position[0], self.position[1], self.width, self.height,
                       x_position, y_position, obj.width, obj.height):
            print("Oof!")
            return True
        else:
            return False
    
    def interact(self, game, player):
        pass

    def can_interact(self, player):
        pass
        
    def render(self, screen, camera):
        pass # set positions of this object align with the map
