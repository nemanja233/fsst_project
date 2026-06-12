import pygame
import sys
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import main
from main import height,width

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

def draw():
    main.screen.blit(backgorund,(0,0))
    main.screen.blit(bird_image, bird)

    for pipe in pipes:
        main.screen.blit(pipe.img, pipe)

def move():
    for pipe in pipes:
        pipe.x += velocity_x


def create_pipes():
    top_pipe = Pipe(top_pipe_image)
    pipes.append(top_pipe)