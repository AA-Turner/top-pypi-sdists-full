import os
from pathlib import Path
import logging
from flask import Flask, request, jsonify

from ghostcoder import FileRepository
from ghostcoder.runtime.api import APIRuntime

app = Flask(__name__)

# Configure logging
logger = logging.getLogger(__name__)
logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)
logging.getLogger('ghostcoder').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.INFO)
logging.getLogger('openai').setLevel(logging.INFO)
logging.getLogger('httpcore').setLevel(logging.INFO)

# Configuration and initialization
repo_dir = os.environ.get('REPO_DIR', '/home/albert/repos/albert/bulletproof-react')
model_name = os.environ.get('MODEL_NAME', 'gpt-4-1106-preview')
debug_mode = os.environ.get('DEBUG_MODE', 'True') == 'True'

repository = FileRepository(repo_path=Path(repo_dir),
                            exclude_dirs=["benchmark", "playground", "tests", "results"])
runtime = APIRuntime(repository=repository, debug_mode=debug_mode, url="https://2310-84-246-89-56.ngrok-free.app")

# Flask routes
@app.route('/api/<function_name>', methods=['POST'])
def write_code(function_name):
    logger.info(f"Running function {function_name}.")
    request_data = request.json
    response = runtime.run_function(function_name, request_data)
    return response.json()

@app.route('/api/openapi.json', methods=['GET'])
def get_open_api_endpoint():
    return jsonify(runtime.schema())

# Middleware for logging request headers
@app.before_request
def log_request_headers():
    logging.info(f"Request headers: {request.headers}")

if __name__ == "__main__":
    app.run(debug=True)