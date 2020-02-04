import pygame
from pygame.locals import *
from snake import Game as gm

game = gm()
action = -1

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if game.snake.fail:
                game.reset()
            elif (event.key == K_SPACE):
                print(game.step(action))
            elif (event.key == (K_LEFT or K_a)):
                action = 3
                break
            elif (event.key == (K_RIGHT or K_d)):
                action = 1
                break
            elif (event.key == (K_DOWN or K_s)):
                action = 2
                break
            elif (event.key == (K_UP or K_w)):
                action = 0
                break
    game.step(action)
    if game.snake.fail:
        action = -1
    game.render()
