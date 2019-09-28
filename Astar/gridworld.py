import pygame, sys, time, random
from pygame.locals import *
import numpy as np

action_dict = {
    '0' : "Up",
    '1' : "Down",
    '2' : "Right",
    '3' : "Left",
}

# User-defined Classes

class Tile:
    borderColor = pygame.Color('black')
    borderWidth = 4
    image = pygame.image.load('./Static/marvin.jpg')

    def __init__(self, x, y, wall, surface, tile_size = (100, 100)):
        self.wall = wall
        self.origin = (x, y)
        self.tile_coord = [x//100, y//100]
        self.surface = surface
        self.tile_size = tile_size

    def draw(self, pos, goal):
        #     Draw the tile.
        rectangle = pygame.Rect(self.origin, self.tile_size)
        if self.wall:
            pygame.draw.rect(self.surface, pygame.Color('gray'), rectangle, 0)
        elif goal == self.tile_coord:
            pygame.draw.rect(self.surface, pygame.Color('green'), rectangle, 0)
        else:
            pygame.draw.rect(self.surface, pygame.Color('white'), rectangle, 0)

        if pos == self.tile_coord:
            self.surface.blit(Tile.image, self.origin)

        pygame.draw.rect(self.surface, Tile.borderColor, rectangle, Tile.borderWidth)


class Grid_World():
    tile_width = 100
    tile_height = 100
    def __init__(self, surface, board_size = (6, 9), wall_coords = [], start_coord = (0, 3), goal_coord = (5, 8)):
        self.surface = surface
        self.bgColor = pygame.Color('black')
        self.board_size = list(board_size)
        if not wall_coords:
            self.wall_coords = [[2,i] for i in range(board_size[1]-1)]
        else:
            self.wall_coords = wall_coords

        self.start_coord = list(start_coord)
        self.goal_coord = list(goal_coord)
        self.position = list(start_coord)
        self.actions = range(4)
        self.reward = 0

        self.calc_wall_coords()
        self.createTiles()

    def calc_wall_coords(self):
        self.board_wall_coords = [[self.board_size[0] - x - 1, y] for x, y in self.wall_coords]

    def find_board_coords(self, pos):
        x = pos[1]
        y = self.board_size[0] - pos[0] -1
        return [x, y]

    def createTiles(self):
        self.board = []
        for rowIndex in range(0, self.board_size[0]):
            row = []
            for columnIndex in range(0, self.board_size[1]):
                imageIndex = rowIndex * self.board_size[1] + columnIndex
                x = columnIndex * Grid_World.tile_width
                y = rowIndex *  Grid_World.tile_height
                if [rowIndex, columnIndex] in self.board_wall_coords:
                    wall = True
                else:
                    wall = False
                tile = Tile(x, y, wall, self.surface)
                row.append(tile)
            self.board.append(row)

    def draw(self):
        pos = self.find_board_coords(self.position)
        goal = self.find_board_coords(self.goal_coord)
        self.surface.fill(self.bgColor)
        for row in self.board:
            for tile in row:
                tile.draw(pos, goal)

    def update(self):
        if self.position == self.goal_coord:
            return True
        else:
            self.draw()
            return False

    def step(self, action):
        x, y = self.position
        if action == 0:           #action up
            if [x+1, y] not in self.wall_coords and x+1 < self.board_size[0]:
                self.position = [x+1, y]

        elif action == 1:         #action down
            if [x-1, y] not in self.wall_coords and x-1 >= 0:
                self.position = [x-1, y]

        elif action == 2:         #action right
            if [x, y+1] not in self.wall_coords and y+1 < self.board_size[1]:
                self.position = [x, y+1]

        elif action == 3:         #action left
            if [x, y-1] not in self.wall_coords and y-1 >= 0:
                self.position = [x, y-1]
        # Reward definition
        if self.position == self.goal_coord:
            self.reward = 1
        else:
            self.reward = 0

    def change_the_wall(self, wall_coords):
        self.wall_coords = wall_coords
        self.calc_wall_coords()
        self.createTiles()

    def change_the_goal(self, goal):
        self.goal_coord = list(goal)

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # Set window size and title, and frame delay
    surfaceSize = (1000, 600)
    windowTitle = 'Grid_World'
    pauseTime = 1  # smaller is faster game

    # Create the window
    surface = pygame.display.set_mode(surfaceSize, 0, 0)
    pygame.display.set_caption(windowTitle)

    # create and initialize objects
    gameOver = False
    board = Grid_World(surface)

    # Draw objects
    board.draw()

    # Refresh the display
    pygame.display.update()

    # Loop forever
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                # Handle additional events

        # Update and draw objects for next frame
        gameOver = board.update()
        if gameOver:
            break

        # Refresh the display
        pygame.display.update()

        # Set the frame speed by pausing between frames
        time.sleep(pauseTime)