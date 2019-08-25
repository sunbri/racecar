import numpy as np
import math

def sigmoid(x):
    return 1 / (1. + np.exp(-x))

class Net:
    def __init__(self):
        self.weights_1 = 2 * np.random.randn(4, 5)
        self.weights_2 = 2 * np.random.randn(4, 4)
        self.weights_3 = 2 * np.random.randn(2, 4)
        self.biases_1 = 2 * np.random.randn(4, 1)
        self.biases_2 = 2 * np.random.randn(4, 1)
        self.biases_3 = 2 * np.random.randn(2, 1)

    def feedforward(self, inputs):
        self.layer_1 = sigmoid(np.dot(self.weights_1, inputs) + self.biases_1)
        self.layer_2 = sigmoid(np.dot(self.weights_2, self.layer_1) + self.biases_2)
        self.output = sigmoid(np.dot(self.weights_3, self.layer_2) + self.biases_3)
        return self.output

def mutate_matrix(mats):
    mat = np.zeros(mats[0].shape)
    for i in range(0, mats[0].shape[0]):
        for j in range(0, mats[0].shape[1]):
            rand = np.random.rand()
            index = math.floor(rand / (.9 / len(mats)))
            if rand <= .9:
                mat[i, j] = mats[index][i, j]
            else:
                mat[i, j] = 2 * np.random.randn()
    return mat

def mutate_networks(nets):
    mutation = Net()
    mutation.weights_1 = mutate_matrix([net.weights_1 for net in nets])
    mutation.weights_2 = mutate_matrix([net.weights_2 for net in nets])
    mutation.weights_3 = mutate_matrix([net.weights_3 for net in nets])
    mutation.biases_1 = mutate_matrix([net.biases_1 for net in nets])
    mutation.biases_2 = mutate_matrix([net.biases_2 for net in nets])
    mutation.biases_3 = mutate_matrix([net.biases_3 for net in nets])
    return mutation
