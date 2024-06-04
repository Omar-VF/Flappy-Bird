import pygame
from pygame.locals import *
from random import randint
from db  import scores_db
import ctypes

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()

# Game Variables
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
CLOCK = pygame.time.Clock()
FPS = 60
SCROLL_SPEED = 4
GROUND_SCROLL = 0
FLYING = False
GAME_OVER = False
PIPE_GAP = 175
PIPE_FREQUENCY = 1750  # millisec
LAST_PIPE = pygame.time.get_ticks()
SCORE = 0
PASS_PIPE = False
ZOOM = False
SCORE_CHECK = True

# Font
font = pygame.font.SysFont("Bauhaus 93", 60)

# Colours
white = (255, 255, 255)

# Game Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")


# Load Images
bg = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")
button_img = pygame.image.load("img/restart.png")


# Text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    SCORE = 0
    return SCORE


# Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load("img/Bird1.png"),
            pygame.image.load("img/Bird2.png"),
            pygame.image.load("img/Bird3.png"),
        ]
        self.index = 0
        self.counter = 0
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

            if self.rect.bottom < 768:
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
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -70)

        if not GAME_OVER and not FLYING:
            self.image = pygame.transform.rotate(self.images[self.index], 0)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        # Pos 1 = top , pos -1 = bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(PIPE_GAP / 2)]

    def update(self):
        if FLYING and not GAME_OVER:
            self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()


# Restart Button
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):
        global ZOOM
        # Get mouse pos
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                action = True

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)

button = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 60, button_img)

# Game Loop
run = True
while run:

    CLOCK.tick(FPS)

    # Draw BG
    screen.blit(bg, (0, 0))

    # Draw Ground
    screen.blit(ground, (GROUND_SCROLL, 768))

    # Draw Flappy
    bird_group.draw(screen)
    bird_group.update()

    # Draw Pipes
    pipe_group.draw(screen)
    pipe_group.update()

    # Score Check
    if len(pipe_group):
        if (
            flappy.rect.left > pipe_group.sprites()[0].rect.left
            and flappy.rect.right < pipe_group.sprites()[0].rect.right
            and PASS_PIPE == False
        ):
            PASS_PIPE = True

        if PASS_PIPE:
            if flappy.rect.left > pipe_group.sprites()[0].rect.right:
                SCORE += 1
                PASS_PIPE = False

    draw_text(str(SCORE), font, white, int(SCREEN_WIDTH / 2) - 30, 20)

    # Ground Collision
    if flappy.rect.bottom >= 768:
        GAME_OVER = True
        FLYING = False

    # Ceiling Collision
    if flappy.rect.top <= 0:
        GAME_OVER = True
        FLYING = False

    # Pipe Collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        GAME_OVER = True
        FLYING = False

    if FLYING and not GAME_OVER:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - LAST_PIPE > PIPE_FREQUENCY:
            pipe_height = randint(-150, 100)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            LAST_PIPE = time_now

        # Scroll ground
        #screen.blit(ground, (GROUND_SCROLL, 555))
        GROUND_SCROLL -= SCROLL_SPEED
        if abs(GROUND_SCROLL) > 35:
            GROUND_SCROLL = 0

    # GameOver and Restart
    if GAME_OVER:
        draw_text(
            f"HIGHEST : {str(scores_db.highscore())}",
            font,
            white,
            int(SCREEN_WIDTH / 2) - 140,
            100,
        )
        if SCORE_CHECK:
            scores_db.score_upload(SCORE)
            SCORE_CHECK = False

        if button.draw():
            GAME_OVER = False
            SCORE = reset_game()
            SCORE_CHECK = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.SCALED:
            pygame.display.toggle_fullscreen()
        if (
            (event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[K_SPACE])
            and FLYING == False
            and GAME_OVER == False
        ):
            FLYING = True

    pygame.display.update()

pygame.quit()
