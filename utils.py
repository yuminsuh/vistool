""" Read data from event file """
import tensorflow as tf
from collections import defaultdict

def read_data_from_eventfile(filepath):
    data = defaultdict(list)
    #for e in tf.python.summary.summary_iterator(filepath): # tensorflow 1.8+
    for e in tf.train.summary_iterator(filepath):
        for v in e.summary.value:
            data[v.tag].append((e.step, v.simple_value))
    
    for k,v in data.items():
        s, d = zip(*data[k])
        data[k] = {'step': s, 'data': d}
    
    return data

if __name__ == '__main__':
    filepath = '/home/yumin/Downloads/events.out.tfevents.1567233695.ubuntu'
    data = read_data_from_eventfile(filepath)
