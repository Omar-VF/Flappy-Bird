import pygame
from pygame.locals import *

pygame.init()

# Game Variables
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 685
CLOCK = pygame.time.Clock()
FPS = 60
GROUND_SCROLL = 0
SCROLL_SPEED = 4
FLYING = False
GAME_OVER = False

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
        self.vel = 0
        self.clicked = False

    def update(self):

        # Gravity
        if FLYING:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < 555:
                self.rect.y += int(self.vel)

        if GAME_OVER == False:
            # Jump
            if (
                pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[K_SPACE]
            ) and self.clicked == False:
                self.clicked = True
                self.vel = -10

            if (
                pygame.mouse.get_pressed()[0] == 0
                and pygame.key.get_pressed()[K_SPACE] == 0
            ):
                self.clicked = False

            # Animations
            self.counter += 1
            FLAP_COOLDOWN = 5

            if self.counter > FLAP_COOLDOWN:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # Rotate
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)


# Game Loop
run = True
while run:

    CLOCK.tick(FPS)

    # Draw BG
    screen.blit(bg, (0, 0))

    # Draw Ground
    screen.blit(ground, (GROUND_SCROLL, 555))

    # Draw Flappy
    bird_group.draw(screen)
    bird_group.update()

    # Check if Bird hits the ground
    if flappy.rect.bottom > 555:
        GAME_OVER = True
        FLYING = False

    # Scroll ground
    if GAME_OVER == False:
        screen.blit(ground, (GROUND_SCROLL, 555))
        GROUND_SCROLL -= SCROLL_SPEED
        if abs(GROUND_SCROLL) > 35:
            GROUND_SCROLL = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (
            (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN)
            and FLYING == False
            and GAME_OVER == False
        ):
            FLYING = True

    pygame.display.update()

pygame.quit()
