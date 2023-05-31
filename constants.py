from enum import Enum 

class Constants(Enum):

    # game constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    PIPE_WIDTH = 80
    PIPE_HEIGHT = 500
    GAP_SIZE = 150
    BIRD_RADIUS = 20
    GRAVITY = 0.2
    JUMP_VELOCITY = 3
    PIPE_SPEED = 4

    # algorithm constants
    POPULATION_SIZE = 500
    GENERATIONS = 20
    CROSSOVER_RATE = 0.8
    MUTATION_RATE = 0.05
    ELITISM_RATE = 0.2