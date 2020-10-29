import math

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

class Face:
    def __init__(self):
        pass

    # [inspired from pyimagesearch.com](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
    def calc_eye_aspect_ratio(self, eye):
        A = dist(eye[1], eye[5])
        B = dist(eye[2], eye[4])
        C = dist(eye[0], eye[4])

        return (A + B) / (2.0 * C)

