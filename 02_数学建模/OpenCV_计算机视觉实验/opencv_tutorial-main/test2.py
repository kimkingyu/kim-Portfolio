"""BGR 色彩通道分离与灰度化处理模块."""

import cv2

# 读取样本图像
image = cv2.imread('opencv_logo.jpg')

# BGR 通道分离显示 (Blue, Green, Red)
cv2.imshow('Blue Channel', image[:, :, 0])
cv2.imshow('Green Channel', image[:, :, 1])
cv2.imshow('Red Channel', image[:, :, 2])

# 转换为灰度单通道图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale Image', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
