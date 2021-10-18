import cv2
from threading import Thread
from datetime import datetime as dt

class Threaded_Webcam:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.ret, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            self.ret, self.frame = self.stream.read()
            #self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
