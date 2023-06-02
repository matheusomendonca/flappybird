import numpy as np
from game.pipe import Pipe
from constants import Constants
import pickle
import pygame
import abc
from model.neural_network import NeuralNetwork


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

    def compute_score(self, pipes = list[Pipe]):

        for pipe in pipes:
            pipe_checkpoint = pipe.x + Constants.PIPE_WIDTH.value/2
            bird_checkpoint = self.x
            if pipe_checkpoint > bird_checkpoint and pipe_checkpoint - bird_checkpoint < Constants.PIPE_SPEED.value:
                self.score += 1
                
    @abc.abstractmethod
    def compute_fitness(self):
        pass

class AIBird(BaseBird):

    def __init__(self, 
                 screen, 
                 x: int = Constants.SCREEN_WIDTH.value // 2, 
                 y: int = Constants.SCREEN_HEIGHT.value // 2):
        super().__init__(screen=screen,
                         x=x,
                         y=y)
        self.image = self.bird_image.copy()
        self.manual_play = False
        self.neural_network_inputs = None
        self.fitness = 0

    def jump_decision(self, pipes: list[Pipe]):

        # neural network inputs update
        self._bird_sensors(pipes=pipes)
       
        # Pass inputs through neural network and make jump decision
        decision = self.neural_network.predict(self.neural_network_inputs)[0, 0]
        if decision > 0.5:
            self.jump()
    
    def load_neural_network_weights(self, filename: str):

        # Load the pickled bird instance
        with open(filename, "rb") as file:
            bird_parameters = pickle.load(file)

        # load weights
        self.neural_network.weights1 = bird_parameters['weights1']
        self.neural_network.weights2 = bird_parameters['weights2']
        self.neural_network.biases1 = bird_parameters['biases1']
        self.neural_network.biases2 = bird_parameters['biases2']
    
    def _bird_sensors(self, pipes: list[Pipe]) -> np.ndarray:
             
        # find closest upcoming pipe
        distance_to_pipes = np.array([pipe.x - self.x for pipe in pipes])
        distance_to_pipes[distance_to_pipes < 0] = 1e6
        index_closest_pipe = np.argmin(distance_to_pipes)
        closest_pipe = pipes[index_closest_pipe] 
            
        # distance to midpoint (y-axis)
        distance_to_mid_point_closest = (closest_pipe.bottom_start + closest_pipe.top_height)/2 - self.y

        # horizontal distance to next pipe
        horizontal_distance = closest_pipe.x + Constants.PIPE_WIDTH.value/2 - self.x

        # Prepare inputs for neural network
        self.neural_network_inputs = np.array([[
                                                distance_to_mid_point_closest,
                                                horizontal_distance,
                                                self.y
                                                ]])
    
    def compute_fitness(self) -> None:
        
        vertical_distance_score = 1/(self.neural_network_inputs[0][0]+1e4)
        self.fitness += 1/Constants.SCREEN_WIDTH.value + vertical_distance_score


class ManualBird(BaseBird):

    def __init__(self, 
                 screen, 
                 x: int = Constants.SCREEN_WIDTH.value // 2, 
                 y: int = Constants.SCREEN_HEIGHT.value // 2):
        super().__init__(screen=screen,
                         x=x,
                         y=y)
        self.image = self.bird_image.copy()
        self.manual_play = True
        self.change_color(color=(255, 0, 0))

    def compute_fitness(self) -> None:
        pass
    