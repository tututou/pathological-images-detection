import re
import os


class GenerateHtmlFile(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, dst_dir, filename):
        self.dst_dir = dst_dir
        self.filename = filename

    def read_dzi_data(self):
        info_list = list()
        info_dict = dict()

        with open(os.path.join(self.dst_dir, self.filename)) as f:
            content = f.read()

        xmlns = re.search(r'xmlns=[^ \n]*', content).group()
        Format = re.search(r'Format=[^ \n]*', content).group()
        Overlap = re.search(r'Overlap=[^ \n]*', content).group()
        TileSize = re.search(r'TileSize=[^ \n]*', content).group()
        Height = re.search(r'Height=[^ \n]*', content).group()
        Width = re.search(r'Width=[^ \n]*', content).group()

        info_list.append(xmlns)
        info_list.append(Format)
        info_list.append(Overlap)
        info_list.append(TileSize)
        info_list.append(Height)
        info_list.append(Width)

        for each in info_list:
            key, value = each.split('=')
            info_dict[key] = eval(value)

        return info_dict

    def generate_html_data(self):

        info_dict = self.read_dzi_data()
        name, suffix = self.filename.split('.')

        # 读取html模板
        with open('dzsave.html') as f:
            html = f.read()

        html = re.sub(r'OpenSeadragon_Demo0', name + '.svs', html)
        html = re.sub(r"'http://schemas.microsoft.com/deepzoom/2008'", '"%s"' % info_dict['xmlns'], html)
        html = re.sub(r"'./dzsave_files/'", '"{}"'.format('./' + name + '_files/'), html)
        html = re.sub(r"'1'", '"{}"'.format(info_dict['Overlap']), html)
        html = re.sub(r"'254'", '"{}"'.format(info_dict['TileSize']), html)
        html = re.sub(r"'jpeg'", '"{}"'.format(info_dict['Format']), html)
        html = re.sub(r"'22787'", '"{}"'.format(info_dict['Height']), html)
        html = re.sub(r"'87648'", '"{}"'.format(info_dict['Width']), html)

        # 修改dzi文件的内容
        with open(os.path.join(self.dst_dir, self.filename), 'w') as f:
            f.write(html)
        # 讲dzi文件重命名为html文件
        os.rename(os.path.join(self.dst_dir, self.filename), os.path.join(self.dst_dir, name + '.html'))

