import time
from flask import Blueprint, Response, url_for, jsonify, current_app
from .cameras import get_camera_list, get_camera

api = Blueprint('api', __name__)


@api.route('/cameras/')
def get_cameras():
    """Return the list of available cameras."""
    cameras = get_camera_list()
    for i in range(len(cameras)):
        cameras[i]['stream'] = url_for('api.get_stream', camera=cameras[i]['name'])
        cameras[i]['configuration'] = url_for('api.get_configuration', camera=cameras[i]['name'])
    return jsonify({'cameras': cameras})


@api.route('/cameras/<camera>/stream')
def get_stream(camera):
    """Return the MJPEG stream for a camera."""
    return Response(get_camera(camera).stream(current_app.config['FPS']),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@api.route('/cameras/<camera>/configuration')
def get_configuration(camera):
    """Return the current configuration for a camera."""
    return jsonify(get_camera(camera).get_configuration())


@api.route('/cameras/<camera>/configuration', methods=['PUT', 'PATCH'])
def set_configuration(camera):
    """Apply configuration changes to the camera."""
    get_camera(camera).set_configuration(request.json)
    return jsonify({})
