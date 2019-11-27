#!/usr/local/bin/python3

from describe import get_dataset, is_number
from logreg_train import select_right_data_to_list, g

import matplotlib.pyplot as plt
import argparse
import numpy as np

# Globals
reverse_houses = {
    0: 'Gryffindor',
    1: 'Hufflepuff',
    2: 'Ravenclaw',
    3: 'Slytherin'
}

def find_houses(dataset, theta, reverse_houses):
    test_houses = []
    arr = g(np.dot(dataset, theta.T))
    for row in arr:
        row = row.tolist()
        house = reverse_houses[row.index(max(row))]
        test_houses.append(house)
    return test_houses

def arguments_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('test', type=str, help='test file')
    parser.add_argument('weights', type=str, help='weights file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    # Argument
    args = arguments_parsing()
    dataset, num_categories = get_dataset(args.test)
    num_categories.remove('Index')
    nb = len(num_categories)
    dataset, useless = select_right_data_to_list(dataset, num_categories)

    # Read weights
    try:
        with open(args.weights, 'r') as f:
            w = np.zeros((4, nb + 1))
            fl = f.readlines()
            for i,x in enumerate(fl):
                for j,n in enumerate(x.split(',')):
                    n = float(n) if is_number(n) else 0
                    w[j][i] = n
    except:
        w = np.zeros((4, nb + 1))
    print('weights:', w)

    # Predict
    y_pred = find_houses(dataset, w, reverse_houses)

    # Create predict file
    with open('houses.csv', "w+") as f:
        f.write('Index,Hogwarts House\n')
        for i, house in enumerate(y_pred):
            f.write('{},{}'.format(i, house))
            f.write('\n')
