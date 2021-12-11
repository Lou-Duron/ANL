import random
from constants import Constants
from Organisms import *
from Objects import *
from typing import List

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR
'''
New vision -> Meh
WALL -> artefacts
Better duplicate
food when died#
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

######################################################################################################

    def check_organism_priority(self):
        for organism in self.population:
            organism.life -= 1 # Lose 1 life point
            if organism.life == 0: # If life == 0
                self.remove_organism(organism) 
            elif organism.food == 4:
                organism.food = 0
                if organism.color == COLOR.ORANGE:
                    self.duplicate_organism(organism)
            elif not organism.eat(self): # Eat if you can
                #organism.go_towards_food(self.grid)
                organism.random_move(self) # Else move randomly

######################################################################################################

    def is_in_grid(self, x, y):
        return x >= 0 and x < self.width and  y >= 0  and y < self.height

    def get_square(self, position):
        return self.grid[position.x][position.y]

    def remove_organism(self, organism: Organism):
        for block in organism.blocks:
            f = Food(block.pos.x, block.pos.y, COLOR.FOOD) # Tranform to food
            self.grid[block.pos.x][block.pos.y].block = f
            self.food.append(f)
        self.population.remove(organism)

    def duplicate_organism(self, org: Organism):
        #try to duplicate else -> False
        max_size = max(self.width, self.height)
        for x in range(org.pos.x - max_size, org.pos.x - max_size, max_size):
            for y in range(org.pos.y - max_size, org.pos.y - max_size, max_size):
                print(x,y)
        #new_org = org.copy()
        #self.add_organism(Organism(x, y, org.color, org.direction, org.speed, org.vision))
    
    def add_organism(self, organism):
        self.population.append(organism)
        for block in organism.blocks:
            self.get_square(block.pos).block = block
    
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
    

