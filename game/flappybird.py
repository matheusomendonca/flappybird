"""Main script for the flappy bird game."""

from dataclasses import dataclass, field
from typing import Any

import pygame

from game.bird import AIBird, ManualBird
from game.pipe import Pipe
from model.constants import Constants


@dataclass
class FlappyBirdGame:
    """Flappy bird game."""

    train_mode: bool = True
    screen = pygame.display.set_mode(
        (Constants.SCREEN_WIDTH.value, Constants.SCREEN_HEIGHT.value))
    background_image: Any = field(init=False)
    clock: Any = field(init=False)
    font: Any = field(init=False)
    best_bird: dict = field(init=False)

    def __post_init__(self) -> None:

        # Initialize Pygame
        pygame.init()

        # Load images
        self.background_image = pygame.image.load("img/background.png")
        self.background_image = pygame.transform.scale(
            self.background_image, (Constants.SCREEN_WIDTH.value, Constants.SCREEN_HEIGHT.value))

        # game parameters
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.best_bird_parameters = {'weights1': None,
                                     'weights2': None,
                                     'biases1': None,
                                     'biases2': None}

    def play(self,
             birds: list[AIBird, ManualBird],
             generation: int = None,
             best_fitness: float = None) -> bool:
        """Play game."""

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

            self.screen.blit(self.background_image, (0, 0)
                             )  # Draw the background

            # Create and move pipes
            if len(pipes) == 0 or pipes[-1].x < Constants.SCREEN_WIDTH.value - 150:
                pipes.append(
                    Pipe(x=Constants.SCREEN_WIDTH.value, screen=self.screen))
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

            # Check collision and update fitness and score
            for bird in birds:

                bird.compute_score(pipes=pipes)

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

                if bird.alive and self.train_mode:
                    bird.compute_fitness()
                    if bird.fitness > best_fitness:
                        best_fitness = bird.fitness
                        self.best_bird_parameters['weights1'] = bird.neural_network.weights1.copy(
                        )
                        self.best_bird_parameters['weights2'] = bird.neural_network.weights2.copy(
                        )
                        self.best_bird_parameters['biases1'] = bird.neural_network.biases1.copy(
                        )
                        self.best_bird_parameters['biases2'] = bird.neural_network.biases2.copy(
                        )

            # Remove dead birds from the population
            birds = [bird for bird in birds if bird.alive]

            if len(birds) == 0:
                return best_fitness, False

            if self.train_mode and best_fitness > 100:
                return best_fitness, True

            if self.train_mode:
                # Render generation number and maximum score on screen
                text_generation = self.font.render(
                    "Generation: " + str(generation), True, (255, 255, 255))
                text_score = self.font.render(
                    f"Best Fitness: {best_fitness:.3f}", True, (255, 255, 255))
                self.screen.blit(text_generation, (10, 10))
                self.screen.blit(text_score, (10, 50))
            else:
                y_position = 10
                offset = 40
                for bird in birds:
                    if isinstance(bird, ManualBird):
                        text = f"Manual Score: {bird.score}"
                    elif isinstance(bird, AIBird):
                        text = f"AI Score: {bird.score}"
                    else:
                        text = f"Score: {bird.score}"
                    text_score = self.font.render(text, True, (255, 255, 255))
                    self.screen.blit(text_score, (10, y_position))
                    y_position += offset

            pygame.display.update()
            self.clock.tick(60)
