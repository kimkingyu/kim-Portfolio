"""工业六轴机械臂视觉引导与物料分拣自动化控制脚本.

本脚本通过 Socket / Modbus 与工业六轴机器人通信，实现基于光电传感与
视觉预定位的多工位自动化抓取与码垛控制流程。
"""

import time
from wlkata_mirobot_Virtual import Virtual_WlkataMirobot

# ----------------- 关节坐标姿态定义 (J1 ~ J6, 单位: 度) -----------------
# 抓取预备位（上方安全过渡点）
POSE_PICK_ABOVE = [-72, 9.4, 10.2, 0, -19.7, 0.2]
# 工件抓取位点
POSE_PICK = [-72, 14.9, 15.6, 0, -30.4, 0.2]

# 工位 4 放置上方过渡位与目标放置位
POSE_PLACE_4_ABOVE = [-25.5, 8.5, 10.8, -0.1, -18.3, 3.4]
POSE_PLACE_4 = [-25.5, 13.7, 16.2, -0.1, -28.9, 3.3]

# 工位 3 放置上方过渡位与目标放置位
POSE_PLACE_3_ABOVE = [-6.5, -2.5, 21.5, 0.3, -18, -15.5]
POSE_PLACE_3 = [-6.5, 4.3, 28, 0.3, -31.3, -15.5]

# 工位 2 放置上方过渡位与目标放置位
POSE_PLACE_2_ABOVE = [13.9, 0.2, 19.6, 0.6, -19, -35.9]
POSE_PLACE_2 = [13.9, 6.2, 25.4, 0.7, -30.8, -35.8]

# 工位 1 放置上方过渡位与目标放置位
POSE_PLACE_1_ABOVE = [31.4, 16.2, 3.5, 0.9, -19.1, -53.3]
POSE_PLACE_1 = [31.4, 20.6, 8, 0.9, -27.9, -53.2]

# ----------------- 数字量 I/O 通道映射 -----------------
IO_SUCTION_CUP = 0      # 真空吸盘控制通道
IO_CYLINDER = 1         # 气动推杆控制通道
SENSOR_PHOTOELECTRIC = 4 # 光电物料到位检测传感器输入通道

# ----------------- 控制器连接与初始化 -----------------
sort_count = 0
arm = Virtual_WlkataMirobot(server_IP="172.20.10.6", server_port=5478)

# 机械臂初始就绪位点
arm.set_joint_angle(com1_P=POSE_PLACE_4_ABOVE)
arm.set_Output(IO_SUCTION_CUP, 0)
arm.set_Output(IO_CYLINDER, 0)
time.sleep(1)

start_time = time.time()
end_time = time.time()

# ----------------- 自动化分拣主循环 -----------------
while True:
    time.sleep(1)
    object_detected = arm.get_Input(SENSOR_PHOTOELECTRIC)

    if object_detected == 1:
        start_time = time.time()
        arm.set_Single_modbusValues(301, 1)

        # 复位气动推料机构
        arm.set_Output(IO_CYLINDER, 0)

        # 运动至抓取预备位与物料抓取位
        arm.set_joint_angle(com1_P=POSE_PICK_ABOVE, speed=5000)
        arm.set_joint_angle(com1_P=POSE_PICK, speed=5000)

        # 启动真空吸附装置
        arm.set_Output(IO_SUCTION_CUP, 1)
        time.sleep(1)  # 保持负压建立延时
        arm.set_joint_angle(com1_P=POSE_PICK_ABOVE, speed=5000)

        # 目标工位 1 码垛放置
        if sort_count == 0:
            arm.set_Single_modbusValues(301, 2)
            arm.set_joint_angle(com1_P=POSE_PLACE_1_ABOVE, speed=5000)
            arm.set_joint_angle(com1_P=POSE_PLACE_1, speed=5000)
            arm.set_Output(IO_SUCTION_CUP, 0)
            time.sleep(1)
            arm.set_joint_angle(com1_P=POSE_PLACE_1_ABOVE, speed=5000)
            sort_count += 1
            arm.set_Single_modbusValues(300, sort_count)
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            arm.set_Single_modbusValues(302, elapsed_time)

        # 目标工位 2 码垛放置
        elif sort_count == 1:
            arm.set_Single_modbusValues(301, 3)
            arm.set_joint_angle(com1_P=POSE_PLACE_2_ABOVE, speed=5000)
            arm.set_joint_angle(com1_P=POSE_PLACE_2, speed=5000)
            arm.set_Output(IO_SUCTION_CUP, 0)
            time.sleep(1)
            arm.set_joint_angle(com1_P=POSE_PLACE_2_ABOVE, speed=5000)
            sort_count += 1
            arm.set_Single_modbusValues(300, sort_count)
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            arm.set_Single_modbusValues(303, elapsed_time)

        # 目标工位 3 码垛放置
        elif sort_count == 2:
            arm.set_Single_modbusValues(301, 4)
            arm.set_joint_angle(com1_P=POSE_PLACE_3_ABOVE, speed=5000)
            arm.set_joint_angle(com1_P=POSE_PLACE_3, speed=5000)
            arm.set_Output(IO_SUCTION_CUP, 0)
            time.sleep(1)
            arm.set_joint_angle(com1_P=POSE_PLACE_3_ABOVE, speed=5000)
            sort_count += 1
            arm.set_Single_modbusValues(300, sort_count)
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            arm.set_Single_modbusValues(304, elapsed_time)

        # 目标工位 4 码垛放置并完成批次任务
        elif sort_count == 3:
            arm.set_Single_modbusValues(301, 5)
            arm.set_joint_angle(com1_P=POSE_PLACE_4_ABOVE, speed=5000)
            arm.set_joint_angle(com1_P=POSE_PLACE_4, speed=5000)
            arm.set_Output(IO_SUCTION_CUP, 0)
            time.sleep(1)
            arm.set_joint_angle(com1_P=POSE_PLACE_4_ABOVE, speed=5000)
            sort_count += 1
            arm.set_Single_modbusValues(300, sort_count)
            arm.set_Single_modbusValues(301, 0)
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            arm.set_Single_modbusValues(305, elapsed_time)
            break

    else:
        # 未检测到物料，驱动气动推料机构上料
        arm.set_Output(IO_CYLINDER, 1)
        time.sleep(2)
        arm.set_Output(IO_CYLINDER, 0)
