import pygame
from constants import Constants

COLOR = Constants.COLOR
FONT = Constants.FONT

class Slider():
    def __init__(self, name, val, maxi, mini, pos):
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = 650
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
 
        self.txt_surf = FONT.arial.render(name, 1, COLOR.BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))
 
        # Static graphics - slider background #
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, COLOR.BLUE, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, COLOR.ORANGE, [10, 10, 80, 10], 0)
        pygame.draw.rect(self.surf, COLOR.FOOD, [10, 30, 80, 5], 0)
 
        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes
 
        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(COLOR.TRANS)
        self.button_surf.set_colorkey(COLOR.TRANS)
        pygame.draw.circle(self.button_surf, COLOR.BLACK, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, COLOR.ORANGE, (10, 10), 4, 0)

    def draw(self,screen):
    # static
        surf = self.surf.copy()

        # dynamic
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

            # screen
        screen.blit(surf, (self.xpos, self.ypos))
 
    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi

 

