from flask import Flask, render_template
import click
from .api import api


@click.command()
@click.option('--fps', '-f', default=15, help='Refresh frame rate.')
@click.option('--camera', '-c', default='fake', help='Camera driver to use. Valid options are "fake", "pi". (default is "fake")')
@click.option('--debug/--no-debug', '-d/', default=False, help='Enable or disable debug mode (default is disabled).')
def run_app(fps, camera, debug):
    """Campy is a webcam server accessible through a REST API."""
    app = Flask(__name__)
    app.config['CAMERA'] = camera
    app.config['FPS'] = fps
    app.register_blueprint(api)

    @app.route('/')
    def index():
        return render_template('index.html', camera=app.config['CAMERA'])

    app.run(host='0.0.0.0', threaded=True, debug=debug)
    return 0
