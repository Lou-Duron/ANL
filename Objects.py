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
        self.life = 1000
        self.closest_food = None
        self.blocks: list[Block] = []
        self.head = Head(x, y, COLOR.BLACK)
        self.blocks.append(self.head)
        for i in range(1, 4):
            if self.direction == DIRECTIONS.NORTH:
                self.blocks.append(Body(x, y + i, color))
            elif self.direction == DIRECTIONS.EAST: 
                self.blocks.append(Body(x - i, y, color))
            elif self.direction == DIRECTIONS.SOUTH: 
                self.blocks.append(Body(x, y - i, color))
            elif self.direction == DIRECTIONS.WEST: 
                self.blocks.append(Body(x + i, y, color))
        self.center = self.blocks[1] # Get center

    def mutate(self):
        
        pass

    def eat(self, grid, food):
        for i in range(-1,2):
            for j in range(-1,2):
                x, y = self.head.pos.x + i , self.head.pos.y + j
                if Position(x,y).is_in_grid(grid):
                    if type(grid[x][y].block) is Food:
                        self.food += 1                    
                        food.remove(grid[x][y].block)
                        grid[x][y].block = None
                        self.life += 20 # Expanding life for 20 time units
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
        self.pos = self.head.pos

    def rotate(self, clock_wise, grid):
        # get center
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


    def rotate_towards_direction(self, current_dir, aim_dir, grid):
        if abs(current_dir - aim_dir) % 2 != 0:
            if current_dir - aim_dir == -1 or current_dir - aim_dir == 3 :
                self.rotate(True, grid)
            else:
                self.rotate(False, grid)
        else:
            self.rotate(True, grid)

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

    def update_closest_food(self, grid):
        if self.closest_food is not None:
            min_dist = self.head.pos.distance_to(self.closest_food.pos)
            if type(grid[self.closest_food.pos.x][self.closest_food.pos.y].block) is not Food:
                self.closest_food = None
                min_dist = 10000
        else:
            min_dist = 10000
        for s in self.get_vision(grid):
            if type(s.block) is Food:
                dist = self.head.pos.distance_to(s.pos)
                if dist < min_dist:
                    self.closest_food = s.block
                    min_dist = dist
        
    
    def go_towards_food(self, grid):
        self.update_closest_food(grid)
        if self.closest_food is not None:
            dir_to_food = self.head.pos.direction_to(self.closest_food.pos)
            if self.direction != dir_to_food:
                self.rotate_towards_direction(self.direction, dir_to_food, grid)
            else:
                self.move_straight(self.speed, grid)
        else:
            self.random_move(grid)


    def get_vision(self, grid):
        squares = []
        if self.direction == DIRECTIONS.NORTH :
            for x in range(self.head.pos.x - self.vision, self.head.pos.x + self.vision + 1):
                for y in range(self.head.pos.y - self.vision , self.head.pos.y):
                    square_pos = Position(x,y)
                    if square_pos.distance_to(self.head.pos) <= self.vision:
                        if square_pos.is_in_grid(grid):  
                            squares.append(grid[x][y])
        elif self.direction == DIRECTIONS.EAST: 
            for x in range(self.head.pos.x + 1, self.head.pos.x + self.vision + 1):
                for y in range(self.head.pos.y - self.vision, self.head.pos.y + self.vision + 1):
                    square_pos = Position(x,y)
                    if square_pos.distance_to(self.head.pos) <= self.vision:
                        if square_pos.is_in_grid(grid):  
                            squares.append(grid[x][y])
        elif self.direction == DIRECTIONS.SOUTH: 
            for x in range(self.head.pos.x - self.vision, self.head.pos.x + self.vision + 1):
                for y in range(self.head.pos.y + 1 , self.head.pos.y + self.vision + 2):
                    square_pos = Position(x,y)
                    if square_pos.distance_to(self.head.pos) <= self.vision:
                        if square_pos.is_in_grid(grid):  
                            squares.append(grid[x][y])
        elif self.direction == DIRECTIONS.WEST: 
            for x in range(self.head.pos.x - self.vision, self.head.pos.x):
                for y in range(self.head.pos.y - self.vision, self.head.pos.y + self.vision):
                    square_pos = Position(x,y)
                    if square_pos.distance_to(self.head.pos) <= self.vision:
                        if square_pos.is_in_grid(grid):  
                            squares.append(grid[x][y])
        return squares

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
        elif direction == 5:
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
        closest_dir = 5
        for direction in check_dirs:
            newpos = self.translate(direction, 1)
            dist = target_pos.distance_to(newpos)
            if dist < closest_dist:
                closest_dir = direction
                closest_dist = dist
        return closest_dir
    
    def is_in_grid(self, grid):
        return self.x >= 0 and self.x < len(grid) and  self.y >= 0  and self.y < len(grid[0])