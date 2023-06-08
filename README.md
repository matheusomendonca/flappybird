# FlappyBird AI
This is a simple implementation of the Flappy Bird game using Pygame, enhanced with an AI agent that learns to play the game. The player can either control the bird manually, watch the AI agent play the game autonomously and compete against the AI agent.

<p align="center">
  <img src="img/example.gif"/>
</p>

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone or download the repository to your local machine.
3. Install the required dependencies using the following command:
```
pip install -r requirements.txt
```

## Usage
The code has two main execution scripts:

* `execute_training.py`: execute training pipeline to play the game. Game parameters and learning algorithm parameters can be edited in `constants.Constants`.
* `main.py`: main script to play the game in three distinct modes:
  * `trained_bird`: watch the trained bird play the game (it is fun! :))
  * `manual`: manual input from the keyboard;
  * `competition`: compete against the trained bird (Human vs AI).

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

