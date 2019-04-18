from vis import HTML_page
import glob

page = HTML_page('vis_example.html')
img_list = glob.glob('/home/yumin/dataset/Office/amazon/images/bookcase/*.jpg')
print(len(img_list))
page.add_img_table(img_list, num_col=5)
page.add_img_table(img_list, num_col=5)
page.end_page()
