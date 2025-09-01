from enums.direction import Direction
from objects import InteractiveObject
from helper import obj_collision, can_interact_default, overlap
import pygame
import config
import random

class Boxes(InteractiveObject):
    def __init__(self, x_position, y_position, boxes):
        super().__init__(num_stages=1)
        self.position = [x_position, y_position]
        self.boxes = boxes
        self.stack_height_limit = 5

        self.width = 0.15
        self.height = 0.15

        self.images = []

        self.render_offset_x = -0.25
        self.render_offset_y = 0.0
        
        self.id = random.randint(1000, 9999)
        
        
        
        
    def __str__(self):
        return "a stack of boxes #" + str(self.id)

    def render(self, screen, camera):
        i = 0
        for box in self.boxes:
            box.position[1] = self.position[1] - i * 0.15
            box.render(screen, camera)
            i += 1
        if len(self.boxes) > 1:                          
            gap = 0.345
            for i in range(0, len(self.boxes)):
                image = pygame.transform.scale(pygame.image.load("images/box/box.png"),
                                                   (int(.5 * config.SCALE), int(.5 * config.SCALE)))
                screen.blit(image, ((self.position[0] + self.render_offset_x - camera.position[0])*config.SCALE,
                                 (self.position[1] + (gap * -i) + self.render_offset_y - camera.position[1])*config.SCALE))

    def can_interact(self, player):
        return can_interact_default(self, player, range=.5)

    def collision(self, obj, x_position, y_position):
        col = overlap(self.position[0], self.position[1], self.width, self.height,
                       x_position, y_position, obj.width, obj.height)
        return col

    def interact(self, game, player):
        if self.get_interaction_stage(player) == 0:
            # Player is not holding a basket
            if player.carried_box is None and player.curr_basket is None:
                if len(self.boxes) > 2:
                    if len(self.boxes) < self.stack_height_limit:
                        if player.holding_food is None:
                            box = self.boxes.pop()
                            player.carried_box = box
                            box.being_held = True
                            box.in_stack = False
                            box.stack = None
                            self.set_interaction_message(player, "You picked up a box of " + str(box.food_contents["amount"]) + " " + box.food_contents["food"])
                    else:
                        self.set_interaction_message(player, "This stack is full!")                       
                else:
                    box = self.boxes.pop()
                    player.carried_box = box
                    box.being_held = True
                    box.in_stack = False
                    box.stack = None
                    self.set_interaction_message(player, "You picked up a box of " + str(box.food_contents["amount"]) + " " + box.food_contents["food"])
                    box = self.boxes.pop() # the last box
                    box.in_stack = False
                    box.stack = None
                    self.width = 0
                    self.position = [0, 0]
                    #game.objects.remove(self)

                    
            # Player is holding a basket; return it
            else:
                if len(self.boxes) < self.stack_height_limit:
                    print("Stack height:", len(self.boxes))
                    self.set_interaction_message(player, "You put back the box of " + str(player.carried_box.food_contents["amount"]) + " " + player.carried_box.food_contents["food"])
                    self.boxes.append(player.carried_box)
                    player.carried_box.being_held = False
                    player.carried_box.in_stack = True
                    player.carried_box = None                    
                    
                else:
                    self.set_interaction_message(player, "This stack is full!")
            
            
