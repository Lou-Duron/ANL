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
        self.key = 0
        self.population: List[Organism] = []
        self.food = {}
        self.grid: List[List[Square]] = []
        for i in range(width):
            array = []
            for j in range(height):
                array.append(Square(i,j))
            self.grid.append(array)

    def check_organisme_priority(self):
        for organism in self.population:
            if organism.color != COLOR.BLUE:
                organism.life -= 1
            if organism.life == 0:
                for b in organism.blocks:
                    if b.pos.is_in_grid(self.grid):
                        self.grid[b.pos.x][b.pos.y].block = None
                self.population.remove(organism)
            elif organism.food == 4:
                organism.food = 0
                organism.reproduce(self.grid)
            elif not organism.eat(self.grid, self.food): # Eat if you can
                organism.random_move(self.grid) # Else move randomly



    def get_square(self, position):
        return self.grid[position.x][position.y]
    
    def add_organism(self, organism):
        self.population.append(organism)
        for b in organism.blocks:
            self.get_square(b.pos).block = b
    
    def add_random_organism(self):
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
            f = Food(x, y, COLOR.FOOD, self.key)
            self.food[self.key] = f
            self.key += 1
            self.grid[x][y].block = f

    def add_random_food(self, rate):
        for i in range(rate):
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid) - 1)
            self.add_food(x,y)
    

