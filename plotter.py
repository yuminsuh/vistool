import numpy as np
import matplotlib.pyplot as plt 

class Plotter(object):
    def __init__(self, num_data, suptitle='', title='', num_row=0, num_col=0, \
                 fig_w_pad=0.0, fig_h_pad=0.2, fig_rect=[0,0,1,0.9], \
                 fig_w_inch=6.4, fig_h_inch=4.8):
        self.suptitle = suptitle
        self.title = title
        self.num_data = num_data
        assert(num_data != 0)
        if num_row==0 and num_col==0:
            num_row, num_col = 1, num_data
        self.num_row = num_row
        self.num_col = num_col
        
        self.fig_w_pad = fig_w_pad
        self.fig_h_pad = fig_h_pad
        self.fig_rect = fig_rect
        self.fig_w_inch = fig_w_inch
        self.fig_h_inch = fig_h_inch

        with plt.style.context('ggplot', 'fast'):
            self.fig, self.axes_array = plt.subplots(num_row, num_col)
            self.fig.suptitle(suptitle)
            self.fig.tight_layout(w_pad=self.fig_w_pad, h_pad=self.fig_h_pad, rect=self.fig_rect)
            self.fig.set_size_inches(self.fig_w_inch, self.fig_h_inch)

    def get_axes(self, axes_idx):
        axes = self.axes_array if self.num_row==1 and self.num_col==1 else \
               self.axes_array[axes_idx] if self.num_row==1 or self.num_col==1 else \
               self.axes_array[axes_idx//self.num_col, axes_idx%self.num_col]
        return axes

    def plot_axes(self, axes_idx, x, y, label='', xlabel='', ylabel='', title=''):
        axes = self.get_axes(axes_idx)
        axes.plot(x, y, label=label)
        if xlabel!='':
            axes.set_xlabel(xlabel)
        if ylabel!='':
            axes.set_ylabel(ylabel)
        if title!='':
            axes.set_title(title)
    #     axes.legend()

    def set_axes(self, axes_idx, xlabel='', ylabel='', title=''):
        axes = self.get_axes(axes_idx)
        if xlabel != '':
            axes.set_xlabel(xlabel)
        if ylabel != '':
            axes.set_ylabel(ylabel)
        if title != '':
            axes.set_title(title)

    def preprocess(self, xs, ys):
        xs, ys = np.array(xs).squeeze(), np.array(ys).squeeze()
        if self.num_data==1:
            xs = xs.reshape(1,xs.size)
            ys = ys.reshape(1,ys.size)
        return xs, ys

    def plot_single_legend(self, xs, ys, label='', xlabel='', ylabel='', title=''):
        xs, ys = self.preprocess(xs, ys)
        for data_idx, (x, y) in enumerate(zip(xs, ys)):
            self.set_axes(data_idx, xlabel=xlabel, ylabel=ylabel, title='{} {}'.format(self.title, data_idx))
            self.plot_axes(data_idx, x, y, label=label)
            
    def legend(self, **kwargs):
        plt.legend(**kwargs)

    def show(self):
        self.fig.show()
