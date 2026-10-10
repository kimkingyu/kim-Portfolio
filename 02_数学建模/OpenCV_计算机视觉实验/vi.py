"""工业六轴机械臂原点复位与运动学轨迹校准脚本."""

import time
from wlkata_mirobot_Virtual import Virtual_WlkataMirobot

# ----------------- 预设空间位姿姿态配置 -----------------
# 抓取预备位与工件抓取位
POSE_PICK_ABOVE = [-72, 9.4, 10.2, 0, -19.7, 0.2]
POSE_PICK = [-72, 14.9, 15.6, 0, -30.4, 0.2]

# 工位 4 ~ 1 的码垛位姿
POSE_PLACE_4_ABOVE = [-25.5, 8.5, 10.8, -0.1, -18.3, 3.4]
POSE_PLACE_4 = [-25.5, 13.7, 16.2, -0.1, -28.9, 3.3]
POSE_PLACE_3_ABOVE = [-6.5, -2.5, 21.5, 0.3, -18, -15.5]
POSE_PLACE_3 = [-6.5, 4.3, 28, 0.3, -31.3, -15.5]
POSE_PLACE_2_ABOVE = [13.9, 0.2, 19.6, 0.6, -19, -35.9]
POSE_PLACE_2 = [13.9, 6.2, 25.4, 0.7, -30.8, -35.8]
POSE_PLACE_1_ABOVE = [31.4, 16.2, 3.5, 0.9, -19.1, -53.3]
POSE_PLACE_1 = [31.4, 20.6, 8, 0.9, -27.9, -53.2]

# 数字量 I/O 通道定义
IO_SUCTION_CUP = 0
IO_CYLINDER = 1

# 控制器实例连接
arm = Virtual_WlkataMirobot(server_IP="192.168.10.101", server_port=5478)

# 六轴硬件机械原点复位 (Homing Sequence)
arm.home(com1=True)

# 关节运动学测试：移动至安全过渡位与预备抓取位
arm.set_joint_angle(com1_P=POSE_PLACE_4_ABOVE)
arm.set_joint_angle(com1_P=POSE_PICK_ABOVE)
