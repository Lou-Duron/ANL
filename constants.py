import pygame

class Constants:
    
    class COLOR:
        RED = (204, 13, 13)
        ORANGE = (203, 112, 13)
        YELLOW = (219, 198, 23)
        GREEN  = (56, 183, 18)
        CYAN = (18, 183, 152)
        BLUE = (18, 69, 183)
        PURPLE = (132, 45, 164)
        ROSE = (246, 33, 251)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        BK = (30, 32, 35)
        VISION = (215,215,215)
        FOOD = (50, 118, 51)    
        TRANS = (1, 1, 1)    
        BASIC_ORG = [RED, BLUE, GREEN]
        ORG = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, ROSE, PURPLE]

    class FONT:
        verdana = pygame.font.SysFont("Verdana", 12)
        arial = pygame.font.SysFont("Arial", 12)

    class DIRECTIONS():
        NORTH = 0
        EAST = 1
        SOUTH = 2
        WEST = 3

    class TYPE():
        HEAD = 0
        BODY = 1
        EYE = 2
        LEG = 3
        ATTACK = 4
        DEFENCE = 5
        
