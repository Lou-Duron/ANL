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

    def checkOrganismPriority(self):
        for organism in self.population: # For each organism
            organism.life -= 1 # Lose 1 life point
            if organism.life == 0: # If life == 0
                self.removeOrganism(organism) # Die
            elif organism.food == len(organism.blocks): # If enought food
                organism.reproduce(self) # Try to reproduce
            elif not organism.tryToEat(self): # Try to eat
                #organism.goTowardsFood(self.grid)
                organism.randomMove(self) # Else move randomly

######################################################################################################

    def isInGrid(self, x, y): # Check if osition in grid
        return x >= 0 and x < self.width and  y >= 0  and y < self.height

    def orgNewPosAreValid(self, org, positions): # Check organisme new position
        for pos in positions:
            if not self.isInGrid(pos[0], pos[1]):
                return False
            if type(self.grid[pos[0]][pos[1]].block) is Block:
                if self.grid[pos[0]][pos[1]].block not in org.blocks:
                    return False
        return True

    def getSquare(self, position): 
        return self.grid[position.x][position.y]

    def removeOrganism(self, organism: Organism):
        for block in organism.blocks:
            f = Food(block.pos.x, block.pos.y, COLOR.FOOD) # Tranform to food
            self.grid[block.pos.x][block.pos.y].block = f
            self.food.append(f)
        self.population.remove(organism)
    
    def addOrganism(self, organism):
        self.population.append(organism)
        for block in organism.blocks:
            self.getSquare(block.pos).block = block
    
    def addRandomOrganism(self, number):
        for i in range(number):
            x = random.randint(3, len(self.grid) - 4)
            y = random.randint(3, len(self.grid[0]) - 4)
            dir = random.randint(0,3)
            col = random.choice(list(COLOR.BASIC_ORG))
            og = Organism(col,dir,1, 5)
            og.initBasicOrg(x,y)
            self.addOrganism(og)
    
    def addFood(self, x, y):
        if self.grid[x][y].block is None :
            f = Food(x, y, COLOR.FOOD)
            self.food.append(f)
            self.grid[x][y].block = f

    def addRandomFood(self, number):
        for i in range(number):
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid[0]) - 1)
            self.addFood(x,y)
    

