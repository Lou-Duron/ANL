import random
from constants import Constants
from Objects import *
import mutations as mut

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
    #   change block.type
    #       eyes
    #       attack
    #       defense
    #       move (speed, direction)
    # Change color##
    # change speed
    # reproduction rate 
    # life
    # food consumption
    # life per food
    # speed
    # pas de cannibalisme
    # gros -> pas facilement butable

        
    def mutate(self, game):
        r = random.randint(0, 50) # chance to mutate
        if r == 0:
            print(f"mutating")
            r2 = random.randint(0, 4) # between x and y included
            
            if r2 <= 2:
                mut.add_block(self, game)
            elif r2 == 3:
                mut.remove_block(self, game)
            elif r2 == 4:
                mut.change_color(self)
            else:
                pass

    def reproduce(self, game): # -> return true is successful
        self.food = 0 
        for i in range(-10, 11, 10):
            for j in range(-10, 11, 10):
                x = self.blocks[0].pos.x + i
                y = self.blocks[0].pos.y + j
                if game.isInGrid(x,y) and type(game.grid[x][y]) is not Block:
                    new_copy = self.copyItself()
                    if new_copy.translate(i,j, game):
                        new_copy.mutate(game)
                        game.addOrganism(new_copy)
                        return True             
        return False

    def initBasicOrg(self, x, y): # Create a 4 block basic organism
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

    def copyItself(self): # return a copy of the organism
        new_org = Organism(self.color, self.direction, self.speed, self.vision)
        for block in self.blocks:
            new_org.blocks.append(Block(block.pos.x, block.pos.y, block.color, block.type))
        return new_org

    def moveStraight(self, step, game): # Return true if successful
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
        if game.orgNewPosAreValid(self, new_pos):    
            for i, block in enumerate(self.blocks):
                game.grid[block.pos.x][block.pos.y].block = None
                block.pos.x = new_pos[i][0]  
                block.pos.y = new_pos[i][1]
                if type(game.grid[block.pos.x][block.pos.y].block) is Food:
                    game.food.remove(game.grid[block.pos.x][block.pos.y].block)
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
        if game.orgNewPosAreValid(self, new_pos):    
            for i, block in enumerate(self.blocks):
                game.grid[block.pos.x][block.pos.y].block = None
                block.pos.x = new_pos[i][0]  
                block.pos.y = new_pos[i][1]
                if type(game.grid[block.pos.x][block.pos.y].block) is Food:
                    game.food.remove(game.grid[block.pos.x][block.pos.y].block)
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
        if game.orgNewPosAreValid(self, new_pos):    
            for i, block in enumerate(self.blocks):
                game.grid[block.pos.x][block.pos.y].block = None
                block.pos.x = new_pos[i][0]  
                block.pos.y = new_pos[i][1]
                if type(game.grid[block.pos.x][block.pos.y].block) is Food:
                    game.food.remove(game.grid[block.pos.x][block.pos.y].block)
                game.grid[block.pos.x][block.pos.y].block = block
            return True
        return False 
      
    def getAdjacentSquares(self, game):
        squares = []
        for block in self.blocks[1:]: 
            positions = [[1,0], [-1,0], [0,1], [0,-1]]
            for p in positions:
                    new_x = block.pos.x + p[0]
                    new_y = block.pos.y + p[1]
                    if game.isInGrid(new_x, new_y):
                        if type(game.grid[new_x][new_y].block) is not Block:
                            if game.grid[new_x][new_y].block not in squares:
                                squares.append(game.grid[new_x][new_y])
        return squares

    def tryToEat(self, game): # True if successful    
        for i in range(-1,2): # MUT ?
            for j in range(-1,2):
                x, y = self.blocks[0].pos.x + i , self.blocks[0].pos.y + j
                if game.isInGrid(x,y):
                    if type(game.grid[x][y].block) is Food:
                        self.food += 1                    
                        game.food.remove(game.grid[x][y].block)
                        game.grid[x][y].block = None
                        self.life += 20 # Expanding life for 20 time units # MUT ?
                        return True
        return False

    def randomMove(self, game):
        r = random.randint(0, 4) ## MUT
        if r == 0:
            r2 = random.randint(0,1)
            if r2 == 0:
                self.rotate(True, game)
            else:
                self.rotate(False, game)
        else:
            if not self.moveStraight(self.speed, game):
                if not self.rotate(True, game):
                    self.rotate(False, game)

######################################################################################################
    def rotateTowardsDirection(self, current_dir, aim_dir, grid):
        if abs(current_dir - aim_dir) % 2 != 0:
            if current_dir - aim_dir == -1 or current_dir - aim_dir == 3 :
                self.rotate(True, grid)
            else:
                self.rotate(False, grid)
        else:
            self.rotate(True, grid)



    def updateClosestFood(self, grid):
        if self.closest_food is not None:
            min_dist = self.blocks[0].pos.distance_to(self.closest_food.pos)
            if type(grid[self.closest_food.pos.x][self.closest_food.pos.y].block) is not Food:
                self.closest_food = None
                min_dist = 10000
        else:
            min_dist = 10000
        for s in self.getVision(grid):
            if type(s.block) is Food:
                dist = self.blocks[0].pos.distance_to(s.pos)
                if dist < min_dist:
                    self.closest_food = s.block
                    min_dist = dist
        
    
    def goTowardsFood(self, grid):
        self.updateClosestFood(grid)
        if self.closest_food is not None:
            dir_to_food = self.blocks[0].pos.direction_to(self.closest_food.pos)
            if self.direction != dir_to_food:
                self.rotateTowardsDirection(self.direction, dir_to_food, grid)
            else:
                self.moveStraight(self.speed, grid)
        else:
            self.randomMove(grid)
######################################################################################################
    def getVision(self, game): # Too slow...
        blocks = []
        for x in range(self.blocks[0].pos.x - self.vision, self.blocks[0].pos.x + self.vision + 1):
            for y in range(self.blocks[0].pos.y - self.vision , self.blocks[0].pos.y + self.vision + 1):
                if game.isInGrid(x,y):
                    i = 0
                    if game.grid[x][y].block is not None:
                        if game.grid[x][y].block not in self.blocks:
                            blocks.append(game.grid[x][y].block)
        return blocks
