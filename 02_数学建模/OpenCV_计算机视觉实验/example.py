"""系统环境与时间基准诊断脚本."""

import os
import time

# 打印当前系统工作路径与执行时间戳
current_dir = os.path.dirname(os.path.abspath(__file__))
timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"[{timestamp}] System Initialized at: {current_dir}")
