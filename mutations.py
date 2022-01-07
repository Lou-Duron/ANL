from Objects import *
from Organisms import *
from game import Game
import random

def add_block(org: Organism, game):
    adj_squares = org.getAdjacentSquares(game)
    if len(adj_squares) > 0:
        print(f"Size : {len(org.blocks)} -> {len(org.blocks) + 1}")
        new_pos = random.choice(adj_squares).pos
        new_block = Block(new_pos.x, new_pos.y, org.color, TYPE.BODY)
        org.blocks.append(new_block)
        game.grid[new_block.pos.x][new_block.pos.y].block = new_block

    # Remove block
def remove_block(org: Organism, game):
    if len(org.blocks) > 2 :
        print(f"Size : {len(org.blocks)} -> {len(org.blocks) - 1}")
        for block in reversed(org.blocks): ## ! Remove only body !
            if block.type == TYPE.BODY:
                org.blocks.remove(block)
                game.grid[block.pos.x][block.pos.y].block = None
                break
    else :
        print("Too small to shrink...")

def change_color(org: Organism):
    new_col = random.choice(list(COLOR.ORG))
    print(f"Color")
    org.color = new_col
    for block in org.blocks[1:]:
        block.color = new_col
    pass
