import io
import time
import numpy as np
from picamera import PiCamera

class PiCam:
    def __init__(self, framerate=25, width=640, height=480):
        self.size = (width, height)
        self.framerate = framerate

        self.camera = PiCamera()
        self.camera.resolution = self.size
        self.camera.framerate = self.framerate

    def snapshot(self): # jpg 사진 한 장을 리턴
        frame = io.BytesIO()
        self.camera.capture(frame, 'jpeg', use_video_port=True)
        frame.seek(0)
        return frame.getvalue()
        # truncate 안한 이유 : frame이 지역 변수라서

class MJpegStreamCam(PiCam):
    def __init__(self, framerate=25, width=640, height=480):
        super().__init__(framerate=framerate, width=width, height=height)

    # 이터레이터
    def __iter__(self):
        frame = io.BytesIO()
        while True:
            self.camera.capture(frame, format="jpeg", use_video_port=True)
            image = frame.getvalue()

            # Mjpeg 용 HTTP 메시지
            # 여기서 b는 바이트 배열로 표현하라
            yield (b'--myboundary\n'
                    b'Content-Type:image/jpeg\n'
                    b'Content-Length: ' + f"{len(image)}".encode() + b'\n'
                    b'\n' + image + b'\n')
            frame.seek(0)
            frame.truncate()
            # time.sleep(1/self.framerate)