#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander, roscpp_initialize
import tf

class PandaVelocityController:
    def __init__(self):
        roscpp_initialize([])
        rospy.init_node('panda_velocity_controller', anonymous=True)

        self.group = MoveGroupCommander("panda_arm")
        self.group.set_max_velocity_scaling_factor(0.1)
        self.group.set_max_acceleration_scaling_factor(0.1)
        self.group.set_planning_time(5.0)

        # 初始化目标姿态
        rospy.sleep(1.0)  # 确保 MoveIt 状态准备好
        self.target_pose = self.group.get_current_pose().pose

        # 用于缓存上一次收到的速度指令
        self.last_command = None

        rospy.Subscriber('hand_gesture', String, self.velocity_callback)

    def velocity_callback(self, msg):
        try:
            raw_data = msg.data.strip()
            if raw_data == self.last_command:
                return  # 指令未变，不执行

            self.last_command = raw_data  # 更新缓存

            data = list(map(float, raw_data.split()))
            if len(data) != 6:
                rospy.logwarn("Invalid data: %s", raw_data)
                return

            vx, vy, vz, rx, ry, rz = data
            dt = 0.03  # 移动保持原速
            rotation_scale = 3.0  # 转动放大 3 倍

            # 更新目标位置
            self.target_pose.position.x += vx * dt
            self.target_pose.position.y += vy * dt
            self.target_pose.position.z += vz * dt

            # 当前四元数
            q_orig = [
                self.target_pose.orientation.x,
                self.target_pose.orientation.y,
                self.target_pose.orientation.z,
                self.target_pose.orientation.w
            ]

            # 增量旋转（放大角度）
            q_delta = tf.transformations.quaternion_from_euler(
                rx * dt * rotation_scale,
                ry * dt * rotation_scale,
                rz * dt * rotation_scale
            )
            q_result = tf.transformations.quaternion_multiply(q_delta, q_orig)

            self.target_pose.orientation.x = q_result[0]
            self.target_pose.orientation.y = q_result[1]
            self.target_pose.orientation.z = q_result[2]
            self.target_pose.orientation.w = q_result[3]

            # 执行运动
            self.group.clear_pose_targets()
            self.group.set_pose_target(self.target_pose)
            success = self.group.go(wait=True)

            if not success:
                rospy.logwarn("Motion planning failed.")

        except Exception as e:
            rospy.logerr("Velocity command failed: %s", str(e))

    def run(self):
        rospy.spin()

if __name__ == "__main__":
    try:
        controller = PandaVelocityController()
        controller.run()
    except rospy.ROSInterruptException:
        pass


