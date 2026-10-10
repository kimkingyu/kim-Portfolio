"""感兴趣区域 (ROI) 切片与几何裁剪模块."""

import cv2

# 读取样本图像
image = cv2.imread('opencv_logo.jpg')

# 提取目标 ROI 区域 (y: 10~170, x: 40~200)
crop = image[10:170, 40:200]

# 显示裁剪区域
cv2.imshow('ROI Crop Result', crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
