import pygame
import sys
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import main
from main import height,width
import random

bird_y = height / 2
bird_x = width / 8
bird_width = 34
bird_height = 24

pipe_x = width
pipe_y = 0
pipe_width=64
pipe_height=512

backgorund = pygame.image.load(r"C:\Users\necan\OneDrive\Documents\Schule\FSST\project_dbpy\flappybirdbg.png")
bird_image = pygame.image.load(r"C:\Users\necan\OneDrive\Documents\Schule\FSST\project_dbpy\flappybird.png")
bird_image = pygame.transform.scale(bird_image,(bird_width,bird_height))
top_pipe_image = pygame.image.load(r"C:\Users\necan\OneDrive\Documents\Schule\FSST\project_dbpy\toppipe.png")
bot_pipe_image = pygame.image.load(r"C:\Users\necan\OneDrive\Documents\Schule\FSST\project_dbpy\bottompipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image,(pipe_width,pipe_height))
bot_pipe_image = pygame.transform.scale(bot_pipe_image,(pipe_width,pipe_height))


class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False


class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

bird = Bird(bird_image)

pipes = []
timer_pipes = pygame.USEREVENT + 0          #Custom event
pygame.time.set_timer(timer_pipes, 1500)
velocity_x = -2

velocity_y = 0
gravity = 0.4

score = 0
game_over = False

def draw():
    main.screen.blit(backgorund,(0,0))
    main.screen.blit(bird_image, bird)

    for pipe in pipes:
        main.screen.blit(pipe.img, pipe)

    text = str(int(score))

    if game_over:
        text = f"Game Over: " + text

    text_font = pygame.font.SysFont("Arial", 45)
    text_render = text_font.render(text,True,"white")
    main.screen.blit(text_render,(5,0))


def move():
    global velocity_y, game_over, score
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > main.height:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe_width:
            score += 0.5
            pipe.passed = True

        if bird.colliderect(pipe):
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x + pipe_width < 0:         # Speicher problem
        pipes.pop(0)

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2)
    opening_space = main.height/4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bot_pipe = Pipe(bot_pipe_image)
    bot_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bot_pipe)