"""Genetic operations for optization."""

import random

import numpy as np

from game.bird import AIBird
from model.constants import Constants
from model.neural_network import NeuralNetwork


def tournament_selection(population: list[AIBird]):
    """Perform tournament selection"""
    parents = []
    for _ in range(int(Constants.ELITISM_RATE.value * Constants.POPULATION_SIZE.value)):
        candidate1 = random.choice(population)
        candidate2 = random.choice(population)
        if candidate1.fitness > candidate2.fitness:
            parents.append(candidate1)
        else:
            parents.append(candidate2)
    return parents


def perform_crossover(parent1: AIBird, parent2: AIBird):
    """One-point crossover between two parents."""

    if random.random() < Constants.CROSSOVER_RATE.value:
        # Create empty child network
        child_network = NeuralNetwork()

        # Perform one-point crossover for weights1
        crossover_point = random.randint(0, child_network.weights1.size)
        child_network.weights1 = np.concatenate(
            (parent1.neural_network.weights1[:crossover_point],
             parent2.neural_network.weights1[crossover_point:])
        )

        # Perform one-point crossover for weights2
        crossover_point = random.randint(0, child_network.weights2.size)
        child_network.weights2 = np.concatenate(
            (parent1.neural_network.weights2[:crossover_point],
             parent2.neural_network.weights2[crossover_point:])
        )

        # Perform one-point crossover for biases1
        crossover_point = random.randint(0, child_network.biases1.size)
        child_network.biases1 = np.concatenate(
            (parent1.neural_network.biases1[:crossover_point],
             parent2.neural_network.biases1[crossover_point:])
        )

        # Perform one-point crossover for biases2
        crossover_point = random.randint(0, child_network.biases2.size)
        child_network.biases2 = np.concatenate(
            (parent1.neural_network.biases2[:crossover_point],
             parent2.neural_network.biases2[crossover_point:])
        )

        # Create and return the child with the new network
        child = AIBird(screen=parent1.screen)
        child.neural_network = child_network
        offspring = child
    else:
        if random.random() < 0.5:
            offspring = parent1
        else:
            offspring = parent2
    return offspring


def perform_mutation(bird: AIBird):
    """Perform mutation."""
    # Mutate weights in the hidden layer
    for i in range(bird.neural_network.hidden_size):
        for j in range(bird.neural_network.input_size):
            if random.random() < Constants.MUTATION_RATE.value:
                bird.neural_network.weights1[j][i] += np.random.normal(0, 0.1)

     # Mutate weights in the output layer
    for i in range(bird.neural_network.output_size):
        for j in range(bird.neural_network.hidden_size):
            if random.random() < Constants.MUTATION_RATE.value:
                bird.neural_network.weights2[j][i] += np.random.normal(0, 0.1)

    # Mutate biases1
    for i in range(bird.neural_network.hidden_size):
        if random.random() < Constants.MUTATION_RATE.value:
            bird.neural_network.biases1[i] += np.random.normal(0, 0.1)

    # Mutate biases2
    for i in range(bird.neural_network.output_size):
        if random.random() < Constants.MUTATION_RATE.value:
            bird.neural_network.biases2[i] += np.random.normal(0, 0.1)

    return bird
