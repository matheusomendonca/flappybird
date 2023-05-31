from model.train import TrainBird
from game.game import FlappyBirdGame


def execute_training():
    training_process = TrainBird(game=FlappyBirdGame(train_mode=True))
    training_process.train()

if __name__=="__main__":
    execute_training()