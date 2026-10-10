"""基础几何图元绘制与文本标注模块."""

import cv2
import numpy as np

# 创建纯黑背景画板 (300x300, 3通道)
image = np.zeros((300, 300, 3), dtype=np.uint8)

# 绘制线段 (起点, 终点, BGR颜色, 线宽)
cv2.line(image, (100, 200), (200, 200), (255, 0, 0), 5)

# 绘制矩形边界框 (左上角, 右下角, BGR颜色, 线宽)
cv2.rectangle(image, (30, 100), (60, 150), (0, 255, 0), 5)

# 绘制圆形 (圆心坐标, 半径, BGR颜色, 线宽)
cv2.circle(image, (150, 200), 20, (0, 0, 255), 3)

# 渲染文字标注
cv2.putText(image, "Visual Detection Demo", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# 显示绘制结果
cv2.imshow('Primitive Drawing', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
