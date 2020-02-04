import random
import pygame
from pygame.locals import *
from snake import Game as gm

max_steps = 300


def todir(action, snake):
    ''' takes action to be -1, 0, 1 with 0 meaning forward, -1 turn left, and
        1 turn right, and converts it to the correct action for snake. Note
        for the direction 0 means North, 1 means east, 2 means south, and 3
        means west.
    '''
    dir = action
    if snake.dirx == 1:
        dir = 1 + action
    elif snake.dirx == -1:
        dir = 3 + action
    elif snake.diry == 1:
        dir = 2 + action
    elif snake.diry == -1:
        dir = 0 + action
    return dir % 4


def random_games():
    for episode in range(10):
        game = gm()
        for i in range(max_steps):
            action = random.randint(-1, 1)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if game.snake.fail:
                        game.reset()
            game.step(todir(action, game.snake))
            if game.snake.fail:
                break
            game.render()


if __name__ == "__main__":
    random_games()
