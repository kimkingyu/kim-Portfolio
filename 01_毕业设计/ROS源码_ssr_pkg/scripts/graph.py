#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
import matplotlib.pyplot as plt
import csv
import os
import numpy as np

poses = []  # 每一项：[time, x, y, z, qx, qy, qz, qw, j1, j2, ..., j7]
latest_joints = None  # 缓存最新的关节角度数据

def pose_callback(msg):
    global latest_joints
    timestamp = msg.header.stamp.to_sec()
    pos = msg.pose.position
    ori = msg.pose.orientation

    if latest_joints is None or len(latest_joints) < 7:
        rospy.logwarn_throttle(5, "Waiting for joint states...")
        return

    # 记录末端位姿 + 关节角度
    poses.append([
        timestamp,
        pos.x, pos.y, pos.z,
        ori.x, ori.y, ori.z, ori.w,
        *latest_joints[:7]  # 取前7个关节
    ])
    rospy.loginfo_throttle(1.0, f"Recording pose at t={timestamp:.2f}")

def joint_callback(msg):
    global latest_joints
    latest_joints = msg.position

def save_and_plot():
    if not poses:
        rospy.logwarn("No pose data recorded. Nothing to save.")
        return

    save_dir = os.path.expanduser("~/pose_logs")
    os.makedirs(save_dir, exist_ok=True)

    # 保存 CSV
    csv_path = os.path.join(save_dir, "pose_joint_record.csv")
    with open(csv_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Time", "Pos_X", "Pos_Y", "Pos_Z", 
                         "Ori_X", "Ori_Y", "Ori_Z", "Ori_W",
                         "Joint_1", "Joint_2", "Joint_3", "Joint_4", "Joint_5", "Joint_6", "Joint_7"])
        writer.writerows(poses)
    rospy.loginfo(f"Saved pose & joint data to: {csv_path}")

    # 绘制末端位置图
    poses_np = np.array(poses)
    times = poses_np[:, 0] - poses_np[0, 0]  # 相对时间

    plt.figure()
    plt.plot(times, poses_np[:, 1], label='X')
    plt.plot(times, poses_np[:, 2], label='Y')
    plt.plot(times, poses_np[:, 3], label='Z')
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("End Effector Position Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_dir, "ee_position_plot.png"))

    # 可选：绘制关节角图
    plt.figure()
    for i in range(7):
        plt.plot(times, poses_np[:, 8 + i], label=f'Joint {i+1}')
    plt.xlabel("Time (s)")
    plt.ylabel("Joint Angle (rad)")
    plt.title("Joint Angles Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_dir, "joint_angle_plot.png"))

    rospy.loginfo("Saved plots and data.")

def main():
    rospy.init_node("ee_pose_joint_recorder", anonymous=True)
    rospy.Subscriber("/ee_pose", PoseStamped, pose_callback)
    rospy.Subscriber("/joint_states", JointState, joint_callback)
    rospy.on_shutdown(save_and_plot)
    rospy.loginfo("Recording started. Press Ctrl+C to stop.")
    rospy.spin()

if __name__ == '__main__':
    main()
