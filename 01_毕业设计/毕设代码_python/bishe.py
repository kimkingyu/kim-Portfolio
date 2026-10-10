import time
import numpy
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarkerOptions, HandLandmarkerResult
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

# Default index is 0.
# If you have more than 1 camera, please do a test to determine the index
DEVICE_ID = 0# 0,1,2,3
# Please check your camera fps
FPS = 30
# Please check your camera resolutions
# Higher resolution may cause performance issue
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

class HandGestureCapture:
    def __init__(self):
        self.init_video()


    def init_video(self):
        self.capture = cv2.VideoCapture(DEVICE_ID, cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FPS, FPS)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)


        def run(self):
            while True:
                ret, frame = self.capture.read()
                if ret:
                    frame_as_numpy_array = numpy.asarray(frame)
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_as_numpy_array)
                    self.hand_detector.detect_async(mp_image, self.get_cur_time())

                    if self.hand_result:
                        frame = self.draw_landmarks_on_image(frame, self.hand_result)

                    cv2.imshow('frame', frame)
                    key = cv2.waitKey(1)
                    if key == 27:
                        break
            self.exit()

            def exit(self):
                self.capture.release()
                cv2.destroyAllWindows()
