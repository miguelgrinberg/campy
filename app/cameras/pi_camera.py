"""The Raspberry Pi camera module."""
import io
import time
import threading
import picamera
from ..base_camera import BaseCamera


class Frame(object):
    def __init__(self):
        self.stream = io.BytesIO()
        self.frame = None


class Camera(BaseCamera):
    def __init__(self):
        self.resolution = (640, 480)
        self.quality = 5

        self.frames = [Frame() for i in range(10)]
        self.current_stream = 0
        self.next_stream = 0
        self.last_accessed = time.time()
        self.thread = None

    def start(self):
        """Start the camera's background thread."""
        if self.thread is not None and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        while self.get_current_frame() is None:
            time.sleep(0.1)

    def get_current_frame(self):
        """Return the current frame from the camera."""
        self.last_accessed = time.time()
        return self.frames[self.current_stream].frame

    def _streams(self):
        """Generator that provides frames from a ring buffer,
        used by the camera's capture_sequence() method."""
        while True:
            # If there are no clients reading frames then stop.
            if time.time() - self.last_accessed > 10:
                return
 
            # store the next frame from the camera
            stream = self.frames[self.next_stream].stream
            if stream.tell() > 0:
                stream.seek(0)
                self.frames[self.next_stream].frame = stream.read()
                self.current_stream = self.next_stream

            # return the next entry in the ring buffer for the
            # following frame
            self.next_stream = self.current_stream + 1
            if self.next_stream >= len(self.frames):
                self.next_stream = 0
            stream = self.frames[self.next_stream].stream
            stream.seek(0)
            stream.truncate()
            yield stream
        
    def _run(self):
        """Background thread that grabs frame from the camera."""
        with picamera.PiCamera() as camera:
            camera.resolution = self.resolution
            camera.capture_sequence(self._streams(), 'jpeg', use_video_port=True,
                                    quality=self.quality)
