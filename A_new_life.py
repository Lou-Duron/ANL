import pygame
import time
from Objects import *
from game import Game
from constants import Constants

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR

# Variables
screen_width = 700
screen_height  = 700
block_size = 1
window_width = screen_width
window_height = screen_height
window_pos = Position(0,0)
clock_ticks = 5

# Setup
pygame.init()
pygame.display.set_caption('A new life')
screen = pygame.display.set_mode((screen_width, screen_height))
game = Game(window_width, window_height)
game_over = False
clock = pygame.time.Clock()
##################################################################################################
for i in range(20):
    game.add_random_organism()

##################################################################################################
def draw_window():
    for x in range(window_pos.x, window_pos.x + window_width):
        for y in range(window_pos.y, window_pos.y + window_height):
            if game.grid[x][y].block is not None:
                b = game.grid[x][y].block 
                pygame.draw.rect(screen, b.color, [(b.pos.x - window_pos.x) * block_size, (b.pos.y - window_pos.y) * block_size, block_size, block_size])


def draw_organisms():
    for organism in game.population:
        for block in organism.blocks:
            if block.pos.is_in_grid(game.grid):  
                pygame.draw.rect(screen, block.color, [(block.pos.x - window_pos.x) * block_size, (block.pos.y - window_pos.y) * block_size, block_size, block_size])

def draw_food():
    for key in game.food.keys():
        f = game.food[key]
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
        # ZOOM on wheel
        elif event.type == pygame.MOUSEWHEEL: 
            e_x, e_y = pygame.mouse.get_pos()
            if (block_size == 1  and event.y == 1) or block_size  > 1:
                e_block_x = int(e_x / block_size + window_pos.x)
                e_block_y = int(e_y / block_size + window_pos.y)
                block_size += event.y
                window_width = int(screen_width/block_size)
                window_height = int(screen_height/block_size)
                window_pos.x = min(max(int(e_block_x - (e_x / block_size) ), 0), screen_width - window_width - 1)
                window_pos.y = min(max(int(e_block_y - (e_y / block_size) ), 0), screen_height - window_height - 1)
    screen.fill(COLOR.BK)
##################################################################################################  
# LOOP
    game.add_random_organism()
    #game.move_all_randomly()
    game.add_random_food(5)
    game.check_organisme_priority()
##################################################################################################  
    draw_organisms()
    draw_food()
    #draw_window()
    #draw_vision()

##################################################################################################

    pygame.display.update()
    #clock.tick(clock_ticks)
pygame.display.update() 
pygame.quit()
quit()