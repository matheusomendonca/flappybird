"""Main execution script."""

from game.flappybird import FlappyBirdGame
from game.bird import AIBird, ManualBird


def main(play_type: str):
    """ Main execution."""

    game = FlappyBirdGame(train_mode=False)
    filename = "trained_bird.pkl"

    if play_type == 'trained_bird':

        ai_bird = AIBird(screen=game.screen)
        ai_bird.load_neural_network_weights(filename=filename)
        birds = [ai_bird]

    elif play_type == 'manual':

        bird = ManualBird(screen=game.screen)
        birds = [bird]

    elif play_type == 'competition':

        ai_bird = AIBird(screen=game.screen)
        ai_bird.load_neural_network_weights(filename=filename)
        manual_bird = ManualBird(screen=game.screen)
        birds = [ai_bird, manual_bird]

    else:
        raise ValueError("Invalid game option!")

    game.play(birds)


if __name__ == "__main__":
    main(play_type='competition')
