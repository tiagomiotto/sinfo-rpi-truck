from componentClass import Component
import cv2
from flask import Flask, render_template, Response


class Camera(Component):

    class VideoCamera():

        def __init__(self):
            # Start camera with opencv
            self.video = cv2.VideoCapture(0)

        def frame(self):
            # Get frame
            success, image = self.video.read()
            # Enconde to jpeg
            ret, jpeg = cv2.imencode('.jpg', image)
            cv2.imshow('image',image)
            cv2.waitKey(0)
            return jpeg.tobytes()



    class FlaskAppWrapper(object):
        """
        Wrapper for flask in order to comply with the standards stablished
        for Flask application formats
        """
        app = None
        
        # Wrapper for the enpoint function that spits out code 200 if successful 
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
                                  self.EndpointAction(handler))

                        

    def setup(self):
        self.video = self.VideoCamera()
        self.app = self.FlaskAppWrapper("myapp")
        self.app.add_endpoint("/","/",handler=self.streamVideo)

    def gen(self,camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def streamVideo(self):
        return Response(self.gen(self.video),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    def run(self):
        self.setup()
        self.app.run()