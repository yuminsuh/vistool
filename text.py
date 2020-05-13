import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys
import torch
import re

parser = argparse.ArgumentParser()
parser.add_argument('--paths', nargs='+', type=str, help='text paths')
parser.add_argument('--keys', nargs='+', type=str, help='key')
parser.add_argument('--out', type=str, help='output path to save a montage')
parser.add_argument('--identifier', type=str, default=None, help='identifier')

def read_lines(txt_path):
    with open(txt_path, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    return lines

def get_keylines(lines, keyword):
    keylines = [l for l in lines if keyword in l]
    return keylines

def get_number_from_key(line, key):
    if key not in line: return None #raise ValueError("{} is not included in {}".format(key, line))
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line[line.find(key)+len(key):])
    return numbers[0]

def get_numbers_from_key(keylines, key):
    return [float(get_number_from_key(keyline,key)) for keyline in keylines]

def get_number(line, idx):
    tmp_numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line) # line에서 숫자 추출
    return tmp_numbers[idx]

def extract_numbers(txt_path, key, identifier=None):
    identifier = key if identifier is None else identifier
    print('**')
    print(identifier)
    lines = read_lines(txt_path)
    keylines = get_keylines(lines, identifier)
    numbers = get_numbers_from_key(keylines, key)
    return numbers

def plot_keys(txt_paths, keys, identifier, out=None, xlabel='iter', ylabel=''):
    if not isinstance(txt_paths, list):
        txt_paths = [txt_paths]
    if not isinstance(keys, list):
        txt_paths = [keys]

    numbers = {txt_path: {key: extract_numbers(txt_path,key,identifier) for key in keys} for txt_path in txt_paths}
    fig, ax = plt.subplots(1, len(keys))
    for i,key in enumerate(keys):
        axx = ax[i] if len(keys)>1 else ax
        for txt_path in txt_paths:
            axx.plot(numbers[txt_path][key])
        axx.set_xlabel(xlabel)
        axx.set_xlabel(ylabel)
    if out is not None:
        fig.savefig(out)
        print('figure saved to {}'.format(out))

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    plot_keys(args.paths, args.keys, identifier=args.identifier, out=args.out)

"""
def plot_keys(ax, path, det_key, keys, xlabel='', ylabel='', n=1000000):
    lines = read_lines(path)
    keylines = get_keylines(lines, det_key)
    print(len(keylines))
    print(keylines)
    for key in keys:
        ax.plot([float(get_number_from_key(line, key)) for line in keylines][:n])
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.legend(keys)
"""
