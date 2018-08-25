import openslide
import numpy as np
import scipy.signal as signal
import scipy.io as sio
import cv2
from multiprocessing import Pool
import os

# slide = openslide.open_slide('../pathological_images_storage_and_display/svs/8602.svs')
#
#
# dimension = slide.level_dimensions[1]
# downsample = int(slide.level_downsamples[1])
#
# downsample_img = np.array(slide.read_region((0, 0), 1, (21912, 5696)))
#
# n, m, z = downsample_img.shape
#
# bw = np.zeros((n, m))
# print(n, m, z)
# print(downsample_img[5695, 21911, 3])
#
# pool = Pool(5)
# for i in range(n):
#     for j in range(m):
#         if downsample_img[i, j, 0] > 130 and (((int(downsample_img[i, j, 0]) - int(downsample_img[i, j, 1])) > 30) or ((
#                 int(downsample_img[i, j, 0]) - int(downsample_img[i, j, 2])) > 30)):
#             bw[i, j] = 1
#
# img_Blur = cv2.blur(bw, (100, 100), cv2.BORDER_REPLICATE)
# print(img_Blur.shape)
# print(bw.shape)
# data = sio.loadmat('h.mat')
# print(data['h'].shape)
# res = data['h'] == img_Blur
# print(np.all(res))

class Operation(object):
    def __init__(self):
        self.slide = openslide.open_slide('../pathological_images_storage_and_display/svs/8602.svs')

    def read(self):
        self.img = np.array(self.slide.read_region((0, 0), int(self.slide.level_downsamples[1]), self.slide.level_dimensions[1]))
        n, m, z = self.img.shape
        self.bw = np.zeros((n, m))

        pool = Pool(5)
        for i in range(n):
            for j in range(m):
                self.change(i, j)
                pool.apply_async(self.change, (i, j))
        pool.close()
        pool.join()

    def change(self, i, j):
        # print(os.getpid())
        if self.img[i, j, 0] > 130 and (
                ((int(self.img[i, j, 0]) - int(self.img[i, j, 1])) > 30) or
                ((int(self.img[i, j, 0]) - int(self.img[i, j, 2])) > 30)):
            self.bw[i, j] = 1
        print(i,j)


op = Operation()
op.read()