#!/usr/local/bin/python3

import sys
import argparse
import math

def error_exit(string):
    print(string)
    sys.exit(0)

def get_content(file):
    try:
        f = open(file, 'r')
    except:
        error_exit('Wrong file')
    content = f.read()
    return content

def is_number(s):
    if s == 'Nan':
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_count(dataset, num_categories):
    count = {c: 0 for c in num_categories}
    for data in dataset:
        for k in count:
            count[k] += 1 if k in data else 0
    return count

def get_mean(dataset, num_categories, count):
    mean = {c: 0 for c in num_categories}
    for data in dataset:
        for k in mean:
            mean[k] += data[k] / count[k] if k in data else 0
    return mean

def get_std(dataset, num_categories, mean, count):
    std = {c: 0 for c in num_categories}
    for data in dataset:
        for k in std:
            std[k] += ((data[k] - mean[k]) ** 2 / (count[k] - 1) if k in data
                    else 0)
    for k in std:
        std[k] = math.sqrt(std[k])
    return std

def get_min(dataset, num_categories):
    mini = {c: 9999999 for c in num_categories}
    for data in dataset:
        for k in mini:
            mini[k] = data[k] if k in data and data[k] < mini[k] else mini[k]
    return mini

def get_max(dataset, num_categories):
    maxi = {c: -9999999 for c in num_categories}
    for data in dataset:
        for k in maxi:
            maxi[k] = data[k] if k in data and data[k] > maxi[k] else maxi[k]
    return maxi

def get_percentile(percent, dataset, num_categories, count):
    percentile = {c: 0 for c in num_categories}
    for k in percentile:
        N = sorted([d[k] for d in dataset if k in d])
        l = (count[k] - 1) * percent
        f = math.floor(l)
        c = math.ceil(l)
        percentile[k] = (N[int(l)] if f == c
                else N[int(f)] * (c-l) + N[int(c)] * (l-f))
    return percentile

def print_describe(num_categories, metrics, *args):
    print('\t\t', end=' ')
    for c in num_categories:
        print('{:>16}'.format(c[:16], align='>'), end=' ')
    print('')
    for i, m in enumerate(metrics):
        print('{:<16}'.format(m), end=' ')
        for c in num_categories:
            print('{:>16}'.format('{0:.6f}'.format(args[i][c])), end=' ')
        print('')
    return

def get_dataset(file):
    num_categories = []
    dataset = []
    content = get_content(file)
    content_lines = content.split('\n')
    while content_lines[-1] == '':
        content_lines = content_lines[:-1]
    categories = content_lines[0].split(',')
    
    count = {el:0 for el in categories}
    for line in content_lines[1:]:
        data = {}
        for i, category in enumerate(categories):
            sp = line.split(',')
            d = sp[i] if len(sp) == len(categories) else ''
            if not d:
                continue
            data[category] = float(d) if is_number(d) else d
                
            # Numeric categories
            if category not in num_categories and d and is_number(d):
                num_categories.append(category)
                
        dataset.append(data)
    return dataset, num_categories

if __name__ == '__main__':
    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='file described')
    args = parser.parse_args()

    metrics = ['count', 'mean', 'std', 'min', '25%', '33%',
            '50%', '66%', '75%', 'max']
    dataset, num_categories = get_dataset(args.file)

    count = get_count(dataset, num_categories)
    mean = get_mean(dataset, num_categories, count)
    std = get_std(dataset, num_categories, mean, count)
    mini = get_min(dataset, num_categories)
    maxi = get_max(dataset, num_categories)
    percent25 = get_percentile(0.25, dataset, num_categories, count)
    percent33 = get_percentile(0.33, dataset, num_categories, count)
    percent50 = get_percentile(0.5, dataset, num_categories, count)
    percent66 = get_percentile(0.66, dataset, num_categories, count)
    percent75 = get_percentile(0.75, dataset, num_categories, count)

    print_describe(num_categories, metrics, count, mean, std, mini, percent25,
            percent33, percent50, percent66, percent75, maxi)
