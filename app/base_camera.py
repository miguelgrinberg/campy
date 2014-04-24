import time
from flask import current_app


class BaseCamera(object):
    def start(self):
        """Start the camera."""
        pass

    def get_current_frame(self):
        """Return the current frame from the camera."""
        raise NotImplementedError('camera drivers must implement get_current_frame()')

    def stream(self, fps):
        """Generator that returns the MJPEG stream from a camera."""
        interval = 1.0 / fps
        while True:
            now = time.time()
            frame = self.get_current_frame()
            yield b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: ' + \
                  str(len(frame)).encode() + b'\r\n\r\n' + frame + b'\r\n'
            remaining = interval - (time.time() - now)
            if remaining > 0:
                time.sleep(interval - (time.time() - now))

    def get_configuration(self):
        """Return the current camera configuration."""
        return {}

    def set_configuration(self, configuration):
        """Apply configuration changes."""
        raise NotImplementedError('camera drivers must implement set_configuration()')

