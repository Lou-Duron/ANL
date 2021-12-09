import pygame
from Objects import *
from game import Game
from constants import Constants

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR

# Variables
screen_width = 1350
screen_height  = 700
block_size = 1
window_width = screen_width
window_height = screen_height
window_pos = Position(0,0)
clock_ticks = 1    

# Setup
pygame.init()
pygame.display.set_caption('A new life')
screen = pygame.display.set_mode((screen_width, screen_height))
game = Game(window_width, window_height)
game_over = False
clock = pygame.time.Clock()
##################################################################################################

#game.add_random_organism(1)
#print(Position(100,100).direction_to(Position(105,99)))
#print(Position(101,101).direction_to(Position(105,99)))
#test = Organism(100,100, COLOR.RED, 0, 1, 10)

#game.add_organism(test)
#game.add_food(105, 99)
#game.add_food(110, 100)
#game.add_food(115, 100)
#game.add_random_food(1000)

##################################################################################################
def draw_window():
    for x in range(window_pos.x, window_pos.x + window_width):
        for y in range(window_pos.y, window_pos.y + window_height):
            if game.grid[x][y].block is not None:
                b: Block = game.grid[x][y].block 
                pygame.draw.rect(screen, b.color, [(b.pos.x - window_pos.x) * block_size, (b.pos.y - window_pos.y) * block_size, block_size, block_size])

def draw_food_range():
    for org in game.population:
        for i in range(-1,2):
                for j in range(-1,2):
                    x, y = org.head.pos.x + i , org.head.pos.y + j
                    if Position(x,y).is_in_grid(game.grid):
                        pygame.draw.rect(screen, COLOR.VISION, [(x - window_pos.x) * block_size, (y - window_pos.y) * block_size, block_size, block_size])
          
# IDEA : get organism and food in the current window for optimisation 
# For the moment, negative values are computed but not displayed

def draw_organisms():
    for organism in game.population:
        for block in organism.blocks:
            if block.pos.is_in_grid(game.grid):  
                pygame.draw.rect(screen, block.color, [(block.pos.x - window_pos.x) * block_size, (block.pos.y - window_pos.y) * block_size, block_size, block_size])

def draw_food():
    for f in game.food:
        pygame.draw.rect(screen, COLOR.FOOD, [(f.pos.x - window_pos.x) * block_size, (f.pos.y - window_pos.y) * block_size, block_size, block_size])

def draw_vision():
    for organism in game.population:
        vision = organism.get_vision(game.grid)
        for square in vision:
            pygame.draw.rect(screen, COLOR.VISION, [(square.x - window_pos.x) * block_size, (square.y - window_pos.y) * block_size, block_size, block_size])
##################################################################################################

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEWHEEL: # ZOOM on mouse wheel
            e_x, e_y = pygame.mouse.get_pos()
            if (block_size == 1  and event.y == 1) or block_size  > 1:
                e_block_x = int(e_x / block_size + window_pos.x)
                e_block_y = int(e_y / block_size + window_pos.y)
                block_size += event.y
                window_width = int(screen_width/block_size)
                window_height = int(screen_height/block_size)
                window_pos.x = min(max(int(e_block_x - (e_x / block_size) ), 0), screen_width - window_width - 1)
                window_pos.y = min(max(int(e_block_y - (e_y / block_size) ), 0), screen_height - window_height - 1)
    
##################################################################################################  
# LOOP
    game.add_random_organism(10)
    game.add_random_food(10)
    #print(test.head.pos.x, test.head.pos.y)
    game.check_organism_priority()
##################################################################################################  
    screen.fill(COLOR.BK)
    #draw_vision() 
    draw_organisms()
    draw_food()
    #draw_food_range()
    #draw_window()
     
##################################################################################################
    pygame.display.update()
    #clock.tick(clock_ticks)
pygame.display.update() 
pygame.quit()
quit()