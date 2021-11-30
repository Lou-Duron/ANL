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
clock = pygame.time.Clock()
game = Game(window_width, window_height)
game_over = False
##################################################################################################
test = game.add_organism(Organism(1,2, COLOR.BLUE, DIRECTIONS.EAST, 1, 10))

for i in range(20):
    game.add_random_organism()


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
# LOOP
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
    game.add_random_organism()
    game.move_all_randomly()
    #game.add_random_food()
    #draw_vision()
    draw_organisms()
    #draw_food()

    pygame.display.update()
    #clock.tick(clock_ticks)
 ##################################################################################################
pygame.display.update() 
pygame.quit()
quit()