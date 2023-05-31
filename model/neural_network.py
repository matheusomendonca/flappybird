import numpy as np

class NeuralNetwork:
    def __init__(self):
        self.input_size = 3
        self.hidden_size = 4
        self.output_size = 1

        # Randomly initialize the weights
        self.weights1 = np.random.randn(self.input_size, self.hidden_size)
        self.weights2 = np.random.randn(self.hidden_size, self.output_size)

        # Randomly initialize the biases
        self.biases1 = np.random.randn(self.hidden_size)
        self.biases2 = np.random.randn(self.output_size)

    def predict(self, inputs):
        hidden_layer_output = np.maximum(0, np.dot(inputs, self.weights1) + self.biases1)  # ReLU activation
        output = self.sigmoid(np.dot(hidden_layer_output, self.weights2) + self.biases2)
        return output

    @staticmethod
    def sigmoid(x):
        x = np.clip(x, -700, 700)
        return 1 / (1 + np.exp(-x))
