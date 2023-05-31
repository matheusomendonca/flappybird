import pygame
from constants import Constants
from model.neural_network import NeuralNetwork
import abc


class BaseBird(metaclass = abc.ABCMeta):

    bird_image = pygame.image.load("img/bird.png")

    def __init__(self,
                 screen, 
                 x: int = Constants.SCREEN_WIDTH.value // 2, 
                 y: int = Constants.SCREEN_HEIGHT.value // 2) -> None:
        
        self.x = x
        self.y = y
        self.screen = screen
        
        self.velocity = 0
        self.alive = True
        self.score = 0
        self.neural_network = NeuralNetwork()

    def jump(self):
        self.velocity = -Constants.JUMP_VELOCITY.value

    def move(self):
        self.velocity += Constants.GRAVITY.value
        self.y += self.velocity

    def draw(self):
        self.screen.blit(self.image, (self.x - Constants.BIRD_RADIUS.value, int(self.y) - Constants.BIRD_RADIUS.value))

    def change_color(self, color):
        self.image.fill(color, special_flags=pygame.BLEND_RGB_MULT)

    @abc.abstractmethod
    def compute_score(self):
        pass