import pygame
from random import choice, randrange

RES = (600, 600)
TILE = 100
thickness = 7
xdes = -10
ydes = -10
WIDTH = 1500
HEIGHT = 1500
# loading the image of vertical wall of asteroids 
verticalwall = pygame.image.load('images/verticaltest.png')
verticalwall = pygame.transform.scale(verticalwall, (3*thickness, TILE+10))

# loading the image of the horizontal wall of asteroids
horizontalwall = pygame.image.load('images/horizontaltest.png')
horizontalwall = pygame.transform.scale(horizontalwall, (TILE+10, 3*thickness))

# setting the number of columns and rows in the maze
cols, rows = WIDTH // TILE, HEIGHT // TILE

# class for the cell of the maze
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}  # give walls to all cells when initialised
        self.visited = False  # initially all cells are unvisited
        self.thickness = thickness

    def __str__(self):
        return f'({self.x}, {self.y})'  # return the string representation of the cell

    # method to draw the walls of the cell on a screen sc
    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE

        # only draw the walls that are set as True
        if self.walls['top']:
            wall_rect = horizontalwall.get_rect(center = (x + TILE//2, y))
            sc.blit(horizontalwall, wall_rect)
        if self.walls['right']:
            wall_rect = verticalwall.get_rect(center = (x + TILE, y + TILE//2))
            sc.blit(verticalwall, wall_rect)
        if self.walls['bottom']:
            wall_rect = horizontalwall.get_rect(center = (x + TILE//2, y + TILE))
            sc.blit(horizontalwall, wall_rect)
        if self.walls['left']:
            wall_rect = verticalwall.get_rect(center = (x, y + TILE//2))
            sc.blit(verticalwall, wall_rect)


    # function to get the rectangles of the walls for collision detection
    def get_rects(self,locx,locy):
    
        rects = []
        x, y = self.x * TILE + locx, self.y * TILE + locy
        # cooridinates of the walls according to the positions of the cells
        if self.walls['top']:
            rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
        if self.walls['right']:
            rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
        if self.walls['bottom']:
            rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
        if self.walls['left']:
            rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
        return rects

    # function to check if a cell is in the dimensions of the grid or not
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    # function to check if there are unvisited neighbours of a cell and return one of them
    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        # check existence of all neighbouring cells
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        # check if the neighbouring cells are unvisited and append them to the neighbours list
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        # return one of the neighbours randomly
        return choice(neighbors) if neighbors else False
        

# function to remove walls between two adjacent cells
def remove_walls(current, next):
    # if the current cell is to the left or right of the next cell
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    # if the current cell is above or below the next cell
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

# function to check whether there is a wall between two cells
def check_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        if current.walls['left'] == False and next.walls['right'] == False:
            return False
        else:
            return True   
    elif dx == -1:
        if current.walls['right'] == False and next.walls['left'] == False:
            return False
        else:
            return True
    dy = current.y - next.y
    if dy == 1:
        if current.walls['top'] == False and next.walls['bottom'] == False:
            return False
        else:
            return True
    elif dy == -1:
        if current.walls['bottom'] == False and next.walls['top'] == False:
            return False
        else:
            return True

# function to generate the maze
def generate_maze(corner):

    # initialisation of the grid cells
    cols, rows = WIDTH // TILE, HEIGHT // TILE
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    path = []
    break_count = 1
    track = False   # if the path of the generation is to be tracked 
    found = 0   # found tells if we encountered the end point or the centre of the maze once
    # finding the destination/end point of the maze based on the corner
    global xdes
    global ydes
    if corner == 0: 
        xdes = 0 
        ydes = 0
    elif corner == 1:
        xdes = cols-1
        ydes = 0
    elif corner == 2:
        xdes = cols - 1
        ydes = rows-1
    elif corner == 3:
        xdes = 0
        ydes = rows - 1

    # keep a track of the path once you encounter the centre or the end point
    if not found and current_cell.x == (cols-1)/2 and current_cell.y == (rows-1)/2 :
        track = True
        found = 1
    if not found and current_cell.x == xdes and current_cell.y == ydes:
        track = True
        found = 2

    # if the path was found once and is found the second time, stop tracking the path
    if found==1 and current_cell.x == xdes and current_cell.y == ydes:
        track = False
    if found==2 and current_cell.x == (cols-1)/2 and current_cell.y == (rows-1)/2 :
        track = False

    # if the path is to be tracked, append the current cell to the path
    if track:
        path.append(current_cell)
    
    # loop to generate the maze
    while break_count != len(grid_cells):
        
        current_cell.visited = True
        # remove wall of the end cell based on the corner
        if corner == 0 and (current_cell.x == 0 and current_cell.y == 0):
            current_cell.walls['left'] = False
        elif corner == 1 and (current_cell.x == cols-1 and current_cell.y == 0):
            current_cell.walls['top'] = False
        elif corner == 2 and (current_cell.x == cols-1 and current_cell.y == rows-1):
            current_cell.walls['right'] = False
        elif corner == 3 and (current_cell.x == 0 and current_cell.y == rows-1):
            current_cell.walls['bottom'] = False
        # check if there are unvisited neighbours of the current cell
        next_cell = current_cell.check_neighbors(grid_cells)
        # if there are unvisited neighbours, visit one of them and make the current cell the next cell
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        # if there are no unvisited neighbours, go back to the previous cell, backtrace
        elif array:
            current_cell = array.pop() 
    
        # keep a track of the path once you encounter the centre or the end point
        if not found and current_cell.x == (cols-1)/2 and current_cell.y == (rows-1)/2 :
            track = True
            found = 1
        if not found and current_cell.x == xdes and current_cell.y == ydes:
            track = True
            found = 2

        # if the path was found once and is found the second time, stop tracking the path
        if found==1 and current_cell.x == xdes and current_cell.y == ydes:
            track = False
        if found==2 and current_cell.x == (cols-1)/2 and current_cell.y == (rows-1)/2 :
            track = False

        # if the path is to be tracked, append the current cell to the path
        if track:
            path.append(current_cell)

    return grid_cells, path, found

def save_path(path, found):
    temp = []
    # temp stores the coordinates of the cells of the correct path
    if found==2:
        # if the order of path is reverse, reverse the order in temp
        temp.append(((cols-1)/2, (rows-1)/2))  # append the centre of the maze
        for i in range(len(path)):
            temp.append(((path[len(path)-i-1]).x, (path[len(path)-i-1]).y))
    else:
        # if order of path is normal, just append the coordinates to temp
        for i in range(len(path)):
            temp.append(((path[i]).x, (path[i]).y))
        temp.append((xdes, ydes)) # append the end point of the maze
    
    # write directions into the file based on temp
    with open("path.txt", "w") as file:
        for i in range(len(temp)-1):
            # check directions based on the x, y coordinates of the cells
            if temp[i+1][0] - temp[i][0] == 1:
                file.write("right\n")
            elif temp[i+1][0] - temp[i][0] == -1:
                file.write("left\n")
            elif temp[i+1][1] - temp[i][1] == 1:
                file.write("down\n")
            elif temp[i+1][1] - temp[i][1] == -1:
                file.write("up\n")

    # write the direction to reach the rocket at the end of the maze
        if xdes == 0 and ydes == 0:
            file.write("left\n")
        elif xdes == cols-1 and ydes == rows-1:
            file.write("right\n")
        elif xdes == cols-1 and ydes == 0:
            file.write("up\n")
        elif xdes == 0 and ydes == rows-1:
            file.write("down\n")

            
