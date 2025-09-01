from objects import CartLike
import config
from helper import can_interact_default, overlap
from enums.direction import Direction
import pygame
from boxes import Boxes
from random import randint, choice
class Box(CartLike):


    def class_string(self):
        return "Box"

    def __str__(self):
        return "box"+str(self.id)+" of "+str(self.food_contents["amount"]) + " " + self.food_contents["food"]
        
    def __init__(self, x_position, y_position, direction=Direction.NORTH):
        super(Box, self).__init__(x_position, y_position, owner=None, capacity=999)
        self.width = 0
        self.height = 0
        self.set_direction(direction)
        self.render_offset_x = -0.25
        self.render_offset_y = 0.05
        self.being_held = False
        self.in_stack = False
        self.stack = None
        self.food_contents = {
                                "food": choice(["steak", "chicken", "ham"]),
                                "amount": randint(6, 12)
                             }
        self.id = randint(1000,9999)

    def set_direction(self, direction):
        self.direction = direction
        if direction == Direction.NORTH or direction == Direction.EAST:
            self.width = 0.15
            self.height = 0.15
        else:
            self.width = 0.15
            self.height = 0.15
        
    def can_interact(self, player):
        return player.carried_box != self and can_interact_default(self, player) and not self.in_stack

    def render(self, screen, camera):
        image = None
        if self.in_stack:
            # don't render - the stack does that.
            return
        image = pygame.transform.scale(pygame.image.load("images/box/box.png"),
                                               (int(.5 * config.SCALE), int(.5 * config.SCALE)))

        rect = pygame.Rect(
            (self.position[0] + self.render_offset_x) * config.SCALE - (camera.position[0] * config.SCALE),
            (self.position[1] + self.render_offset_y) * config.SCALE - (camera.position[1] * config.SCALE),
            config.SCALE, config.SCALE)
        screen.blit(image, rect)
        
    def update_position(self, x_position, y_position):
        if self.direction == Direction.NORTH:
            self.position[0] = x_position+0.05
            self.position[1] = y_position-0.4
        elif self.direction == Direction.SOUTH:
            self.position[0] = x_position+0.2
            self.position[1] = y_position+0.6
        elif self.direction == Direction.EAST:
            self.position[0] = x_position+0.65
            self.position[1] = y_position
        elif self.direction == Direction.WEST:
            self.position[0] = x_position-0.2
            self.position[1] = y_position+0.2
            
    def collision(self, obj, x_position, y_position):
        if self.in_stack:
            return 0
        if not self.being_held:
            return overlap(self.position[0], self.position[1], self.width, self.height,
                        x_position, y_position, obj.width, obj.height)
        else:
            return 0
            
    def interact(self, game, player):
        self.last_held = player
        if player.holding_food is not None:
            self.set_interaction_message(player, "You are holding food.")
        elif player.carried_box is not None:
            new_stack = Boxes(self.position[0], self.position[1], [self, player.carried_box])
            self.set_interaction_message(player, "You created a stack of boxes.")
            player.carried_box.being_held = False
            player.carried_box.in_stack = True
            self.stack = new_stack
            player.carried_box = None
            game.objects.append(new_stack)
            
            
        else:
            if self.in_stack:
                # let the stack deal with this logic
                pass
            else:
                player.carried_box = self
                self.being_held = True
                self.in_stack = False
                self.set_interaction_message(player, "You picked up a box of" + str(self.food_contents["amount"]) + " " + self.food_contents["food"])
                
    def can_toggle(self, player):
        print("Player direction:", player.direction)
        return can_interact_default(self, player)
        
        
# Add Box object.

# add render()

# add update_position()

# add interact() (-like)

#( initialize one )


## Add BoxStack object

# Add box -> boxstack -> box changing

# initialize box stacks


## Add Box "food item" feature

# Divide shelf interaction into two parts - check whether box is held (then 'restock' interaction); check whether no box is held (normal interaction)
