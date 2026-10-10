#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander, roscpp_initialize

def main():
    roscpp_initialize([])
    rospy.init_node("ee_pose_publisher", anonymous=True)

    group = MoveGroupCommander("panda_arm")
    pub = rospy.Publisher("/ee_pose", PoseStamped, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    rospy.loginfo("Publishing current end-effector pose to /ee_pose...")
    while not rospy.is_shutdown():
        pose_msg = PoseStamped()
        pose_msg.header.stamp = rospy.Time.now()
        pose_msg.header.frame_id = "panda_link0"  # 或 base_link，视你使用的机器人模型而定
        pose_msg.pose = group.get_current_pose().pose
        pub.publish(pose_msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
