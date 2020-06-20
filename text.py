import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path as osp
import torch
import re

parser = argparse.ArgumentParser()
parser.add_argument('--paths', nargs='+', type=str, help='text paths')
parser.add_argument('--keys', nargs='+', type=str, help='key')
parser.add_argument('--savepath', type=str, help='output path to save a montage')
parser.add_argument('--identifier', type=str, help='identifier')
parser.add_argument('--xlabel', type=str, default='epoch', help='xlabel')
parser.add_argument('--ylabel', type=str, default='', help='ylabel')
parser.add_argument('--titles', nargs='*', default=None, help='titles')

def pretty(name):
    return name.rstrip(':')

def read_lines(txt_path):
    with open(txt_path, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    return lines

def _get_keylines(lines, keyword):
    keylines = [l for l in lines if keyword in l]
    return keylines

def _get_key_value_from_line(line, key):
    if key not in line: return None #raise ValueError("{} is not included in {}".format(key, line))
#    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line[line.find(key)+len(key):])
    numbers = re.findall(r"(-?[0-9]+\.[0-9]+e-[0-9]+|-?[0-9]+\.[0-9]+)", line[line.find(key)+len(key):])
    return numbers[0]

def _get_key_values_from_lines(lines, key, identifier=None):
    if identifier is None:
        identifier = key
    keylines = _get_keylines(lines, identifier)
    return [float(_get_key_value_from_line(keyline,key)) for keyline in keylines]

def get_key_values_from_file(txt_path, key, identifier=None):
    lines = read_lines(txt_path)
    numbers = _get_key_values_from_lines(lines, key, identifier=identifier)
    return numbers

def get_key_dict_from_files(txt_paths, keys, identifier=None, filekeys=None):
    filekeys = txt_paths if filekeys is None else filekeys
    numbers = {filekey: \
                {pretty(key): get_key_values_from_file(txt_path,key,identifier) for key in keys} 
                for filekey, txt_path in zip(filekeys, txt_paths)}
    return numbers

def make_list(v, duplicate=1):
    if not isinstance(v, list):
        v = [v]
    return v * 1


def plot_keys(txt_paths, keys, identifier=None, \
              compare='files', \
              savepath=None, \
              xlabel='iter', ylabel='', titles=None, \
              figsize=(15,5)):
    txt_paths = make_list(txt_paths)
    keys = make_list(keys)
    titles = make_list(titles, duplicate=len(keys))

    numbers = get_key_dict_from_files(txt_paths, keys, identifier)

    num_key = len(keys)
    fig, ax = plt.subplots(1, num_key, figsize=figsize)
    for i, title in enumerate(titles):
        axx = ax[i] if num_key>1 else ax
        for txt_path in txt_paths:
            axx.plot(numbers[txt_path][key])
        axx.set_xlabel(xlabel)
        axx.set_ylabel(ylabel)
        if title is not None: axx.set_title(title)
    if savepath is not None:
        fig.savefig(savepath)
        print('figure saved to {}'.format(savepath))
    else:
        plt.show()

# deprecated
def _get_number_from_idx(line, idx):
    tmp_numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line) # line에서 숫자 추출
    return tmp_numbers[idx]



from tensorflow.python.summary.summary_iterator import summary_iterator
import os.path as osp
import glob

class TBLogParser(object):
    def __init__(self, logdir):
        self.logdir = logdir
        self.set_logpath()
        self.data = [d for d in summary_iterator(self.logpath)]
        self.set_keys()
        self.set_values()
    def set_logpath(self):
        logdir = self.logdir
        logdir = logdir.replace('[','LBRACE').replace(']','RBRACE')
        logdir = logdir.replace('LBRACE', '[[]').replace('RBRACE', '[]]')
        self.logpath = glob.glob(osp.join(logdir, '*tfevents*'))[-1]
    def extract(self, key):
        steps = []
        values = []
        for d in self.data:
            for v in d.summary.value:
                if v.tag == key:
                    steps.append(d.step)
                    values.append(v.simple_value)
        return steps, values
    def set_keys(self):
        self.keys = set()
        for d in self.data:
            for v in d.summary.value:
                self.keys = self.keys.union([v.tag])
    def set_values(self):
        self.values = {key: self.extract(key) for key in self.keys}


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    plot_keys(args.paths, args.keys, identifier=args.identifier, savepath=args.savepath, xlabel=args.xlabel, ylabel=args.ylabel, titles=args.titles)

"""
def plot_keys(ax, path, det_key, keys, xlabel='', ylabel='', n=1000000):
    lines = read_lines(path)
    keylines = _get_keylines(lines, det_key)
    print(len(keylines))
    print(keylines)
    for key in keys:
        ax.plot([float(_get_key_value_from_line(line, key)) for line in keylines][:n])
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.legend(keys)
"""
