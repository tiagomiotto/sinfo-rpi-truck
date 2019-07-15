from componentClass import Component
import cv2
from flask import Flask, render_template, Response
import time

class Camera(Component):

    class VideoCamera():

        def __init__(self):
            # Start camera with opencv
            self.video = cv2.VideoCapture(0)

            #144p(256*144) gives roughly 30 fps
            self.video.set(3, 427)
            self.video.set(4, 240)

        def __del__(self):
            self.video.release()

        def change_res(self,width, height):
            self.video.set(3, width)
            self.video.set(4, height)

        def frame(self):
            # Get frame
            success, image = self.video.read()
            # Enconde to jpeg
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, jpeg = cv2.imencode('.jpg', image)
            # TODO check erroneous bits on image
            # TODO use a lower resolution for faster tranfers
            return jpeg.tobytes()

    class FlaskAppWrapper(object):
        """
        Wrapper for flask in order to comply with the standards stablished
        for Flask application formats
        """
        app = None

        # Wrapper for the enpoint function that 
        # executes the action and spits out code 200 if successful
        class EndpointAction(object):

            def __init__(self, action):
                self.action = action
                self.response = Response(status=200, headers={})

            def __call__(self, *args):
                self.action()
                return self.response

        def __init__(self, name):
            self.app = Flask(name)

        def run(self):
            self.app.run(host='0.0.0.0')

        def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
            self.app.add_url_rule(endpoint, endpoint_name,
                                  handler)

    def setup(self):
        self.video = self.VideoCamera()
        self.app = self.FlaskAppWrapper("myapp")
        self.app.add_endpoint(
            endpoint='/video', endpoint_name='video', handler=self.streamVideo)
        self.app.add_endpoint(
            endpoint='/', endpoint_name='', handler=self.index)

    def gen(self, camera):
        frames_per_sec =0
        while True:
            begin = time.time()
            frame = camera.frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            end = time.time()
            frames_per_sec = 1.0/(end-begin)
            print("Frames per sec", int(frames_per_sec))
        

    def streamVideo(self):
        return Response(self.gen(self.video),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def index(self):
        return "Hello there, access the video at /video"

    def run(self):
        self.setup()
        self.app.run()
