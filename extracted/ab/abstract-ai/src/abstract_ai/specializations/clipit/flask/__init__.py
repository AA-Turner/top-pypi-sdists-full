from .routes import Flask,clipit_bp,jsonify,get_bp,request,abort,send_from_directory,CORS
import os
def get_abs_dir():
    return os.path.abspath(__file__)
def get_directory():
    abs_path = get_abs_dir()
    abs_dir = os.path.dirname(abs_path)
    return abs_dir
def get_html_dir():
    abs_dir = get_directory()
    html_dir = os.path.join(abs_dir,'html')
    return html_dir
def abstract_clip_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprint
    app.register_blueprint(clipit_bp)

    # Serve the HTML at “/” if localhost, else 403
    @app.route('/', methods=['GET'])
    def index():
        remote = request.remote_addr
        if remote not in ('127.0.0.1', '::1'):
            abort(403)

        return send_from_directory(get_html_dir(), 'drop-n-copy.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found'}, 404

    @app.errorhandler(403)
    def forbidden(e):
        return {'error': 'Forbidden'}, 403

    return app
