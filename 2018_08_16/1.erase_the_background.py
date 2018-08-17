import openslide
import numpy as np
import cv2
import scipy.misc

slide = openslide.open_slide('../8602.svs')

dimension = slide.level_dimensions[1]
downsample = [i for i in range(len(slide.level_dimensions))][1]

downsample_img = np.array(slide.read_region((0, 0), 1, (21912, 5696)))

n, m, z = downsample_img.shape

bw = np.zeros((n, m))
print(n, m, z)

for i in range(n):
    for j in range(m):
        if downsample_img[i, j, 0] > 130 and (((int(downsample_img[i, j, 0]) - int(downsample_img[i, j, 1])) > 30) or ((
                int(downsample_img[i, j, 0]) - int(downsample_img[i, j, 2])) > 30)):
            bw[i, j] = 1

img_Blur = cv2.blur(bw, (100, 100), cv2.BORDER_REPLICATE)

result = img_Blur.copy()
result[result > 0.4] = 1
result[result <= 0.4] = 0

bw3 = np.zeros((n, m, z), dtype=np.uint8)
bw3[:, :, 0] = result
bw3[:, :, 1] = result
bw3[:, :, 2] = result
bw3[:, :, 3] = 1
BackRemImg = bw3 * downsample_img

scipy.misc.imsave('backRem.tif', BackRemImg)
