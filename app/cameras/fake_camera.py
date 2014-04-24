"""A fake camera that loops through a sequence of pictures."""
import os
from ..base_camera import BaseCamera

class Camera(BaseCamera):
    def __init__(self):
        basedir = os.path.dirname(os.path.abspath(__file__))
        filenames = [os.path.join(basedir, 'fake/muybridge%02d.jpg') % n for n in range(15)]
        self.frames = [open(f, 'rb').read() for f in filenames]
        self.n = len(self.frames)
        self.frame = 0

    def get_current_frame(self):
        self.frame += 1
        if self.frame >= self.n:
            self.frame = 0
        return self.frames[self.frame]
