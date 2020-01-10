import math
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
height = 1000
width = 1000
rows = 25
surface = pygame.display.set_mode((width, height))


class Snake():

    def __init__(self):
        # the leftmost entry is considered the head
        pos = (random.randint(0, rows), random.randint(0, rows))
        self.body = deque()
        self.body.append(pos)
        self.dirx = 0
        self.diry = 0
        self.fail = False
        self.fruit = createFruit(self)
        drawBox(pos)

    def move(self):
        # Take the tail of body and make it the new head
        old_tail = self.body.pop()
        # Move the new head one direction towards dirx or diry
        if len(self.body) == 0:
            new_head = (old_tail[0] + 1*self.dirx, old_tail[1] + 1*self.diry)
        else:
            new_head = (self.body[0][0] + 1*self.dirx,
                        self.body[0][1] + 1*self.diry)
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
                self.fruit = createFruit(self)
            drawBox(new_head)
        else:
            self.fail = True
            self.body.append(old_tail)

    def max(self, pos):
        # Check if the box is at the boundaries
        if pos[0] >= rows or pos[1] >= rows or pos[0] < 0 or pos[1] < 0:
            return True
        else:
            return False


def createFruit(snake):
    # Create an array which if the snake occupys that space it will be True
    snakeGrid = [False] * (rows ** 2)
    for i in range(len(snake.body)):
        place = snake.body[i][0] + snake.body[i][1] * rows
        snakeGrid[place] = True
    # the random number corresponding to an empty grid
    randGrid = random.randint(0, rows**2 - len(snake.body))
    # We find the real position of the fruit by counting to the
    # rand grid and skipping over any grids that are filled with a snake
    gridPos = 0
    counter = 0
    freePosition = False
    while not freePosition:
        if gridPos == randGrid:
            if snakeGrid[counter] is False:
                freePosition = True
                break
        elif snakeGrid[counter] is False:
            gridPos += 1
        counter += 1
    pos = (counter % rows, counter // rows)
    drawCircle(pos)
    return pos


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

    def reset(self):
        self.screen = pygame.display.set_mode((width, height))
        self.snake = Snake()
        self.clock = pygame.time.Clock()





def main():
    clock = pygame.time.Clock()
    # drawWindow(height, rows)
    snek = Snake()
    start = False
    fail = False
    pygame.display.set_caption("Snek")
    pygame.init()

    # Main game loop
    while True:
        if snek.fail:
            gameOver()
            start = False
            fail = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if fail:
                    surface.fill(BLACK)
                    snek.__init__()
                    fail = False
                    print(snek.body)
                elif (event.key == (K_LEFT or K_a)):
                    if snek.dirx != 1:
                        snek.dirx = -1
                        snek.diry = 0
                        start = True
                        break
                elif (event.key == (K_RIGHT or K_d)):
                    if snek.dirx != -1:
                        snek.dirx = 1
                        snek.diry = 0
                        start = True
                        break
                elif (event.key == (K_DOWN or K_s)):
                    if snek.diry != -1:
                        snek.diry = 1
                        snek.dirx = 0
                        start = True
                        break
                elif (event.key == (K_UP or K_w)):
                    if snek.diry != 1:
                        snek.diry = -1
                        snek.dirx = 0
                        start = True
                        break
        # drawWindow(height, rows)
        if start:
            snek.move()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
