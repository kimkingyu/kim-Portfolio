"""计算机视觉实验环境与模块诊断入口."""

import sys


def system_diagnostic():
    """检查并输出当前运行环境与核心模块配置."""
    print("=" * 50)
    print("OpenCV 计算机视觉实验套件 - 系统环境检测")
    print(f"Python 解释器版本: {sys.version.split()[0]}")
    print("实验子模块: chap2 (基础语法与IO), chap3 (数据结构与运算符)")
    print("=" * 50)


if __name__ == '__main__':
    system_diagnostic()
