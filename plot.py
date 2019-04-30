import numpy as np
import matplotlib.pyplot as plt

def plot_mult_bar(xs, ys, group_names, xlabel='', ylabel='', title=''):

    num_group = len(ys)
    colors = [plt.get_cmap('jet')(i) for i in np.linspace(0, 1., num_group)]
    starts = np.arange(len(ys[0]))
    fig, ax = plt.subplots()
    bar_width = 0.25
    opacity = 0.8

    for group_idx in range(len(ys)):
        print(starts+bar_width)
        print(ys[group_idx])
        plt.bar(starts+bar_width*group_idx, ys[group_idx], \
                bar_width, alpha=opacity, \
                color=colors[group_idx], label=group_names[group_idx])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(starts + bar_width, xs)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    xs = ['A', 'B', 'C', 'D']
    ys = [[90, 55, 40, 65], [85, 62, 54, 20]]
    plot_mult_bar(xs, ys, ['hi','bye'])
