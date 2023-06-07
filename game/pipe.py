"""Pipes class."""

import random
import pygame
from model.constants import Constants


class Pipe:
    """Pipe class."""

    pipe_image = pygame.image.load("img/pipe.png")

    def __init__(self, x: int, screen):
        """Pipe constructor."""
        self.x = x + Constants.GAP_SIZE.value
        self.screen = screen
        self.top_height = random.randint(
            int(0.3*Constants.SCREEN_HEIGHT.value), int(0.7*Constants.SCREEN_HEIGHT.value))
        self.bottom_start = self.top_height + Constants.GAP_SIZE.value

    def move(self):
        """Move pipe."""
        self.x -= Constants.PIPE_SPEED.value

    def draw(self):
        """Draw pipes in screen."""
        top_pipe_image = pygame.transform.scale(
            self.pipe_image, (Constants.PIPE_WIDTH.value, self.top_height))
        bottom_pipe_image = pygame.transform.scale(
            self.pipe_image, (Constants.PIPE_WIDTH.value, Constants.SCREEN_HEIGHT.value - self.bottom_start))
        self.screen.blit(pygame.transform.flip(
            top_pipe_image, False, True), (self.x, 0))
        self.screen.blit(bottom_pipe_image, (self.x, self.bottom_start))
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x+Constants.PIPE_WIDTH.value /
                           2, 0.5*(self.top_height + self.bottom_start)), 10)

    def is_offscreen(self):
        """Detect if pipe is offscree."""
        return self.x < -Constants.PIPE_WIDTH.value
