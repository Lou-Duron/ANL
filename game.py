import random
from constants import Constants
from Objects import *

COLOR = Constants.COLOR
DIRECTIONS = Constants.DIRECTIONS

class Square:
    def __init__(self,x,y):
      self.block = None
      self.x = x
      self.y = y

class Game:
    def __init__(self, width, height):
        self.grid = []
        self.population = []
        self.food = []
        for i in range(width):
            array = []
            for j in range(height):
                array.append(Square(i,j))
            self.grid.append(array)

    def get_block(self, position):
        return self.grid[position.x][position.y].block
    
    def add_organism(self, organism):
        self.population.append(organism)
        for b in organism.blocks:
            self.get_square(b.pos).block = b
    
    def add_random_organism(self):
        x = random.randint(3, len(self.grid) - 4)
        y = random.randint(3, len(self.grid) - 4)
        col = random.randint(0, 4)
        if col == 0:
            color = COLOR.BLUE
        elif col == 1:
            color = COLOR.YELLOW
        elif col == 2:
            color = COLOR.GREEN
        elif col == 3:
            color = COLOR.RED
        else:
            color = COLOR.ORANGE
        dir = random.randint(0, 3)
        self.add_organism(Organism(x,y,color,dir))

    def move_all_randomly(self):
        for organism in self.population:
            organism.random_move(self.grid)
    
    def add_food(self, x, y):
        if self.grid[x][y].block is None :
            f = Food(x, y)
            self.food.append(f)
            self.grid[x][y].block = f

    def add_random_food(self):
        x = random.randint(0, len(self.grid) - 1)
        y = random.randint(0, len(self.grid) - 1)
        self.add_food(x,y)
    

