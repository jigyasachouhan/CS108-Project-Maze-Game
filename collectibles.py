import pygame
from maze_generator import *
from random import choice, randrange
import math

# images for the icons of the collectibles loaded
star = pygame.image.load("images/scoreboost.png")
clock = pygame.image.load("images/timeboost.png")
logo = pygame.image.load("images/mapicon.png")

# class for the map
class map:
    def __init__(self, direction, loc, collected, n):
        self.collected = collected    # bool for whether the map is collected or not
        self.direction = direction    # direction of the end point of the maze
        self.point = False      # the map does not need to point at the beginning, only when it is collected
        #encoding the location of the map based on the levelchosen i.e n
        if loc == 0:
            self.x = WIDTH/2 - RES[0]/2 + n*TILE
            self.y = HEIGHT/2 - RES[1]/2 + n*TILE
        elif loc == 1:
            self.x = WIDTH/2 + RES[0]/2 - n*TILE
            self.y = HEIGHT/2 - RES[1]/2 + n*TILE
        elif loc == 2:
            self.x = WIDTH/2 - RES[0]/2 + n*TILE
            self.y = HEIGHT/2 + RES[1]/2 - n*TILE
        elif loc == 3:
            self.x = WIDTH/2 + RES[0]/2 - n*TILE
            self.y = HEIGHT/2 + RES[1]/2 - n*TILE
    
    # method to draw the map when it is not collected
    def draw(self, sc):
        global logo
        logo = pygame.transform.scale(logo, (TILE*2/3, TILE*2/3))  # resizing to appropriate dimensions
        logo_sq = logo.get_rect(center = (self.x, self.y))
        sc.blit(logo, logo_sq)   # displaye the map icon on the screen

    def showdir(self, sc, factor):
        self.arrow = pygame.image.load("images/RedArrow.png")  # load the arrow image
        self.arrow = pygame.transform.rotozoom(self.arrow, 90, 0.5)   # rotate the arrow to point in the right direction
    
        # set the x and y coordinates of the arrow based on the direction of the end point of the maze
        if self.direction==0:
            self.xpoint = 0
            self.ypoint = 0
            self.arrow = pygame.transform.rotozoom(self.arrow, 180*math.atan2(self.x, self.y)/math.pi, factor)
        elif self.direction==1:
            self.xpoint = cols - 1
            self.ypoint = 0
            self.arrow = pygame.transform.rotozoom(self.arrow, -180*math.atan2(WIDTH - self.x, self.y)/math.pi, factor)
        elif self.direction==2:
            self.xpoint = cols - 1
            self.y = rows - 1
            self.arrow = pygame.transform.rotozoom(self.arrow, 180 + 180*math.atan2(WIDTH - self.x, HEIGHT - self.y)/math.pi, factor)
        elif self.direction==3:
            self.xpoint = 0
            self.ypoint = rows - 1
            self.arrow = pygame.transform.rotozoom(self.arrow, 180 - 180*math.atan2(self.x, HEIGHT - self.y)/math.pi, factor)    

        arrowrect = self.arrow.get_rect(center = (300, 100))
        sc.blit(self.arrow, arrowrect)   # displaye the arrow on the screen


# class for the time booster
class timebooster:

    def __init__(self, x, y):
        self.collected = False  # by defualt the time booster is not collected
        # location of the time booster
        self.x = x*TILE + TILE/2   
        self.y = y*TILE + TILE/2

    def __str__(self):
        print("<", self.x, self.y, ">")   # debugging purposes

    # method to draw the time booster on the screen
    def draw(self, sc):
        global clock
        clock = pygame.transform.scale(clock, (TILE*3/4, TILE*3/4))     # resizing the image to appropriate dimensions
        clock_rect = clock.get_rect(center = (self.x, self.y))
        sc.blit(clock, clock_rect)  # display the time booster on the screen

# class for the score booster
class scorebooster:

    def __init__(self, x, y):
        self.collected = False  # by default the score booster is not collected
        # location of the score booster
        self.x = x*TILE + TILE/2
        self.y = y*TILE + TILE/2

    def __str__(self):
        print("<", self.x, self.y, ">")   # debugging purposes

    # method to draw the score booster on the screen
    def draw(self, sc):
        global star
        star = pygame.transform.scale(star, (TILE*2/3, TILE*2/3))   # resizing the image to appropriate dimensions
        star_rect = star.get_rect(center = (self.x, self.y))
        sc.blit(star, star_rect)   # display the score booster on the screen
        



