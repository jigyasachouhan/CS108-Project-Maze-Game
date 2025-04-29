import pygame
from maze_generator import *

alien = pygame.image.load("images/alien.png")  # load the image of the alien
sizeofalien = (TILE*2/3, TILE*2/3)  # size of the alien
alien = pygame.transform.scale(alien, sizeofalien)  # resize the alien image to the appropriate dimensions

class Alien:
    # x and y store the location of the alien
    def __init__(self, x, y):
        self.x = x*TILE + TILE/2
        self.y = y*TILE + TILE/2

    def __str__(self):
        print(self.x, self.y)

    # method to draw the alien on the screen
    def draw(self, sc):
        global alien
        alien_rect = alien.get_rect(center = (self.x, self.y))
        sc.blit(alien, alien_rect)
    

        