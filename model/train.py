from game.bird import AIBird
from constants import Constants
import numpy as np
from game.game import FlappyBirdGame
import random
from model.genetic_operations import tournament_selection, perform_crossover, perform_mutation
import pickle

class TrainBird:

    def __init__(self, game: FlappyBirdGame) -> None:
        self.game = game
    
    def initialize_population(self) -> list[AIBird]:

         # Initialize population
        return [AIBird(screen=self.game.screen) for _ in range(Constants.POPULATION_SIZE.value)]
    
    def breed_pupulation(self, parents=list[AIBird]) -> list[AIBird]:

        # Crossover and Mutation
        offspring = []
        for _ in range(int((1 - Constants.ELITISM_RATE.value) * Constants.POPULATION_SIZE.value)):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = perform_crossover(parent1, parent2)
            child = perform_mutation(child)
            offspring.append(child)

        population = parents + offspring

        # Clean up after each generation
        for bird in population:
            bird.alive = True
            bird.score = 0

        return population 
    
    def train(self):

        # initialize generation counter
        generation = 0

        # initial population
        population = self.initialize_population()

        # training loop
        trained = False
        while generation < Constants.GENERATIONS.value and not trained:

            # Get current generation's birds
            current_birds = population.copy()
            
            # Play game
            trained = self.game.play(birds=current_birds, generation=generation)
            
            # Create new generation if all birds die
            print("Generation:", generation, "Score:", self.game.score)
            scores = [bird.score for bird in current_birds]
            print(f"  avg: {np.mean(scores)}, std: {np.std(scores)/np.mean(scores)}")

            # Increment generation count
            generation += 1

            # Perform tournament selection
            parents = tournament_selection(population=current_birds)

            # breed: crossover and mutation
            population =self.breed_pupulation(parents=parents)

        # store best bird
        print("Saving model...")
        with open("trained_bird.pkl", "wb") as file:
                pickle.dump(self.game.best_bird_parameters, file)
        print("Done!")