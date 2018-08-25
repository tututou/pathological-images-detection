import openslide
import numpy as np
import scipy.misc
import scipy.io
import cv2
import os


def RemoveHeadEnd(OriImg):
    n, m, z = OriImg.shape
    i = 0
    while np.sum(OriImg[i, :, :]) == 0:
        i += 1
    h = i
    j = n - 1
    while np.sum(OriImg[j, :, :]) == 0:
        j -= 1
    e = j
    return h, e


if not os.path.exists('./SegPic'):
    os.mkdir('./SegPic')
svsFiles_dir = '/home/frodo/Desktop/work/job content/相关附件/相关附件/'
filenames = os.listdir(svsFiles_dir)


def get_result(img):
    bw = np.where(np.logical_and(img[:, :, 0] > 130, np.logical_or(img[:, :, 0] - img[:, :, 1] > 30,
                                                                   img[:, :, 0] - img[:, :, 2] > 30)), 1, 0)
    bw = bw.astype(dtype=np.float32)
    img_Blur = cv2.blur(bw, (100, 100), cv2.BORDER_REPLICATE)
    result = img_Blur
    result[result > 0.4] = 1
    result[result <= 0.4] = 0
    return result


for imgname in filenames:
    ySite_list, xSite_list = [], []
    imgname = '8602.svs'
    slide = openslide.open_slide(svsFiles_dir + imgname)
    # 获得要切片的图像大小
    size = slide.level_dimensions[1]
    # 获得对应图像大小下的缩放倍率
    level = int(slide.level_downsamples[1])
    # print(size)
    img = np.array(slide.read_region((0, 0), 1, size), dtype=np.float16)
    n, m, z = img.shape

    # 获得重要的信息点
    result = get_result(img)
    # 生成一个mask，并给mask的每一通道赋予相同的result值
    bw3 = np.zeros((n, m, z - 1))
    for i in range(z-1):
        bw3[:, :, i] = result
    # 获得去除背景后的图片
    BackRemImg = bw3 * img[:, :, :-1]

    # 生成（1,m）的数组，为图片的宽（x轴）
    PatchSegMark = np.zeros((1, m))
    # 如果图片的每一单位像素的行的值的总和不为0,说明有切片单元，值设为1；反之，说明没有切片单元，则该位置值设为0
    for i in range(m):
        if np.sum(result[:, i]):
            PatchSegMark[0, i] = 1
        else:
            PatchSegMark[0, i] = 0
    # 对相邻的值做差离值，若值为1（1-0）或者-1（0-1），说明这是切片单元的边界处
    PatchSegPos = np.diff(PatchSegMark, n=1)
    # 值为1代表切片单元的起始边界
    PatchSegPosStart = np.where(PatchSegPos == 1)[1]
    # 值为-1代表切片单元的结束边界
    PatchSegPosEnd = np.where(PatchSegPos == -1)[1]
    # 获得起始边界和结束边界的个数
    StartNum = len(PatchSegPosStart)
    EndNum = len(PatchSegPosEnd)

    if not os.path.exists('./SegPic/' + imgname):
        os.mkdir('./SegPic/' + imgname)
    if PatchSegPosStart[0] > PatchSegPosEnd[0]:         # 代表先出现切片单元
        patch = BackRemImg[:, :PatchSegPosEnd[0], :]    # 第一张图片在0～第一个切片单元的结束边界选取
        h, e = RemoveHeadEnd(patch)                     # 获得每个切片单元的上下边界
        xSite_list.append((0, PatchSegPosEnd[0] - 1))
        ySite_list.append((h, e))

        if StartNum < EndNum:
            for i in range(StartNum):
                patch = BackRemImg[:, PatchSegPosStart[i]:PatchSegPosEnd[i + 1], :]
                h, e = RemoveHeadEnd(patch)
                xSite_list.append((PatchSegPosStart[i], PatchSegPosEnd[i + 1] - 1))
                ySite_list.append((h, e))
        else:
            for i in range(StartNum - 1):
                patch = BackRemImg[:, PatchSegPosStart[i]:PatchSegPosEnd[i + 1], :]
                h, e = RemoveHeadEnd(patch)
                xSite_list.append((PatchSegPosStart[i], PatchSegPosEnd[i + 1] - 1))
                ySite_list.append((h, e))

            patch = BackRemImg[:, PatchSegPosStart[StartNum - 1]:m, :]
            h, e = RemoveHeadEnd(patch)
            xSite_list.append((PatchSegPosStart[StartNum - 1], m - 1))
            ySite_list.append((h, e))

    else:
        if StartNum > EndNum:
            for i in range(StartNum - 1):
                patch = BackRemImg[:, PatchSegPosStart[i]:PatchSegPosEnd[i], :]
                h, e = RemoveHeadEnd(patch)
                xSite_list.append((PatchSegPosStart[i], PatchSegPosEnd[i] - 1))
                ySite_list.append((h, e))
            patch = BackRemImg[:, PatchSegPosStart[StartNum - 1]:m, :]
            h, e = RemoveHeadEnd(patch)
            xSite_list.append((PatchSegPosStart[StartNum - 1], m - 1))
            ySite_list.append((h, e))
        else:
            for i in range(StartNum):
                patch = BackRemImg[:, PatchSegPosStart[i]:PatchSegPosEnd[i], :]
                h, e = RemoveHeadEnd(patch)
                xSite_list.append((PatchSegPosStart[i], PatchSegPosEnd[i] - 1))
                ySite_list.append((h, e))

    print(imgname, ' started!')
    for each in zip(xSite_list, ySite_list):
        size = ((each[0][1] - each[0][0]) * level, (each[1][1] - each[1][0]) * level)
        loc = (each[0][0] * level, each[1][0] * level)
        img = np.array(slide.read_region(loc, 0, size), dtype=np.float16)

        scipy.misc.imsave('切片单元.tif', img)
        # n, m, z = img.shape
        #
        # result = get_result(img)
        #
        # bw3 = np.zeros((n, m, z))
        # for i in range(z):
        #     bw3[:, :, i] = result
        #     if i == 3:
        #         bw3[:, :, i] = 1
        # BackRemImg = bw3 * img
        # BackRemImg = BackRemImg.astype(dtype=np.uint8)
        # print('before saving----')
        # scipy.misc.imsave('SegPic/' + imgname + '/' + str(i) + '.jpg', BackRemImg[:, :, :-1])
        # scipy.io.savemat('SegPic/' + imgname + '/' + str(i) + '.mat', {'BackRemImg': BackRemImg})
        break
    print(imgname, ' finished! \n')
    break
