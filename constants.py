import pygame

class Constants:
    
    class COLOR:
        RED = (176, 4, 4)
        ORANGE = (240, 121, 23)
        BLUE = (25, 107, 195)
        GREEN  = (140, 195, 25)
        YELLOW = (223, 240, 16)
        BLACK = (0, 0, 0)
        BK = (30, 32, 35)
        VISION = (215,215,215)
        FOOD = (50, 118, 51)    
        TRANS = (1, 1, 1)    
        ORG = [RED, ORANGE, BLUE, GREEN, YELLOW]
        
    class FONT:
        verdana = pygame.font.SysFont("Verdana", 12)
        arial = pygame.font.SysFont("Arial", 12)

    class DIRECTIONS():
        NORTH = 0
        EAST = 1
        SOUTH = 2
        WEST = 3
        
        
