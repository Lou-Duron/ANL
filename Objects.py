import random
from constants import Constants

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR



class Organism:
    
    def __init__(self, x, y, color, direction, speed, vision):
        self.pos = Position(x,y)
        self.color = color
        self.direction: int = direction
        self.speed = speed
        self.vision = vision
        self.food = 0
        self.life  = 100
        self.blocks: list[Block] = []
        self.blocks.append(Head(x, y, COLOR.BLACK))
        self.head = self.blocks[0]
        for i in range(1, 4):
            if self.direction == DIRECTIONS.NORTH:
                self.blocks.append(Body(x, y + i, color))
            elif self.direction == DIRECTIONS.EAST: 
                self.blocks.append(Body(x - i, y, color))
            elif self.direction == DIRECTIONS.SOUTH: 
                self.blocks.append(Body(x, y - i, color))
            elif self.direction == DIRECTIONS.WEST: 
                self.blocks.append(Body(x + i, y, color))
        self.center = self.blocks[1]
        
    def eat(self, grid, food):
        for x in range(-1,1):
            for y in range(-1,1):
                if type(grid[self.pos.x + x][self.pos.y + y].block) is Food:
                    self.food += 1
                    print(self.food)
                    #check reproduction
                    
                    food.remove(grid[self.pos.x + x][self.pos.y + y].block)
                    grid[self.pos.x + x][self.pos.y + y].block = None
                    return True
        return False

    def move_straight(self, step, grid):
        for block in self.blocks:
            if block.pos.is_in_grid(grid):
                grid[block.pos.x][block.pos.y].block = None
            if self.direction == DIRECTIONS.NORTH:
                block.pos.y -= step
            elif self.direction == DIRECTIONS.EAST: 
                block.pos.x += step
            elif self.direction == DIRECTIONS.SOUTH: 
                block.pos.y += step
            elif self.direction == DIRECTIONS.WEST: 
                block.pos.x -= step
        for block in self.blocks:
            if block.pos.is_in_grid(grid):
                grid[block.pos.x][block.pos.y].block = block

    def rotate(self, clock_wise, grid):
        #get center
        cw = -1
        if clock_wise: cw = 1
        self.direction = (self.direction + cw) % 4
        for block in self.blocks:
            if block.pos.is_in_grid(grid):
                grid[block.pos.x][block.pos.y].block = None
            delta_x = block.pos.x - self.center.pos.x
            delta_y = block.pos.y - self.center.pos.y
            block.pos.x = self.center.pos.x + (-cw * delta_y)
            block.pos.y = self.center.pos.y + (cw * delta_x)

    def random_move(self, grid):
        r = random.randint(0, 3)
        if r == 0:
            r2 = random.randint(0,1)
            if r2 == 0:
                self.rotate(True, grid)
            else:
                self.rotate(False, grid)
        else:
            self.move_straight(self.speed, grid)

    def get_vision(self, grid):
        block = []
        if self.direction == 0 :
            for x in range(self.head.pos.x - self.vision, self.head.pos.x + self.vision + 1):
                for y in range(self.head.pos.y - self.vision , self.head.pos.y):
                    if abs(self.head.pos.x - x) + abs(self.head.pos.y - y) <= self.vision:
                        if x > 0 and x < len(grid) - 1 and  y > 0  and y < len(grid) - 1:
                            block.append(grid[x][y])
        elif self.direction == 1: 
            for x in range(self.head.pos.x + 1, self.head.pos.x + self.vision + 1):
                for y in range(self.head.pos.y - self.vision, self.head.pos.y + self.vision + 1):
                    if abs(self.head.pos.x - x) + abs(self.head.pos.y - y) <= self.vision:
                        if x > 0 and x < len(grid) - 1 and  y > 0  and y < len(grid) - 1:
                            block.append(grid[x][y])
        elif self.direction == 2: 
            for x in range(self.head.pos.x - self.vision, self.head.pos.x + self.vision + 1):
                for y in range(self.head.pos.y + 1 , self.head.pos.y + self.vision + 2):
                    if abs(self.head.pos.x - x) + abs(self.head.pos.y - y) <= self.vision:
                        if x > 0 and x < len(grid) - 1 and  y > 0  and y < len(grid) - 1:
                            block.append(grid[x][y])
        elif self.direction == 3: 
            for x in range(self.head.pos.x - self.vision, self.head.pos.x):
                for y in range(self.head.pos.y - self.vision, self.head.pos.y + self.vision):
                    if abs(self.head.pos.x - x) + abs(self.head.pos.y - y) <= self.vision:
                        if x > 0 and x < len(grid) - 1 and  y > 0  and y < len(grid) - 1:
                            block.append(grid[x][y])
        return block

class Block:       
   
   def __init__(self, x, y, color):
      self.pos = Position(x,y)
      self.color = color



   
class Head(Block):
    def __init__(self, x, y, color):
        Block.__init__(self, x, y, color)

class Body(Block):
   def __init__(self, x, y, color):
        Block.__init__(self, x, y, color)

class Food(Block):
    def __init__(self, x, y, color):
        Block.__init__(self, x, y, color)
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, pos) -> int:
        return abs(pos.x - self.x) + abs(pos.y - self.y)

    def distance_to(self, pos):
        """
        Returns Manhattan (L1/grid) distance to pos
        """
        return self - pos

    def is_adjacent(self, pos):
        return (self - pos) <= 1

    def __eq__(self, pos) -> bool:
        return self.x == pos.x and self.y == pos.y

    def equals(self, pos):
        return self == pos

    def translate(self, direction, units) -> 'Position':
        if direction == DIRECTIONS.NORTH:
            return Position(self.x, self.y - units)
        elif direction == DIRECTIONS.EAST:
            return Position(self.x + units, self.y)
        elif direction == DIRECTIONS.SOUTH:
            return Position(self.x, self.y + units)
        elif direction == DIRECTIONS.WEST:
            return Position(self.x - units, self.y)
        elif direction == DIRECTIONS.CENTER:
            return Position(self.x, self.y)

    def direction_to(self, target_pos: 'Position') -> DIRECTIONS:
        """
        Return closest position to target_pos from this position
        """
        check_dirs = [
            DIRECTIONS.NORTH,
            DIRECTIONS.EAST,
            DIRECTIONS.SOUTH,
            DIRECTIONS.WEST,
        ]
        closest_dist = self.distance_to(target_pos)
        closest_dir = DIRECTIONS.CENTER
        for direction in check_dirs:
            newpos = self.translate(direction, 1)
            dist = target_pos.distance_to(newpos)
            if dist < closest_dist:
                closest_dir = direction
                closest_dist = dist
        return closest_dir
    
    def is_in_grid(self, grid):
        return self.x >= 0 and self.x < len(grid) and  self.y >= 0  and self.y < len(grid)