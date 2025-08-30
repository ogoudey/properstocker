from helper import can_interact_default, overlap

class Wall:
    def __init__(self, x, y):
        self.position = [x, y]
        self.width, self.height = 0.5, 0.5
        
    def __str__(self):
        return "a wall"
           
    def collision(self, obj, x_position, y_position):
        if overlap(self.position[0], self.position[1], self.width, self.height,
                       x_position, y_position, obj.width, obj.height):
            print("Oof!")
            return True
        else:
            return False

    
    def render(self, a, b):
        pass # already rendered
        
    def render_interaction(self, a, b):
        pass # not interactive
