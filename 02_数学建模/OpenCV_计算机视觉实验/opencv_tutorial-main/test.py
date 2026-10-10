"""OpenCV 图像基础读取与属性分析模块."""

import cv2

# 输出 OpenCV 版本信息
print(f"OpenCV Version: {cv2.__version__}")

# 读取图像数据
image = cv2.imread('opencv_logo.jpg')

# 打印图像空间尺寸及色彩通道 (Height, Width, Channels)
print(f"Image Dimensions: {image.shape}")

# 渲染窗口并展示图像
cv2.imshow('Image Display', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
