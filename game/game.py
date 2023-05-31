from game.bird import AIBird
from game.pipe import Pipe
import pygame
from constants import Constants
import numpy as np
from typing import Any
from dataclasses import dataclass, field


@dataclass
class FlappyBirdGame:

    train_mode: bool = True
    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH.value, Constants.SCREEN_HEIGHT.value))
    background_image: Any = field(init=False)
    clock: Any = field(init=False)
    score: int = field(init=False)
    font: Any = field(init=False)
    best_bird: dict = field(init=False)

    def __post_init__(self) -> None:

        # Initialize Pygame
        pygame.init()
        
         # Load images
        self.background_image = pygame.image.load("img/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (Constants.SCREEN_WIDTH.value, Constants.SCREEN_HEIGHT.value))
        
        # game parameters
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.best_bird_parameters = {'weights1': None,
                                     'weights2': None,
                                     'biases1': None,
                                     'biases2': None}

    def play(self, birds: list[AIBird], generation: int = None) -> None:
         
        pipes = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            if bird.manual_play:
                                bird.jump()

            self.screen.blit(self.background_image, (0, 0))  # Draw the background

            # Create and move pipes
            if len(pipes) == 0 or pipes[-1].x < Constants.SCREEN_WIDTH.value - 150:
                pipes.append(Pipe(x=Constants.SCREEN_WIDTH.value, screen=self.screen))
            for pipe in pipes:
                pipe.move()
                pipe.draw()
                if pipe.is_offscreen():
                    pipes.remove(pipe)

            # Perform actions for each bird
            for bird in birds:
                bird.move()
                bird.draw()

                # Prepare inputs for neural network
                if not bird.manual_play:
                                     
                    # Pass inputs through neural network and make jump decision
                    bird.jump_decision(pipes=pipes)

            # Check collision and update score
            for bird in birds:
                if bird.alive:
                    if bird.y > Constants.SCREEN_HEIGHT.value or bird.y < 0:
                        bird.alive = False
                    else:
                        for pipe in pipes:
                            if (bird.x + Constants.BIRD_RADIUS.value > pipe.x and bird.x - 
                                Constants.BIRD_RADIUS.value < pipe.x + Constants.PIPE_WIDTH.value):
                                if (bird.y - Constants.BIRD_RADIUS.value < pipe.top_height or 
                                bird.y + Constants.BIRD_RADIUS.value > pipe.bottom_start):
                                    bird.alive = False
                if bird.alive and not bird.manual_play:
                    bird.compute_score()
                    if bird.score > self.score:
                        self.score = bird.score
                        self.best_bird_parameters['weights1'] = bird.neural_network.weights1.copy()
                        self.best_bird_parameters['weights2'] = bird.neural_network.weights2.copy()
                        self.best_bird_parameters['biases1'] = bird.neural_network.biases1.copy()
                        self.best_bird_parameters['biases2'] = bird.neural_network.biases2.copy()
            
            # Remove dead birds from the population
            birds = [bird for bird in birds if bird.alive]

            if len(birds) == 0:
                break

            if self.train_mode and self.score > 100:
                return True
          
            if self.train_mode:
                 # Render generation number and maximum score on screen
                text_generation = self.font.render("Generation: " + str(generation), True, (255, 255, 255))
                text_score = self.font.render("Max Score: " + str(self.score), True, (255, 255, 255))
                self.screen.blit(text_generation, (10, 10))
                self.screen.blit(text_score, (10, 50))

            pygame.display.update()
            if self.train_mode:
                self.clock.tick(60)
            else:
                self.clock.tick(60)