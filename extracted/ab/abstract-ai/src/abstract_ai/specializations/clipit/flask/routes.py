from abstract_flask import jsonify,get_bp,request,abort,Flask,CORS,send_from_directory
import pyperclip
clipit_bp,logger = get_bp('routes', __name__)

def is_local_request():
    """Allow only localhost (IPv4 or IPv6)."""
    remote = request.remote_addr
    return remote in ('127.0.0.1', '::1')

@clipit_bp.route('/', methods=['GET'])
def index():
    # Will be overridden by flask_app, but define here if needed
    abort(404)

@clipit_bp.route('/copy', methods=['POST'])
def copy_route():
    # Reject any callers not from localhost
    if not is_local_request():
        abort(403)

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    try:
        pyperclip.copy(data['text'])
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
