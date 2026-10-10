import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarkerOptions, HandLandmarkerResult
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.9)
mpDraw = mp.solutions.drawing_utils
handlmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5, circle_radius=2)
handConStyle = mpDraw.DrawingSpec(color=(255, 255, 255), thickness=5, circle_radius=2)
pTime = 0
cTime = 0

# 定义阈值，用于判断方向的偏移程度
THRESHOLD = 0.05

def get_finger_state(handLms):
    """ 计算每根手指是否张开 """
    tip_ids = [4, 8, 12, 16, 20]  # 指尖关键点索引
    finger_states = []

    # 拇指：比较 x 轴（左手是小于，右手是大于）
    if handLms.landmark[tip_ids[0]].x > handLms.landmark[tip_ids[0] - 2].x:
        finger_states.append(1)  # 张开
    else:
        finger_states.append(0)  # 握拳

    # 其余四根手指：比较 y 轴（指尖在指根上方）
    for i in range(1, 5):
        if handLms.landmark[tip_ids[i]].y < handLms.landmark[tip_ids[i] - 2].y:
            finger_states.append(1)  # 张开
        else:
            finger_states.append(0)  # 握拳

    return finger_states

def get_thumb_direction(handLms, label):
    """ 判断大拇指的方向 """
    tip_id = 4
    base_id = 2
    wrist_id = 0  # 手腕关键点索引
    thumb_tip = handLms.landmark[tip_id]
    thumb_base = handLms.landmark[base_id]
    wrist = handLms.landmark[wrist_id]

    # 计算 x 和 y 方向的差值
    dx = thumb_tip.x - thumb_base.x
    dy = thumb_tip.y - thumb_base.y

    # 当大拇指位置比较高时，判定为 up
    if thumb_tip.y < wrist.y:
        return "Up"
    elif thumb_tip.y > wrist.y:
        return "Down"

    if label == "Left":
        if abs(dx) > abs(dy) and abs(dx) > THRESHOLD:
            if dx > 0:
                return "Right"
            else:
                return "Left"
        else:
            return None
    else:
        if abs(dx) > abs(dy) and abs(dx) > THRESHOLD:
            if dx > 0:
                return "Left"
            else:
                return "Right"
        else:
            return None

def get_hand_state(finger_states, thumb_direction):
    """ 根据手指状态和大拇指方向判断整体手势 """
    if finger_states == [1, 1, 1, 1, 1]:
        return "Open"
    elif finger_states == [0, 0, 0, 0, 0]:
        return "Fist"
    elif finger_states == [1, 0, 0, 0, 0] and thumb_direction:
        return f"Thumb {thumb_direction}"
    else:
        return "Other"

while True:
    ret, img = cap.read()
    if ret:
        # 水平翻转图像
        img = cv2.flip(img, 1)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        imgHeight, imgWidth = img.shape[:2]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handlmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    xPos = round(lm.x, 2)
                    yPos = round(lm.y, 2)
                    zPos = round(lm.z, 2)
                    xrPos = int(lm.x * imgWidth)
                    yrPos = int(lm.y * imgHeight)
                    cv2.putText(img, str(i), (xrPos - 25, yrPos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
                    print(i, xPos, yPos, zPos)

        if result.multi_handedness:
            for idx, handedness in enumerate(result.multi_handedness):
                label = handedness.classification[0].label  # 获取左手或右手
                handLms = result.multi_hand_landmarks[idx]  # 获取对应的手部关键点
                first_lm = handLms.landmark[0]  # 选取一个参考点
                cx, cy = int(first_lm.x * imgWidth), int(first_lm.y * imgHeight)
                cv2.putText(img, label, (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # 获取手指状态
                finger_states = get_finger_state(handLms)

                # 获取大拇指方向
                thumb_direction = get_thumb_direction(handLms, label)

                # 获取手的状态
                hand_state = get_hand_state(finger_states, thumb_direction)

                # 计算文本显示位置（手腕 landmark[0]）
                wrist = handLms.landmark[0]
                cx, cy = int(wrist.x * imgWidth), int(wrist.y * imgHeight)

                text = f"{hand_state}"
                cv2.putText(img, text, (cx - 100, cy - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"fps:{int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('b'):
        break