import random
from constants import Constants
from Objects import *
from typing import List

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR

class Square:
    def __init__(self,x,y):
      self.block = None
      self.x = x
      self.y = y

class Game:
    def __init__(self, width, height):
        self.population: List[Block] = []
        self.food: List[Food]= []
        self.grid: List[List[Square]] = []
        for i in range(width):
            array = []
            for j in range(height):
                array.append(Square(i,j))
            self.grid.append(array)

    def get_square(self, position):
        return self.grid[position.x][position.y]
    
    def add_organism(self, organism):
        self.population.append(organism)
        for b in organism.blocks:
            self.get_square(b.pos).block = b
    
    def add_random_organism(self):
        self.add_organism(Organism(1,2, COLOR.BLUE, DIRECTIONS.EAST, 1, 10))
        x = random.randint(3, len(self.grid) - 4)
        y = random.randint(3, len(self.grid) - 4)
        dir = random.randint(0,3)
        col = random.choice(list(COLOR.ORG))
        self.add_organism(Organism(x,y,col,dir,1, 10))

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
    

