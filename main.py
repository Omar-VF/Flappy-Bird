import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 487
SCREEN_HEIGHT = 548

screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

#load images
bg = pygame.image.load("img/bg.png")

run = True
while run:

    screen.blit(bg , (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()