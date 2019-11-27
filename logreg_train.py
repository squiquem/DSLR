#!/usr/local/bin/python3

from describe import get_dataset, error_exit

import matplotlib.pyplot as plt
import argparse
import numpy as np
import random

# Globals
houses = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
houses_y = {
    'Gryffindor': [1, 0, 0, 0],
    'Hufflepuff': [0, 1, 0, 0],
    'Ravenclaw': [0, 0, 1, 0],
    'Slytherin': [0, 0, 0, 1]
}

def g(z):
    """
    Sigmoid
    """
    return 1 / (1 + np.exp(-z))

def standardization(X):
    """
    Input: 1d-array
    Returns standardized input
    """
    m = sum(X) / len(X)
    std = np.sqrt(sum((X - m)**2) / (len(X) - 1))
    for i in range(len(X)):
        X[i] = (X[i] - m) / std
    return X

def select_right_data_to_list(dataset, num_categories):
    """
    Inputs: dataset (dictionary), list of numeric categories
    Removes NaN, returns array with only numeric categories 
    and 1d-array from hogwarts houses
    """
    new = []
    y = []
    for data in dataset:
        newel = []
        for c in num_categories:
            newel.append(data[c]) if c in data else newel.append(0)
        if 'Hogwarts House' in data:
            y.append(houses_y[data['Hogwarts House']])
        new.append(newel)
    s = np.array([np.array([1] + xi) for xi in new])
    for i in range(1, len(s[0])):
        s[:, i] = standardization(s[:, i])
    return s, np.array(y)

def cost(X, Y, theta):
    """
    theta * X = Y
    m = students nb
    n = parameters nb
    Y = matrix(4, m)
    X = matrix(n, m)
    theta = matrix(4, n)
    Cost function
    """
    if len(X) != len(Y):
        error_exit('House data error')
    result = np.zeros(4)
    for j in range(4):
        for i, x in enumerate(X):
            result[j] += Y[i][j] * np.log(g(np.dot(theta[j], x))) \
                    + (1 - Y[i][j]) * np.log(1 - g(np.dot(theta[j], x)))
        result[j] /= -len(X)
    return result

def new_theta(lr, X, Y, theta):
    """
    Gradient descent function
    """
    m = len(X)
    n = len(X[0])
    for j in range(4):
        theta[j] -= 2 * lr / m * np.dot(g(np.dot(X, theta[j]))- Y[j], X)
    return theta

def arguments_parsing():
    """
    Parsing arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='file described')
    parser.add_argument('-e', '--epochs', type=int,
            help='number of iterations', default=100)
    parser.add_argument('-lr', '--learningrate', type=float,
            help='learning rate', default=0.1)
    parser.add_argument('-o', '--output', type=str,
            help='output file', default='weights.txt')
    parser.add_argument('-st', '--stochastic', action='store_true',
            help='stochastic gradient descent or not')
    args = parser.parse_args()
    return args

def plotting(E, C):
    """
    Plotting graphs for houses
    """
    plt.plot(E, C[:,0], color='r')
    plt.plot(E, C[:,1], color='g')
    plt.plot(E, C[:,2], color='b')
    plt.plot(E, C[:,3], color='y')
    plt.xlabel('Epochs')
    plt.ylabel('Cost')
    plt.title('Cost = f(epochs)')
    plt.show()

def create_w_file(theta):
    """
    Creating weights file for prediction
    """
    with open(args.output,"w+") as f:
        for i in range(n):
            for j in range(3):
                f.write('{}, '.format(theta[j][i]))
            f.write('{}'.format(theta[3][i]))
            f.write('\n')

if __name__ == '__main__':

    # Arguments
    args = arguments_parsing()
    lr, epochs = args.learningrate, args.epochs
    if epochs <= 0:
        error_exit('Enter positive number of epochs')
    if lr <= 0:
        error_exit('Enter positive learning rate')

    # Preprocessing
    dataset, num_categories = get_dataset(args.file)
    num_categories.remove(num_categories[0])
    X, y = select_right_data_to_list(dataset, num_categories)
    m, n = len(X), len(X[0])
    theta = np.zeros((4, n))
    E, C = [i for i in range(epochs)], np.zeros((epochs, 4))

    for e in range(epochs):
        print("Epoch", e + 1, "/", epochs, end='\r')
        if args.stochastic:
            for i in range(10):
                sampling = random.choices(dataset, k=200)
                X, y = select_right_data_to_list(sampling, num_categories)
                C[e] = cost(X, y, theta)
                theta = new_theta(lr, X, y.T, theta)
        else:
            C[e] = cost(X, y, theta)
            theta = new_theta(lr, X, y.T, theta)

    # Plot cost=f(epoch)
    plotting(E, C)

    # Create file
    create_w_file(theta)
