#!/usr/local/bin/python3

from describe import get_dataset

import matplotlib.pyplot as plt
import math
import argparse

if __name__ == '__main__':

    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='file described')
    parser.add_argument('-lf', '--search', help='all plot', action="store_true")
    parser.add_argument('-o', '--output', type=str, help='save file')
    args = parser.parse_args()

    houses = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    colors = ['red', 'yellow', 'blue', 'green']
    labels = ['Gr', 'Huf', 'Rav', 'Sly']

    dataset, num_categories = get_dataset(args.file)
    num_categories.remove('Index')

    p = 2
    if not args.search:
        num_categories = ['Care of Magical Creatures']
        p = 1
    plt.figure(figsize = (15, 20))
    plt.subplots_adjust(top=0.98, wspace = 0.2, hspace = 0.5)
    for j, c in enumerate(num_categories):
        plt.subplot(math.ceil(len(num_categories) / 2), p, j+1)
        for i, h in enumerate(houses):
            tmp_dataset = [data[c] for data in dataset if c in data and data['Hogwarts House'] == h]
            plt.hist(tmp_dataset, bins=25, alpha=0.5, label = labels[i], color = colors[i])
        plt.legend(loc = 'upper right')
        plt.title(c)
    if args.output:
        plt.savefig(args.output, format='png')
    plt.show()
