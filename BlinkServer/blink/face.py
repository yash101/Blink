import math
import dlib
import appdirs
import requests
import bz2
import cv2
import numpy as np
from scipy.spatial import distance as dist
from os import makedirs, path
from imutils import face_utils, resize
from imutils.video import VideoStream, FileVideoStream


# def dist(a, b):
#     return math.sqrt((a * a) + (b * b))

class Face:
    def __init__(self):
        self.model_path = self.get_shape_predictor_model()
        self.init_model()

    def get_shape_predictor_model(self):
        storage_path = appdirs.user_cache_dir(appname='BlinkServer', appauthor='yash101')
        try:
            makedirs(storage_path)
        except:
            pass

        self.model_path = path.join(storage_path, 'model.dat')

        if path.exists(self.model_path):
            return self.model_path
        
        print(f'Downloading face model to {self.model_path}...')

        with requests.get('http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2') as r, open(self.model_path, 'wb') as f:
            r.raise_for_status()
            decompressor = bz2.BZ2Decompressor()

            for chunk in r.iter_content(chunk_size=(1024 ** 2)):
                f.write(decompressor.decompress(chunk))
        
        return self.model_path
    
    def init_model(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.model_path)
        self.blinkThreshold = 0.0
        self.leftEye = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
        self.rightEye = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']


    # [inspired from pyimagesearch.com](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
    def calc_eye_aspect_ratio(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[4])

        return (A + B) / (2.0 * C)

    def start(self):
#        self.stream = VideoStream(src=0).start()
        self.stream = FileVideoStream('/home/yash/Projects/Blink/BlinkServer/test.mp4').start()
        filestream = True

        while not filestream or self.stream.more():
            frame = self.stream.read()
            resized = resize(frame, width=450)
            grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

            self.detect(grayscale)

    def detect(self, img):
        rects = self.detector(img, 0)

        for rect in rects:
            shape = self.predictor(img, rect)
            shape = face_utils.shape_to_np(shape)
            
            leftEye = shape[self.leftEye[0]:self.leftEye[1]]
            rightEye = shape[self.rightEye[0]:self.rightEye[1]]

            leftAspect = self.calc_eye_aspect_ratio(leftEye)
            rightAspect = self.calc_eye_aspect_ratio(rightEye)

            avgAspect = (leftAspect + rightAspect) / 2.0

            print(avgAspect, avgAspect < 0.3)

