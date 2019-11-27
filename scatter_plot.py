#!/usr/local/bin/python3

from describe import get_dataset

import matplotlib.pyplot as plt
import argparse
from itertools import combinations

if __name__ == '__main__':

    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='file described')
    parser.add_argument('-lf', '--search', help='all plot', action="store_true")
    parser.add_argument('-o', '--output', type=str, help='save file')
    args = parser.parse_args()

    dataset, num_categories = get_dataset(args.file)
    num_categories.remove('Index')

    houses = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    colors = ['red', 'yellow', 'blue', 'green']
    labels = ['Gr', 'Huf', 'Rav', 'Sly']

    plt.figure()
    comb = list(combinations(num_categories, 2))

    if not args.search:
        comb = [['Defense Against the Dark Arts', 'Astronomy']]
    for t in comb:
        for i, h in enumerate(houses):
            X = [data[t[0]] for data in dataset if t[0] in data and t[1] in data and data['Hogwarts House'] == h]
            Y = [data[t[1]] for data in dataset if t[0] in data and t[1] in data and data['Hogwarts House'] == h]
            plt.scatter(X, Y, label = labels[i], color = colors[i])
        plt.legend(loc='upper right')
        plt.title("Correlated features")
        plt.xlabel(t[0])
        plt.ylabel(t[1])
        if not args.search and args.output:
            plt.savefig(args.output, format='png')
        plt.show()
