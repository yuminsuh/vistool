import cv2
import base64
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os.path as osp


class Page(object):
    def __init__(self, savepath):
        self.savepath = savepath
        self.file = open(savepath, 'w')
        self.file.write('<html><body>\n')

    def add_img_table(self, img_list=[], correct_list=None, num_col=5, bottom_legend=None, msg=''):
        table = Table(msg=msg)
        self.file.write(table.img_table(img_list, num_col, correct_list=correct_list, bottom_legend=bottom_legend))

    def end_page(self):
        self.file.write('</body></html>')
        self.file.flush()

class Table(object):
    def __init__(self, msg=''):
        self.code = '<table cellspacing="0" cellpadding="0">\n'
        self.msg = msg

    def img_table(self, img_list, num_col, correct_list=None, row_numbering=False, bottom_legend=None):
        correct_list = [True] * len(img_list) if correct_list==None else correct_list
        bottom_legend = [''] * len(img_list) if bottom_legend==None else bottom_legend
        num_img = len(img_list)
        num_row = num_img//num_col + 1
        self.code += '<tr><td>{}</td></tr>\n'.format(self.msg)
        self.code += '<tr><td>#image={}</td></tr>\n'.format(num_img)
        for row_idx in range(num_row):
            self.begin_row(row_idx if row_numbering else None)
            for col_idx in range(num_col):
                img_idx = row_idx*num_col + col_idx
                if img_idx >= num_img:   break
                img_path = img_list[img_idx]
                img = np.array(Image.open(img_path))
                self.cell(self._figure(img, top_legend=osp.basename(img_path), bottom_legend=(bottom_legend[img_idx], correct_list[img_idx])))
            self.end_row()
        self.end_table()
        return self.code

    def begin_row(self, row_idx=None):
        self.code += '<tr>'
        if row_idx!=None:
            self.cell('#{}'.format(row_idx))

    def end_row(self):
        self.code += '</tr>\n'

    def end_table(self):
        self.code += '</table>\n'

    def cell(self, obj = '', style = ''):
        self.code += '<td style="{}">{}</td>\n'.format(style, str(obj))

    # code written by Vadim Kantorov (http://vadimkantorov.com)
    def _figure(self, image = None, top_legend = '', bottom_legend = '', interpolation = cv2.INTER_LINEAR, width = 150, height = 150, bgr_image = None):
        # image: uint8 numpy.ndarry. (h x w x 3)
        image = cv2.resize(image, dsize = (width, height), interpolation = interpolation) if interpolation is not None else image
        code = '<td><figure><figure style="margin:0; width: {}px"><figcaption style="font-size: 0.7em">{}</figcaption></figure><img src="data:image/jpeg;base64,{}" width="{}" height="{}" /><figcaption style="background: {}">{}</figcaption></figure></td>'.format(width, top_legend, base64.b64encode(cv2.imencode('.jpg', image)[1]).decode('ascii'), width, height, ('green' if bottom_legend[1] is True else 'red' if bottom_legend[1] is False else 'white' if bottom_legend[1] is None else bottom_legend[1]) if isinstance(bottom_legend, tuple) else 'white', '&nbsp;' + (bottom_legend[0] if isinstance(bottom_legend, tuple) else bottom_legend))
        return code 
