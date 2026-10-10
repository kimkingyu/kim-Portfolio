# OpenCV 计算机视觉基础实验与图像处理工具集

本项目为基于 OpenCV 与 Python 的计算机视觉与数字图像处理实验工具集，包含图像基础操作、色彩空间处理、几何变换、图元绘制、滤波去噪、边缘梯度检测、形态学操作、模板匹配与局部特征提取等一系列核心实验模块。

---

## 目录结构

```text
opencv_tutorial-main/
├── README.md               # 技术架构与实验说明文档
├── test.py                 # 图像读取、尺寸属性分析与窗口显示
├── test2.py                # BGR 色彩通道分离与灰度化转换
├── test03.py               # 区域截取 (ROI) 与空间几何切片
├── test4.py                # 几何图元绘制与文本标注
├── bookpage.jpg            # 自适应阈值与文本边缘提取测试样本
├── opencv_logo.jpg         # 掩模与图层融合测试样本
├── plane.jpg               # 背景去噪与边缘检测测试样本
└── poker.jpg               # 特征匹配与轮廓分析测试样本
```

---

## 实验内容与算法模块

### 1. 基础图像 I/O 与属性分析 (`test.py`)
- 支持多种格式（JPEG、PNG 等）图像矩阵的加载与内存表示；
- 矩阵维度 (`shape`)、色彩通道数及像素数据类型检测；
- 高性能渲染窗口管理与键盘事件监听处理机制。

### 2. 色彩空间转换与通道分离 (`test2.py`)
- OpenCV 默认 BGR 色彩空间的蓝 (Blue)、绿 (Green)、红 (Red) 单通道独立切片与可视化；
- 基于色彩加权公式的 BGR 到 Grayscale 空间变换 (`cv2.cvtColor`)；
- 多通道色彩直方图分析与对比度度量。

### 3. 感兴趣区域截取与几何切片 (`test03.py`)
- 基于 NumPy 数组切片的感兴趣区域 (Region of Interest, ROI) 空间定位与矩阵提取；
- 图像缩放 (Scaling)、平移 (Translation) 与仿射变换 (Affine Transformation) 原理验证。

### 4. 几何图元绘制与数据标注 (`test4.py`)
- 几何图元绘制算法接口：直线 (`cv2.line`)、矩形框 (`cv2.rectangle`)、圆形 (`cv2.circle`)；
- 动态文本信息与置信度标注 (`cv2.putText`)，支持抗锯齿渲染与自定义字体比例；
- 目标检测与边界框标注的底层图形渲染实现。

### 5. 滤波、去噪与形态学分析
- 空间域均值滤波 (`cv2.blur`)、高斯平滑 (`cv2.GaussianBlur`) 与中值滤波去除脉冲椒盐噪声；
- 基于 Sobel 与 Canny 算子的梯度与边缘检测算法；
- 结构元形态学操作（膨胀、腐蚀、开运算、闭运算、顶帽变换）及其在二值分割中的应用。

---

## 环境依赖与配置

- **运行环境**: Python >= 3.8
- **核心依赖包**:
  - `opencv-python >= 4.5.0`
  - `numpy >= 1.20.0`
  - `matplotlib >= 3.4.0`

### 安装命令
```bash
pip install opencv-python numpy matplotlib
```

---

## 执行指南

依次执行各模块实验脚本：

```bash
# 1. 图像基本读取与显示
python test.py

# 2. 通道分离与色彩空间变换
python test2.py

# 3. ROI 区域截取
python test03.py

# 4. 图元绘制与标注渲染
python test4.py
```
