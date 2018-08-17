import pyvips
import numpy as np

# a = pyvips.Image.new_from_array([[1, 2], [3, 4]])
# b = pyvips.Image.new_from_array([[3, 2], [5, 1]])
#
# print(type(a))
#
# for i in dir(a):
#     if not i.startswith('_'):
#         print(i)

image = pyvips.Image.new_from_file('b.jpg')
print(image.get_fields())
print(image.get('jpeg-multiscan'))
print(image.get('jpeg-chroma-subsample'))

# new_image = image.copy(xres=100, yres=13)
min_value = image.min()
min_value, opts = image.min(x=True, y=True)
x_pos = opts['x']
y_pos = opts['y']
print(min_value)
print(x_pos)
print(y_pos)

# result_image = image.linear(1, 3)
# print(result_image)
# result_image = image.linear(12.4, 13.9)
# print(result_image)
# result_image = image.linear([1, 2, 3], [4, 5, 6])
# print(result_image)
# result_image = image.linear(1, [4, 5, 6])
# print(result_image)

result_iamge = image.ifthenelse([0, 255, 0], [255, 0, 0])
print(result_iamge)
