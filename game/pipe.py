import random
from constants import Constants
import pygame


class Pipe():

    pipe_image = pygame.image.load("img/pipe.png")


    def __init__(self, x, screen):
        self.x = x + Constants.GAP_SIZE.value
        self.screen = screen
        self.top_height = random.randint(int(0.3*Constants.SCREEN_HEIGHT.value), int(0.7*Constants.SCREEN_HEIGHT.value))
        self.bottom_start = self.top_height + Constants.GAP_SIZE.value

    def move(self):
        self.x -= Constants.PIPE_SPEED.value

    def draw(self):
        top_pipe_image = pygame.transform.scale(self.pipe_image, (Constants.PIPE_WIDTH.value, self.top_height))
        bottom_pipe_image = pygame.transform.scale(self.pipe_image, (Constants.PIPE_WIDTH.value, Constants.SCREEN_HEIGHT.value - self.bottom_start))
        self.screen.blit(pygame.transform.flip(top_pipe_image, False, True), (self.x, 0))
        self.screen.blit(bottom_pipe_image, (self.x, self.bottom_start))
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x+Constants.PIPE_WIDTH.value/2, 0.5*(self.top_height + self.bottom_start)), 10)

    def is_offscreen(self):
        return self.x < -Constants.PIPE_WIDTH.value