#!/usr/bin/env python3
import rospy
import cv2
import mediapipe as mp
import time
import math
from std_msgs.msg import String

def main():
    rospy.init_node('hand_gesture_detection_node', anonymous=True)
    gesture_pub = rospy.Publisher('hand_gesture', String, queue_size=10)
    rate = rospy.Rate(30)  # 30Hz

    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(min_detection_confidence=0.9)
    mpDraw = mp.solutions.drawing_utils
    handlmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5, circle_radius=2)
    handConStyle = mpDraw.DrawingSpec(color=(255, 255, 255), thickness=5, circle_radius=2)
    pTime = 0

    init = 0
    direction_ = None

    x = y = z = 0
    rx = ry = rz = 0

    def counts(direction, count=10):
        nonlocal init, direction_
        if direction_ != direction:
            direction_ = direction
            init = 0
        else:
            init += 1
            if init >= count:
                return direction_
        return None

    def get_finger_state(handLms, handedness):
        tip_ids = [4, 8, 12, 16, 20]
        finger_states = []

        # Thumb
        if handedness == 'Right':
            finger_states.append(int(handLms.landmark[tip_ids[0]].x < handLms.landmark[tip_ids[0] - 2].x))
        else:
            finger_states.append(int(handLms.landmark[tip_ids[0]].x > handLms.landmark[tip_ids[0] - 2].x))

        # Other fingers
        for i in range(1, 5):
            finger_states.append(int(handLms.landmark[tip_ids[i]].y < handLms.landmark[tip_ids[i] - 2].y))

        return finger_states

    def get_hand_state(finger_states):
        if finger_states == [1, 1, 1, 1, 1]:
            return "OPEN"
        elif finger_states == [0, 0, 0, 0, 0]:
            return "FIST"
        elif finger_states == [0, 1, 1, 0, 0]:
            return "STOP"
        return None

    def get_y_translation_by_hand_size(handLms, imgWidth, imgHeight):
        x_coords = [lm.x for lm in handLms.landmark]
        y_coords = [lm.y for lm in handLms.landmark]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        hand_width = (max_x - min_x) * imgWidth
        hand_height = (max_y - min_y) * imgHeight

        size_threshold_min = 200
        size_threshold_max = 300

        if hand_width > size_threshold_max or hand_height > size_threshold_max:
            return 1
        elif hand_width < size_threshold_min and hand_height < size_threshold_min:
            return -1
        return 0

    while not rospy.is_shutdown():
        ret, img = cap.read()
        if not ret:
            continue

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        imgHeight, imgWidth = img.shape[:2]

        x = y = z = 0
        rx = ry = rz = 0

        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) >= 2:
            cv2.putText(img, "2hands", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if result.multi_hand_landmarks:
            for idx, handLms in enumerate(result.multi_hand_landmarks):
                handedness = result.multi_handedness[idx].classification[0].label
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handlmsStyle, handConStyle)

                finger_states = get_finger_state(handLms, handedness)
                hand_state = get_hand_state(finger_states)

                # ===== 优先处理旋转手势 =====
                if finger_states[1] == 1 and finger_states[2] == 1 and finger_states[3] == 1 and finger_states[4] == 0:
                    rz = 3  # 顺时针旋转
                elif finger_states == [0, 1, 1, 1, 1]:  # 除拇指外四指
                    rz = -3  # 逆时针旋转
                else:
                    # ========== 移动方向判断 ==========
                    if hand_state is None:
                        x1 = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].x
                        y1 = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].y
                        x2 = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_PIP].x
                        y2 = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_PIP].y

                        if x2 - x1 != 0:
                            angle = math.atan((y2 - y1) / (x2 - x1)) * 180 / math.pi
                        else:
                            angle = 90 if y2 > y1 else -90

                        if (angle > 45 or angle < -45) and y1 > y2:
                            direction = "UP"
                        elif (angle > 45 or angle < -45) and y1 < y2:
                            direction = "DOWN"
                        elif (-45 < angle < 45) and x1 < x2:
                            direction = "RIGHT"
                        elif (-45 < angle < 45) and x1 > x2:
                            direction = "LEFT"
                        else:
                            direction = "NONE"

                        if direction == counts(direction):
                            hand_state = direction

                    # 移动控制
                    if hand_state == "UP":
                        z = 1
                    elif hand_state == "DOWN":
                        z = -1
                    elif hand_state == "LEFT":
                        y = -1
                    elif hand_state == "RIGHT":
                        y = 1
                    elif hand_state == "OPEN":
                        x = get_y_translation_by_hand_size(handLms, imgWidth, imgHeight)
                    elif hand_state in ["FIST", "STOP", "NONE"]:
                        x = y = z = 0

                # 发布话题
                gesture_pub.publish(f"{x} {y} {z} {rx} {ry} {rz}")

                wrist = handLms.landmark[0]
                cx, cy = int(wrist.x * imgWidth), int(wrist.y * imgHeight)
                cv2.putText(img, f"{hand_state} ({x},{y},{z})", (cx - 100, cy - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(img, f"rx:{rx} ry:{ry} rz:{rz}", (cx - 100, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.putText(img, handedness, (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
        pTime = cTime
        cv2.putText(img, f"fps:{int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('img', img)

        if cv2.waitKey(1) == ord('b'):
            break

        rate.sleep()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
