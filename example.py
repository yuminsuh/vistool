from vis import Page
import glob

page = Page('pages/vis_example.html')
img_list = glob.glob('/home/yumin/dataset/office/amazon/images/bookcase/*.jpg')
print(len(img_list))
page.add_img_table(img_list, num_col=5)
page.add_img_table(img_list, num_col=5)
page.end_page()
