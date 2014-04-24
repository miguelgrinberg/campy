import os
import glob
from importlib import import_module

_cameras = {}


def get_camera_list():
    """Obtain the list of available camera drivers."""
    cameras = []
    modules = glob.glob(os.path.join(os.path.dirname(__file__), '*_camera.py'))
    for module in modules:
        m = import_module('.' + os.path.basename(module)[:-3], __name__)
        cameras.append({'name': os.path.basename(module)[:-10], 'description': m.__doc__}) 
    return cameras


def get_camera(name, *args, **kwargs):
    """Return a camera by name and optional arguments.
    If multiple clients request the same camera the same object is returned."""
    global _cameras
    args_str = ','.join([str(x) for x in args])
    kwargs_str = ','.join(['{0}={1}'.format(x, y) for x, y in kwargs.items()])
    full_name = name + '/' + args_str + '/' + kwargs_str
    if full_name not in _cameras:
        mod = import_module('.{0}_camera'.format(name), __name__)
        _cameras[full_name] = mod.Camera(*args, **kwargs)
    _cameras[full_name].start()
    return _cameras[full_name]
