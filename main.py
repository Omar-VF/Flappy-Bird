import pygame
from pygame.locals import *

pygame.init()

# Game Variables
SCREEN_WIDTH = 487
SCREEN_HEIGHT = 548
CLOCK = pygame.time.Clock()
FPS = 60
GROUND_SCROLL = 0
SCROLL_SPEED = 4

# Game Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load Images
bg = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")


# Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        # Handle animations
        self.counter += 1
        FLAP_COOLDOWN = 5

        if self.counter > FLAP_COOLDOWN:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
        
        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)


# Game Loop
run = True
while run:

    CLOCK.tick(FPS)

    # Draw BG
    screen.blit(bg, (0, 0))

    # Draw Flappy
    bird_group.draw(screen)
    bird_group.update()

    # Draw & scroll ground
    screen.blit(ground, (GROUND_SCROLL, 450))
    GROUND_SCROLL -= SCROLL_SPEED
    if abs(GROUND_SCROLL) > 35:
        GROUND_SCROLL = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
