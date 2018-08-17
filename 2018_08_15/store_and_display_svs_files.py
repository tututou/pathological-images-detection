import pyvips
import os
import re_test

# 项目中的svs文件目录
# svsFiles_dir = os.path.join(os.getcwd(), 'svs/')
svsFiles_dir = '/home/frodo/Desktop/work/codes/ubuntu/pathological_images_storage_and_display/svs'
# dzi文件存储目录（在浏览器的root目录下）
dst_dir = '/home/frodo/Desktop/openseadragon/zoomFiles'
# 获取svs目录下的所有文件
file_list = os.listdir(svsFiles_dir)

for filename in file_list:
    # 如果是svs文件，则进行相关操作
    if filename.endswith('.svs'):

        name, suffix = filename.split('.')
        if os.path.exists(os.path.join(dst_dir, name + '.html')):
            continue

        # 读取svs文件
        svs = pyvips.Image.new_from_file(os.path.join(svsFiles_dir, filename), access='sequential')
        # 获取文件名
        zoom_filename = filename.split('.')[0]
        # 存储到对应的目录下
        svs.dzsave(os.path.join(dst_dir, zoom_filename))
        print('{}.dzi is saved!'.format(zoom_filename))

# 遍历目标目录中的dzi文件
for filename in os.listdir(dst_dir):
    if filename.endswith('.dzi'):

        name, suffix = filename.split('.')
        if os.path.exists(os.path.join(dst_dir, name + '.html')):
            continue

        gen_html = re_test.GenerateHtmlFile(dst_dir, filename)
        gen_html.generate_html_data()
        print("{} is changed into a html file!".format(filename))

print('all finished!')