# Simple pygame program
# Import and initialize the pygame library
import pygame
from Core import *
import time

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

game = Game(40, 30, 18)
game.create()

while running:
    game.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
            running = False
        elif event.type == KEYDOWN and event.key == K_UP:
            game.change_direction(SnakeDirection.UP)
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game.change_direction(SnakeDirection.DOWN)
        elif event.type == KEYDOWN and event.key == K_LEFT:
            game.change_direction(SnakeDirection.LEFT)
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            game.change_direction(SnakeDirection.RIGHT)
    status = game.update()
    if status == GameState.CONTINUE:
        time.sleep(0.1)
        continue
    elif status == GameState.LOSE:
        time.sleep(0.1)
        game.create()
    elif status == GameState.WIN:
        time.sleep(0.1)
        running = False

pygame.quit()
