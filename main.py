import pygame
import pygame.image
from pygame.locals import *
from random import randint
from db import scores_db
import ctypes
import datetime


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
PIPE_FREQUENCY = 1500  # millisec
LAST_PIPE = pygame.time.get_ticks()
SCORE = 0
PASS_PIPE = False
SCORE_CHECK = True
DIFFICULTY_COUNT = -1
SWITCH = False


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

easy_img = pygame.image.load("img/Easy.png")
medium_img = pygame.image.load("img/Medium.png")
hard_img = pygame.image.load("img/Hard.png")

easy_img_alt = pygame.image.load("img/Easy_alt.png")
medium_img_alt = pygame.image.load("img/Medium_alt.png")
hard_img_alt = pygame.image.load("img/Hard_alt.png")


# Text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    global DIFFICULTY_COUNT
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    SCORE = 0
    DIFFICULTY_COUNT = -1
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


class EasyMode:
    def __init__(self, x, y, focused, image):
        self.focused = focused
        if self.focused == False:
            self.image = image
        else:
            self.image = easy_img_alt
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):
        global FLYING, PIPE_GAP, PIPE_FREQUENCY
        # Get mouse pos
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button

        if self.rect.collidepoint(pos):
            global DIFFICULTY_COUNT
            self.image = easy_img_alt
            DIFFICULTY_COUNT = 0
            if pygame.mouse.get_pressed()[0]:
                FLYING = True
                PIPE_GAP = 200
                PIPE_FREQUENCY = 1750

        if pygame.key.get_pressed()[K_SPACE] and self.focused:
            FLYING = True
            PIPE_GAP = 200
            PIPE_FREQUENCY = 1750

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))


class MediumMode:
    def __init__(self, x, y, focused, image):
        self.focused = focused
        if self.focused == False:
            self.image = image
        else:
            self.image = medium_img_alt
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):
        global FLYING, PIPE_GAP, PIPE_FREQUENCY
        # Get mouse pos
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button

        if self.rect.collidepoint(pos):
            global DIFFICULTY_COUNT
            self.image = medium_img_alt
            DIFFICULTY_COUNT = 1
            if pygame.mouse.get_pressed()[0]:
                FLYING = True
                PIPE_GAP = 175
                PIPE_FREQUENCY = 1500

        if pygame.key.get_pressed()[K_SPACE] and self.focused:
            FLYING = True
            PIPE_GAP = 175
            PIPE_FREQUENCY = 1500

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))


class HardMode:
    def __init__(self, x, y, focused, image):
        self.focused = focused
        if self.focused == False:
            self.image = image
        else:
            self.image = hard_img_alt
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):
        global FLYING, PIPE_GAP, PIPE_FREQUENCY
        # Get mouse pos
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button

        if self.rect.collidepoint(pos):
            global DIFFICULTY_COUNT
            self.image = hard_img_alt
            DIFFICULTY_COUNT = 2
            if pygame.mouse.get_pressed()[0]:
                FLYING = True
                PIPE_GAP = 150
                PIPE_FREQUENCY = 1300

        if pygame.key.get_pressed()[K_SPACE] and self.focused:
            FLYING = True
            PIPE_GAP = 150
            PIPE_FREQUENCY = 1300

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))


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

    # Cycling through difficulties
    if pygame.key.get_pressed()[K_DOWN] and not SWITCH and not GAME_OVER and not FLYING:
        SWITCH = True
        DIFFICULTY_COUNT += 1
    if pygame.key.get_pressed()[K_UP] and not SWITCH and not GAME_OVER and not FLYING:
        SWITCH = True
        DIFFICULTY_COUNT -= 1
    elif (
        not pygame.key.get_pressed()[K_DOWN]
        and not pygame.key.get_pressed()[K_UP]
        and SWITCH
    ):
        SWITCH = False
        DIFFICULTY_COUNT += 90

    if DIFFICULTY_COUNT != -1:
        if DIFFICULTY_COUNT % 3 == 0:
            easy_button = EasyMode(
                SCREEN_WIDTH - 312, (SCREEN_HEIGHT // 2) - 350, True, easy_img
            )
            medium_button = MediumMode(
                SCREEN_WIDTH - 319, (SCREEN_HEIGHT // 2) - 110, False, medium_img
            )
            hard_button = HardMode(
                SCREEN_WIDTH - 300, (SCREEN_HEIGHT // 2) + 150, False, hard_img
            )
        elif DIFFICULTY_COUNT % 3 == 1:
            easy_button = EasyMode(
                SCREEN_WIDTH - 312, (SCREEN_HEIGHT // 2) - 350, False, easy_img
            )
            medium_button = MediumMode(
                SCREEN_WIDTH - 319, (SCREEN_HEIGHT // 2) - 110, True, medium_img
            )
            hard_button = HardMode(
                SCREEN_WIDTH - 300, (SCREEN_HEIGHT // 2) + 150, False, hard_img
            )
        elif DIFFICULTY_COUNT % 3 == 2:
            easy_button = EasyMode(
                SCREEN_WIDTH - 312, (SCREEN_HEIGHT // 2) - 350, False, easy_img
            )
            medium_button = MediumMode(
                SCREEN_WIDTH - 319, (SCREEN_HEIGHT // 2) - 110, False, medium_img
            )
            hard_button = HardMode(
                SCREEN_WIDTH - 300, (SCREEN_HEIGHT // 2) + 150, True, hard_img
            )
    else:
        easy_button = EasyMode(
            SCREEN_WIDTH - 312, (SCREEN_HEIGHT // 2) - 350, False, easy_img
        )
        medium_button = MediumMode(
            SCREEN_WIDTH - 319, (SCREEN_HEIGHT // 2) - 110, False, medium_img
        )
        hard_button = HardMode(
            SCREEN_WIDTH - 300, (SCREEN_HEIGHT // 2) + 150, False, hard_img
        )

    # Draw difficulty buttons
    if not GAME_OVER and not FLYING:
        easy_button.draw()
        medium_button.draw()
        hard_button.draw()

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
            pipe_height = randint(-200, 150)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            LAST_PIPE = time_now

        # Scroll ground
        GROUND_SCROLL -= SCROLL_SPEED
        if abs(GROUND_SCROLL) > 35:
            GROUND_SCROLL = 0

    # GameOver and Restart
    if GAME_OVER:
        if SCORE_CHECK:
            difficulties = ["Easy", "Medium", "Hard"]
            difficulty = difficulties[DIFFICULTY_COUNT % 3]
            DATE = datetime.date.today()
            scores_db.score_upload(SCORE, difficulty, DATE)
            SCORE_CHECK = False

        draw_text(
            f"HIGHEST : {str(scores_db.highscore(difficulty))}",
            font,
            white,
            int(SCREEN_WIDTH / 2) - 140,
            100,
        )

        if button.draw():
            GAME_OVER = False
            SCORE = reset_game()
            SCORE_CHECK = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
