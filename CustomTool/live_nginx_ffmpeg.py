"""
ffmpeg + nginx + video，rtsp转rtmp播放

测试不通，暂时废弃
主要问题：不能将rtmp服务搭建起来，用p = subprocess.Popen(self.command, stdin=subprocess.PIPE)时候无法启动ffmpeg
        怀疑可能是启动的电脑摄像头，而不是rtsp流（网络摄像头）
"""

import queue
import threading
import cv2 as cv
import subprocess


class Live(object):
    def __init__(self):
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        self.rtmpUrl = "rtmp://127.0.0.1:1654/live/home"
        self.camera_path = 0

    def read_frame(self):
        print("开启推流")
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        # Get video information
        fps = int(cap.get(cv.CAP_PROP_FPS))
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # ffmpeg command
        self.command = ['cmd', '/c', 'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24', '-s',
                        "{}x{}".format(width, height), '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt',
                        'yuv420p', '-preset', 'ultrafast', '-f', 'flv',

                        self.rtmpUrl]

        # read webcamera
        while (cap.isOpened()):
            ret, frame = cap.read()

            if not ret:
                print("Opening camera is failed")
                cap = cv.VideoCapture(self.camera_path)
                # continue

            # put frame into queue
            self.frame_queue.put(frame)

    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = subprocess.Popen(self.command, stdin=subprocess.PIPE)
                break

        while True:
            if self.frame_queue.empty() != True:
                frame = self.frame_queue.get()
                # process frame
                # 你处理图片的代码
                # write to pipe
                p.stdin.write(frame.tostring())

    def run(self):
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,))
        ]
        [thread.setDaemon(True) for thread in threads]
        [thread.start() for thread in threads]