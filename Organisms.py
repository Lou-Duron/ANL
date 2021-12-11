import random
from constants import Constants
from Objects import *

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR

class Organism:
    food = 0
    life = 1000
    def __init__(self, x, y, color, direction, speed, vision):
        self.pos = Position(x,y)
        self.color = color
        self.direction: int = direction
        self.speed = speed
        self.vision = vision
        self.blocks: list[Block] = []

    def init_basic_org(self):
        x, y = self.pos.x, self.pos.y
        color = self.color
        self.blocks.append(Block(x, y, COLOR.BLACK))
        for i in range(1, 4):
            if self.direction == DIRECTIONS.NORTH:
                self.blocks.append(Block(x, y + i, color))
            elif self.direction == DIRECTIONS.EAST: 
                self.blocks.append(Block(x - i, y, color))
            elif self.direction == DIRECTIONS.SOUTH: 
                self.blocks.append(Block(x, y - i, color))
            elif self.direction == DIRECTIONS.WEST: 
                self.blocks.append(Block(x + i, y, color))

    def copy_itself(self): # return a copy of the organism
        new_org = Organism(self.pos.x, self.pos.y, self.color, self.direction, self.speed, self.vision)
        for block in self.blocks:
            new_org.blocks.append(Block(block.pos.x, block.pos.y, self.color))
        return new_org

    def try_to_translate(self, step, direction):
        pass

    def mutate(self):
        # ROTATION AROUND CENTER ?
        pass

    

    def eat(self, game): # True if successful    
        for i in range(-1,2):
            for j in range(-1,2):
                x, y = self.pos.x + i , self.pos.y + j
                if game.is_in_grid(x,y):
                    if type(game.grid[x][y].block) is Food:
                        self.food += 1                    
                        game.food.remove(game.grid[x][y].block)
                        game.grid[x][y].block = None
                        self.life += 20 # Expanding life for 20 time units # MUT ?
                        return True
        return False

    def move_straight(self, step, game): # True if successful
        # Try to move else -> False(Always head first)
        x, y = self.pos.x, self.pos.y 
        if self.direction == DIRECTIONS.NORTH:
            y = self.pos.y - step
        elif self.direction == DIRECTIONS.EAST: 
            x = self.pos.x + step
        elif self.direction == DIRECTIONS.SOUTH: 
            y = self.pos.y + step
        elif self.direction == DIRECTIONS.WEST: 
            x = self.pos.x - step
        # Move - True
        if game.is_in_grid(x,y):
            for block in self.blocks:
                if self.direction == DIRECTIONS.NORTH:
                    block.pos.y -= step
                elif self.direction == DIRECTIONS.EAST: 
                    block.pos.x += step
                elif self.direction == DIRECTIONS.SOUTH: 
                    block.pos.y += step
                elif self.direction == DIRECTIONS.WEST: 
                    block.pos.x -= step
            for block in self.blocks:
                game.grid[block.pos.x][block.pos.y].block = block
            self.pos = self.blocks[0].pos
            return True
        else:
            return False

    def rotate(self, clock_wise, game) -> bool:
        cw = -1
        if clock_wise: cw = 1
        blocks = []
        new_pos = []
        # Try to rotate else -> False
        for block in self.blocks:
            delta_x = block.pos.x - self.pos.x
            delta_y = block.pos.y - self.pos.y
            new_x = self.pos.x + (-cw * delta_y)
            new_y = self.pos.y + (cw * delta_x)
            if game.is_in_grid(new_x, new_y):
                blocks.append(block)
                new_pos.append([new_x,new_y])
            else :
                return False
        # Rotate -> true
        for i, b in enumerate(blocks):
            b.pos.x = new_pos[i][0] 
            b.pos.y = new_pos[i][1]
        self.direction = (self.direction + cw) % 4
        return True

    def random_move(self, game):
        r = random.randint(0, 4)
        if r == 0:
            r2 = random.randint(0,1)
            if r2 == 0:
                self.rotate(True, game)
            else:
                self.rotate(False, game)
        else:
            self.move_straight(self.speed, game)

######################################################################################################
    def rotate_towards_direction(self, current_dir, aim_dir, grid):
        if abs(current_dir - aim_dir) % 2 != 0:
            if current_dir - aim_dir == -1 or current_dir - aim_dir == 3 :
                self.rotate(True, grid)
            else:
                self.rotate(False, grid)
        else:
            self.rotate(True, grid)



    def update_closest_food(self, grid):
        if self.closest_food is not None:
            min_dist = self.pos.distance_to(self.closest_food.pos)
            if type(grid[self.closest_food.pos.x][self.closest_food.pos.y].block) is not Food:
                self.closest_food = None
                min_dist = 10000
        else:
            min_dist = 10000
        for s in self.get_vision(grid):
            if type(s.block) is Food:
                dist = self.pos.distance_to(s.pos)
                if dist < min_dist:
                    self.closest_food = s.block
                    min_dist = dist
        
    
    def go_towards_food(self, grid):
        self.update_closest_food(grid)
        if self.closest_food is not None:
            dir_to_food = self.pos.direction_to(self.closest_food.pos)
            if self.direction != dir_to_food:
                self.rotate_towards_direction(self.direction, dir_to_food, grid)
            else:
                self.move_straight(self.speed, grid)
        else:
            self.random_move(grid)
######################################################################################################
    def get_vision(self, game):
        blocks = []
        for x in range(self.pos.x - self.vision, self.pos.x + self.vision + 1):
            for y in range(self.pos.y - self.vision , self.pos.y + self.vision + 1):
                if game.is_in_grid(x,y):
                    i = 0
                    #if grid[x][y].block is not None and grid[x][y].block not in self.blocks:
                    #blocks.append(grid[x][y].block)
        return blocks
