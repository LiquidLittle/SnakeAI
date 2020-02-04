import numpy as np
import pygame
import random
from collections import deque
from pygame.locals import *

FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
height = 750
width = 750
rows = 25
surface = pygame.display.set_mode((width, height))


class Snake():

    def __init__(self):
        # the leftmost entry is considered the head
        pos = (random.randint(0, rows - 1), random.randint(0, rows - 1))
        self.body = deque()
        self.body.append(pos)
        self.reward = 0
        self.dirx = 0
        self.diry = 0
        self.fail = False
        self.fruit = createFruit(self)
        drawBox(pos)

    def move(self):
        # Take the tail of body and make it the new head
        old_tail = self.body.pop()
        # Move the new head one direction towards dirx or diry
        self.reward = 1
        if len(self.body) == 0:
            new_head = (old_tail[0] + self.dirx, old_tail[1] + self.diry)
        else:
            new_head = (self.body[0][0] + self.dirx,
                        self.body[0][1] + self.diry)
        if not self.max(new_head):
            if new_head in self.body:
                self.fail = True
                self.body.append(old_tail)
            elif new_head != self.fruit:
                drawBox(old_tail, BLACK)
                self.body.appendleft(new_head)
            else:
                self.body.append(old_tail)
                self.body.appendleft(new_head)
                self.reward = 100
                self.fruit = createFruit(self)
            drawBox(new_head)
        else:
            self.fail = True
            self.body.append(old_tail)

    def turn(self, dir):
        ''' The function for changing the direction of the snake, where 0 is UP,
        1 is right, 2 is down, and 3 is left.
        '''
        if dir == 0:
            if self.diry != 1:
                self.dirx = 0
                self.diry = -1
        elif dir == 1:
            if self.dirx != -1:
                self.dirx = 1
                self.diry = 0
        elif dir == 2:
            if self.diry != -1:
                self.dirx = 0
                self.diry = 1
        elif dir == 3:
            if self.dirx != 1:
                self.dirx = -1
                self.diry = 0

    def max(self, pos):
        # Check if the box is at the boundaries
        if pos[0] >= rows or pos[1] >= rows or pos[0] < 0 or pos[1] < 0:
            return True
        else:
            return False

    def observation(self):
        ''' The snakes "eyes". Returns a 5x5 array centered at the snakes head
            where 0 representing empty spaces, 1 representing snake blocks and
            2 representing the fruit and the angle at which the head is
            relative to the fruit.
        '''
        head = self.body[0]
        headv = np.array(head) - np.array((head[0] + self.dirx, head[1]
                                          + self.diry))
        fruitv = np.array(head) - np.array(self.fruit)
        angle = np.math.atan2(np.linalg.det([headv, fruitv]), np.dot(headv,
                                                                     fruitv))
        # Create a 2d grid with 0 representing empty spaces, 1 representing
        # snake blocks and 2 representing the fruit
        grid = np.zeros((5, 5), dtype='int8')
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                # i, j + True coord of head - (2, 2)
                if (i + head[0] - 2, j + head[1] - 2) in self.body or \
                        (i + head[0] - 2) < 0 or (j + head[1] - 2) < 0:
                    grid[j][i] = 1
                elif (i + head[0] - 2, j + head[1] - 2) == self.fruit:
                    grid[j][i] = 2
        # How many times to rotate the grid so its facing the same direction
        # as the head

        rotate = 0
        if self.dirx == 1:
            rotate = 1
        elif self.diry == 1:
            rotate = 2
        elif self.dirx == -1:
            rotate = 3

        grid = np.rot90(grid, rotate)
        return grid, angle


def createFruit(snake):
    fruitBox = random.randint(0, rows ** 2 - len(snake.body))
    # Create 2D array and fill it with False
    gameGrid = [x[:] for x in [[False] * rows] * rows]
    # Where there is part of the snake on a tile make that True
    for sPos in snake.body:
        try:
            gameGrid[sPos[0]][sPos[1]] = True
        except IndexError:
            print("Error: Pos = " + str(sPos))
    # Loop over fruitBox number of False entries in the grid
    loop_num = -1
    box_num = -1
    while loop_num != fruitBox:
        box_num += 1
        coord = numtocoord(box_num)
        if gameGrid[coord[0]][coord[1]] is False:
            loop_num += 1
    drawCircle(coord)
    return coord


def numtocoord(num):
    return (num // rows, num % rows)


def drawCircle(pos, color=(RED)):
    boxSize = height // rows
    circle = (pos[0]*boxSize+1, pos[1]*boxSize+1, boxSize-2, boxSize-2)
    pygame.draw.ellipse(surface, color, circle)


def drawBox(pos, color=(GREEN)):
    boxSize = height // rows
    box = (pos[0]*boxSize+1, pos[1]*boxSize+1, boxSize-2, boxSize-2)
    pygame.draw.rect(surface, color, box)


def drawGrid(height, rows):
    boxSize = height // rows
    x = 0
    y = 0
    for i in range(rows):
        x += boxSize
        y += boxSize

        pygame.draw.line(surface, WHITE, (x, 0), (x, height))
        pygame.draw.line(surface, WHITE, (0, y), (height, y))


def gameOver():
    font = pygame.font.Font("ARCADECLASSIC.TTF", 100)
    fontPress = pygame.font.Font("ARCADECLASSIC.TTF", 30)

    gameText = font.render('Game', True, WHITE)
    overText = font.render('Over', True, WHITE)
    pressText = fontPress.render('Press and key to restart', True, BLUE)
    surface.blit(gameText, (200, 200))
    surface.blit(overText, (200, 300))
    surface.blit(pressText, (150, 400))


def drawWindow(height, rows):
    surface.fill(BLACK)  # Set Background colour
    drawGrid(height, rows)  # Draw the boxes


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.snake = Snake()
        self.clock = pygame.time.Clock()

    def reset(self):
        surface.fill(BLACK)
        self.snake.__init__()

    def step(self, dir):
        self.snake.turn(dir)
        if dir != -1:
            if not self.snake.fail:
                self.snake.move()
                self.checkFail()
        return (self.snake.observation(), self.snake.reward, self.snake.fail,
                len(self.snake.body))

    def render(self):
        pygame.display.update()
        self.clock.tick(FPS)

    def checkFail(self):
        if self.snake.fail:
            gameOver()


def main():
    clock = pygame.time.Clock()
    # drawWindow(height, rows)
    snek = Snake()
    start = False
    pygame.display.set_caption("Snek")
    pygame.init()

    # Main game loop
    while True:
        if snek.fail:
            gameOver()
            start = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if snek.fail:
                    surface.fill(BLACK)
                    snek.__init__()
                elif (event.key == (K_LEFT or K_a)):
                    snek.turn(3)
                    start = True
                    break
                elif (event.key == (K_RIGHT or K_d)):
                    snek.turn(1)
                    start = True
                    break
                elif (event.key == (K_DOWN or K_s)):
                    snek.turn(2)
                    start = True
                    break
                elif (event.key == (K_UP or K_w)):
                    snek.turn(0)
                    start = True
                    break
        # drawWindow(height, rows)
        if start:
            snek.move()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
