from vis import Page
from plotter import Plotter

import glob
import argparse
import numpy as np

def html():
    page = Page('pages/vis_example.html')
    img_list = glob.glob('/home/yumin/dataset/office/amazon/images/bookcase/*.jpg')
    print(len(img_list))
    page.add_img_table(img_list, num_col=5)
    page.add_img_table(img_list, num_col=5)
    page.end_page()

def plot():
    num_data = 4
    num_row, num_col = 1, num_data

    xs = np.arange(0, 1, 0.2)
    ys1 = np.random.rand(num_data, xs.size)
    ys2 = np.random.rand(num_data, xs.size)
    ys3 = np.random.rand(num_data, xs.size)

    plotter = Plotter(num_data=num_data, num_row=num_row, num_col=num_col, \
                      suptitle='EXAMPLE', title='title', \
                      fig_w_inch=10, fig_h_inch=3, fig_rect=[0,0,1,0.85])

    plotter.plot_single_legend([xs,xs,xs,xs], ys1, \
                                xlabel='xlabel', ylabel='ylabel', label='first')
    plotter.plot_single_legend([xs,xs,xs,xs], ys2, label='second')
    plotter.plot_single_legend([xs,xs,xs,xs], ys3, label='third')
    plotter.legend(bbox_to_anchor=(1.1, 1.05))
    plotter.show()
    input("Pause before quit")

def main(args):
    if args.example == 'html':
        html()
    elif args.example == 'plot':
        plot()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vistool examples')
    parser.add_argument('--example', type=str, default='')
    main(parser.parse_args())
