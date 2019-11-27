#!/usr/local/bin/python3

from describe import get_dataset

import matplotlib.pyplot as plt
import argparse

if __name__ == '__main__':

    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='file described')
    parser.add_argument('-o', '--output', type=str, help='save file')
    args = parser.parse_args()

    dataset, num_categories = get_dataset(args.file)
    num_categories.remove('Index')
    nb = len(num_categories)

    houses = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    colors = ['red', 'yellow', 'blue', 'green']
    labels = ['Gr', 'Huf', 'Rav', 'Sly']

    plt.figure(figsize=(20, 15))
    plt.subplots_adjust(top=0.98, right=0.99, left=0.07, bottom=0.07, hspace=0.3, wspace=0.2)
    for j, c1 in enumerate(num_categories):
        for k, c2 in enumerate(num_categories):
            plt.subplot(nb, nb, j * nb + k + 1)
            for i, h in enumerate(houses):
                X = [data[c1] for data in dataset if c1 in data and c2 in data and data['Hogwarts House'] == h]
                Y = [data[c2] for data in dataset if c1 in data and c2 in data and data['Hogwarts House'] == h]
                if c1 == c2:
                    plt.hist(X, bins=25, alpha=0.5, label = labels[i], color = colors[i])
                else:
                    plt.scatter(Y, X, s=1, label = labels[i], color = colors[i])
            plt.xlabel(c2, rotation=12) if j == nb - 1 else plt.xticks([])
            plt.ylabel(c1, rotation=78) if k == 0 else plt.yticks([])
    plt.legend(loc='upper right')
    plt.title('Pair plot')
    if args.output:
        plt.savefig(args.output, format='png')
    plt.show()
