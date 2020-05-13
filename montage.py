import argparse
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='path pattern to make a montage')
parser.add_argument('out', type=str, help='output path to save a montage')
parser.add_argument('nrow', type=int, help='number of rows in the montage')
parser.add_argument('ncol', type=int, help='number of columns in the montage')

def montage(path, nrow, ncol, out=None):
    paths = glob.glob(path)
    order = np.random.permutation(len(paths))
    print(len(paths))
    
    cnt = 0
    fig, ax = plt.subplots(nrow, ncol)
    for ir in range(nrow):
        for ic in range(ncol):
            cnt += 1
            img = Image.open(paths[cnt])
            ax[ir,ic].imshow(img)
            ax[ir,ic].axis('off')
#     plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, wspace=0,hspace=0.1)
    if out is not None:
        plt.savefig(out)
        print('Saved at {}'.format(out))
    else:
        plt.show()
    print("{} x {} random images from {} images".format(nrow, ncol, len(paths)))

if __name__ == "__main__":
	args = parser.parse_args()
	montage(args.path, args.nrow, args.ncol, args.out)

# python ~/code/vistool/montage.py '/home/ma/yumin/dataset/cars196/car_ims/*.jpg' tmp_vistool.jpg 10  10
