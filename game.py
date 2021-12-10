import random
from constants import Constants
from Objects import *
from typing import List

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR
'''
New vision
organism can step on food
Better duplicate
food when died
copy org
colision
'''
class Square:
    def __init__(self,x,y):
      self.block = None
      self.pos = Position(x,y)
      self.x = x
      self.y = y

class Game:
    def __init__(self, width, height):
        self.population: List[Organism] = []
        self.food = []
        self.grid: List[List[Square]] = []
        self.width = width
        self.height = height
        for i in range(width):
            array = []
            for j in range(height):
                array.append(Square(i,j))
            self.grid.append(array)

    def is_in_grid(self, x, y):
        return x >= 0 and x < self.width and  y >= 0  and y < self.height

    def check_organism_priority(self):
        for organism in self.population:
            organism.life -= 1 # Lose 1 life point
            if organism.life == 0: # If life == 0
                self.remove_organism(organism) 
            elif organism.food == 4:
                organism.food = 0
                if organism.color == COLOR.RED:
                    self.duplicate_organism(organism)
            elif not organism.eat(self): # Eat if you can
                #organism.go_towards_food(self.grid)
                organism.random_move(self) # Else move randomly

    def get_square(self, position):
        return self.grid[position.x][position.y]

    def remove_organism(self, organism: Organism):
        for block in organism.blocks:
            if block.pos.is_in_grid(self.grid):
                self.grid[block.pos.x][block.pos.y].block = None
        self.population.remove(organism)

    def duplicate_organism(self, org: Organism):
        x = random.randint(3, len(self.grid) - 4) # Not random
        y = random.randint(3, len(self.grid[0]) - 4)
        self.add_organism(Organism(x, y, org.color, org.direction, org.speed, org.vision))
    
    def add_organism(self, organism):
        self.population.append(organism)
        for b in organism.blocks:
            self.get_square(b.pos).block = b
    
    def add_random_organism(self, number):
        for i in range(number):
            x = random.randint(3, len(self.grid) - 4)
            y = random.randint(3, len(self.grid[0]) - 4)
            dir = random.randint(0,3)
            col = random.choice(list(COLOR.ORG))
            self.add_organism(Organism(x,y,col,dir,1, 10))
    
    def add_food(self, x, y):
        if self.grid[x][y].block is None :
            f = Food(x, y, COLOR.FOOD)
            self.food.append(f)
            self.grid[x][y].block = f

    def add_random_food(self, number):
        for i in range(number):
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid[0]) - 1)
            self.add_food(x,y)
    

