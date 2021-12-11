import random
from constants import Constants
from Objects import *

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR
TYPE = Constants.TYPE

class Organism:
    food = 0
    life = 200
    def __init__(self, color, direction, speed, vision):
        self.color = color
        self.direction: int = direction
        self.speed = speed
        self.vision = vision
        self.blocks: list[Block] = []

    #IDEAS
    #ROTATION AROUND CENTER ?
    # Size :
    #   Add a block##
    #   Remove a block##
    #   chage block.type
    #       eyes
    #       attatck
    #       defense
    #       move (speed, direction)
    # Change color##
    # change speed
    # repdoduction rate 
    # life
    # foos consumption
    # life per food
    # speed
    # 

        
    def mutate(self, game):
        r = random.randint(0, 50) # chance to mutate
        if r == 0:
            print(f"mutating")
            r2 = random.randint(0, 4)
            if r2 < 3: # Add block
                adj_squares = self.get_adgacent_square(game)
                if len(adj_squares) > 0:
                    print(f"Size : {len(self.blocks)} -> {len(self.blocks) + 1}")
                    new_pos = random.choice(adj_squares).pos
                    new_block = Block(new_pos.x, new_pos.y, self.color, TYPE.BODY)
                    self.blocks.append(new_block)
                    game.grid[new_block.pos.x][new_block.pos.y].block = new_block
            elif r2 == 3:
                print(f"Size : {len(self.blocks)} -> {len(self.blocks) - 1}")
                for block in reversed(self.blocks):
                    if block.type == TYPE.BODY:
                        self.blocks.remove(block)
                        game.grid[block.pos.x][block.pos.y].block = None
                        break
            elif r2 == 4: # Chage color
                new_col = random.choice(list(COLOR.ORG))
                print(f"Color")
                self.color = new_col
                for block in self.blocks[1:]:
                    block.color = new_col
                pass
            elif r2 == 1:
                pass

        pass

    def reproduce(self, game):
        for x in range(self.blocks[0].pos.x - 10,self.blocks[0].pos.x + 10, 10):
            for y in range(self.blocks[0].pos.y - 10, self.blocks[0].pos.y + 10, 10):
                if game.is_in_grid(x,y) and type(game.grid[x][y]) is not Block:
                    new_copy = self.copy_itself()
                    if new_copy.translate(x,y, game):
                        new_copy.mutate(game)
                        game.add_organism(new_copy)
                        break
        self.food = 0      

    def init_basic_org(self, x, y): # Create a 4 block basic organism
        color = self.color
        self.blocks.append(Block(x, y, COLOR.BLACK, TYPE.HEAD))
        for i in range(1, 4):
            if self.direction == DIRECTIONS.NORTH:
                self.blocks.append(Block(x, y + i, color, TYPE.BODY))
            elif self.direction == DIRECTIONS.EAST: 
                self.blocks.append(Block(x - i, y, color, TYPE.BODY))
            elif self.direction == DIRECTIONS.SOUTH: 
                self.blocks.append(Block(x, y - i, color, TYPE.BODY))
            elif self.direction == DIRECTIONS.WEST: 
                self.blocks.append(Block(x + i, y, color, TYPE.BODY))

    def copy_itself(self): # return a copy of the organism
        new_org = Organism(self.color, self.direction, self.speed, self.vision)
        for block in self.blocks:
            new_org.blocks.append(Block(block.pos.x, block.pos.y, block.color, block.type))
        return new_org

    def move_straight(self, step, game): # Return true if successful
        new_pos = []
        for block in self.blocks:
            x, y = block.pos.x, block.pos.y 
            if self.direction == DIRECTIONS.NORTH:
                y -= step
            elif self.direction == DIRECTIONS.EAST: 
                x += step
            elif self.direction == DIRECTIONS.SOUTH: 
                y += step
            elif self.direction == DIRECTIONS.WEST: 
                x -= step
            new_pos.append([x,y])
        if game.org_new_pos_are_valid(self, new_pos):    
            for i, block in enumerate(self.blocks):
                game.grid[block.pos.x][block.pos.y].block = None
                block.pos.x = new_pos[i][0]  
                block.pos.y = new_pos[i][1]
                game.grid[block.pos.x][block.pos.y].block = block
            return True
        return False 

    def rotate(self, clock_wise, game): # Return true if successful
        cw = -1
        if clock_wise: cw = 1
        new_pos = []
        # Check if new position is valid
        for block in self.blocks:
            delta_x = block.pos.x - self.blocks[0].pos.x
            delta_y = block.pos.y - self.blocks[0].pos.y
            new_x = self.blocks[0].pos.x + (-cw * delta_y)
            new_y = self.blocks[0].pos.y + (cw * delta_x)
            new_pos.append([new_x,new_y])
        if game.org_new_pos_are_valid(self, new_pos):    
            for i, block in enumerate(self.blocks):
                game.grid[block.pos.x][block.pos.y].block = None
                block.pos.x = new_pos[i][0]  
                block.pos.y = new_pos[i][1]
                game.grid[block.pos.x][block.pos.y].block = block 
            self.direction = (self.direction + cw) % 4
            return True
        return False 
       
    def translate(self, x, y, game): # Return True if successful
        new_pos = []
        for block in self.blocks:
            new_x = block.pos.x + x
            new_y = block.pos.y + y
            new_pos.append([new_x,new_y])
        if game.org_new_pos_are_valid(self, new_pos):    
            for i, block in enumerate(self.blocks):
                game.grid[block.pos.x][block.pos.y].block = None
                block.pos.x = new_pos[i][0]  
                block.pos.y = new_pos[i][1]
                game.grid[block.pos.x][block.pos.y].block = block
            return True
        return False 
      
    def get_adgacent_square(self, game):
        s = []
        for block in self.blocks[1:]: 
            for x in range(-1, 1, 2):
                for y in range(-1, 1, 2):
                    new_x = block.pos.x + x
                    new_y = block.pos.x + y
                    if game.is_in_grid(new_x, new_y):
                        if type(game.grid[new_x][new_y].block) is not Block:
                            if game.grid[new_x][new_y].block not in s:
                                s.append(game.grid[new_x][new_y])
        return s
    #COLLISION
    
    #
    #moves : move_straight, rotate, copy
    # -> return list of new pos
    # if list of block OK in grid + other organisms:
    #   make the move (org, list of new pos) 

    def try_to_eat(self, game): # True if successful    
        for i in range(-1,2):
            for j in range(-1,2):
                x, y = self.blocks[0].pos.x + i , self.blocks[0].pos.y + j
                if game.is_in_grid(x,y):
                    if type(game.grid[x][y].block) is Food:
                        #print(f"Oorg pos : {self.blocks[0].pos.x, self.blocks[0].pos.y} found food")
                        self.food += 1                    
                        game.food.remove(game.grid[x][y].block)
                        game.grid[x][y].block = None
                        self.life += 20 # Expanding life for 20 time units # MUT ?
                        return True
        return False

   


    def random_move(self, game):
        r = random.randint(0, 4) ## MUT
        if r == 0:
            r2 = random.randint(0,1)
            if r2 == 0:
                self.rotate(True, game)
            else:
                self.rotate(False, game)
        else:
            if not self.move_straight(self.speed, game):
                if not self.rotate(True, game):
                    self.rotate(False, game)

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
            min_dist = self.blocks[0].pos.distance_to(self.closest_food.pos)
            if type(grid[self.closest_food.pos.x][self.closest_food.pos.y].block) is not Food:
                self.closest_food = None
                min_dist = 10000
        else:
            min_dist = 10000
        for s in self.get_vision(grid):
            if type(s.block) is Food:
                dist = self.blocks[0].pos.distance_to(s.pos)
                if dist < min_dist:
                    self.closest_food = s.block
                    min_dist = dist
        
    
    def go_towards_food(self, grid):
        self.update_closest_food(grid)
        if self.closest_food is not None:
            dir_to_food = self.blocks[0].pos.direction_to(self.closest_food.pos)
            if self.direction != dir_to_food:
                self.rotate_towards_direction(self.direction, dir_to_food, grid)
            else:
                self.move_straight(self.speed, grid)
        else:
            self.random_move(grid)
######################################################################################################
    def get_vision(self, game):
        blocks = []
        for x in range(self.blocks[0].pos.x - self.vision, self.blocks[0].pos.x + self.vision + 1):
            for y in range(self.blocks[0].pos.y - self.vision , self.blocks[0].pos.y + self.vision + 1):
                if game.is_in_grid(x,y):
                    i = 0
                    #if grid[x][y].block is not None and grid[x][y].block not in self.blocks:
                    #blocks.append(grid[x][y].block)
        return blocks
