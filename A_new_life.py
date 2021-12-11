import pygame
pygame.init()
from Organisms import *
from game import Game
from constants import Constants
from UI import Slider

DIRECTIONS = Constants.DIRECTIONS
COLOR = Constants.COLOR
FONT = Constants.FONT

# Variables
screen_width = 750
screen_height  = 700
block_size = 3
fps = 60
pause = False
window_width = int(screen_width / block_size)
window_height = int(screen_height / block_size)
window_pos = Position(0,0)
frame_count = 0
# Setup
pygame.display.set_caption('A new life')
screen = pygame.display.set_mode((screen_width, screen_height))
game = Game(window_width, window_height)
game_over = False
clock = pygame.time.Clock()

#UI
#Name, value, max, min, pos.x
speed = Slider("FPS", fps, 61, 5, 345)
slides = [speed]

def draw_window(): # unused
    for x in range(window_pos.x, window_pos.x + window_width):
        for y in range(window_pos.y, window_pos.y + window_height):
            if game.grid[x][y].block is not None:
                b: Block = game.grid[x][y].block 
                pygame.draw.rect(screen, b.color, [(b.pos.x - window_pos.x) * block_size, (b.pos.y - window_pos.y) * block_size, block_size, block_size])


def draw_food_range():
    for org in game.population:
        for i in range(-1,2):
                for j in range(-1,2):
                    x, y = org.pos.x + i , org.pos.y + j
                    if Position(x,y).is_in_grid(game.grid):
                        pygame.draw.rect(screen, COLOR.VISION, [(x - window_pos.x) * block_size, (y - window_pos.y) * block_size, block_size, block_size])
          
# IDEA : get organism and food in the current window for optimisation 
# For the moment, negative values are computed but not displayed

def draw_organisms():
    for organism in game.population:
        for block in organism.blocks:
            pygame.draw.rect(screen, block.color, [(block.pos.x - window_pos.x) * block_size, (block.pos.y - window_pos.y) * block_size, block_size, block_size])

def draw_food():
    for f in game.food:
        pygame.draw.rect(screen, COLOR.FOOD, [(f.pos.x - window_pos.x) * block_size, (f.pos.y - window_pos.y) * block_size, block_size, block_size])


def draw_vision(): 
    for organism in game.population:
        vision = organism.get_vision(game) # Too slow...
        for block in vision:
            pygame.draw.rect(screen, COLOR.VISION, [(block.pos.x - window_pos.x) * block_size, (block.pos.y - window_pos.y) * block_size, block_size, block_size])

def update_variables():
    var = []
    fps = str(int(clock.get_fps()))
    var.append(FONT.arial.render(f"FPS : {fps}", 1, COLOR.ORANGE))
    var.append(FONT.arial.render(f"Org : {len(game.population)}", 1, COLOR.ORANGE))
    var.append(FONT.arial.render(f"Food : {len(game.food)}", 1, COLOR.ORANGE))
    var.append(FONT.arial.render(f"Frame : {frame_count}", 1, COLOR.ORANGE))
    return var

##################################################################################################
game.add_random_organism(100)
##################################################################################################
#shortkey
#pause/play
#reset
#edit(food and organism)
# number iteration
# hide screen


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        # Mouse wheel zoom
        elif event.type == pygame.MOUSEWHEEL:
            e_x, e_y = pygame.mouse.get_pos()
            if (block_size == 1  and event.y == 1) or block_size  > 1:
                e_block_x = int(e_x / block_size + window_pos.x)
                e_block_y = int(e_y / block_size + window_pos.y)
                block_size += event.y
                window_width = int(screen_width / block_size)
                window_height = int(screen_height / block_size)
                window_pos.x = min(max(int(e_block_x - (e_x / block_size) ), 0), screen_width - window_width - 1)
                window_pos.y = min(max(int(e_block_y - (e_y / block_size) ), 0), screen_height - window_height - 1)
        # Slider drag and drop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for s in slides:
                if s.button_rect.collidepoint(pos):
                    s.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for s in slides:
                s.hit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               pause = False
##################################################################################################  
    if not pause : 
        frame_count += 1
        #game.add_random_organism(1)
        game.add_random_food(10)
        game.check_organism_priority()
##################################################################################################  
#draw
    screen.fill(COLOR.BK)
    draw_food()
    draw_organisms()
    
    #draw_vision()
    #draw_window()

##################################################################################################
    for i, var in enumerate(update_variables()):
        screen.blit(var, (10,i* 15))
    for s in slides:
        if s.hit:
            s.move()
        s.draw(screen)
    if speed.val == 61:
        clock.tick(300) # Max speed
    elif speed.val == 5:
        pause = True
        clock.tick(300)    
    else: 
        clock.tick(speed.val)
    pygame.display.update()
pygame.display.update() 
pygame.quit()
quit()