"""Training script."""

from model.train import TrainBird
from game.flappybird import FlappyBirdGame


def execute_training():
    """Training pipeline execution."""
    training_process = TrainBird(game=FlappyBirdGame(train_mode=True))
    training_process.train()

if __name__=="__main__":
    execute_training()
