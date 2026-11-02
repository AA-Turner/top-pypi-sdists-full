"""Durable chat submissions, protected by the existing /v1 API key gate."""
from flask import Blueprint, jsonify, request
from hugpy_core.relay import inference_requests as jobs

inference_bp = Blueprint('inference', __name__)


@inference_bp.post('/v1/inference/requests')
def submit():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({'error': 'a JSON object is required'}), 400
    model = body.get('model') or body.get('model_key')
    if not isinstance(model, str) or not model.strip():
        return jsonify({'error': 'model is required'}), 400
    if not isinstance(body.get('messages'), list) or not body['messages']:
        return jsonify({'error': 'messages must be a non-empty list'}), 400
    request_id = jobs.submit('chat', body)
    return jsonify({'request_id': request_id, 'ticket': request_id, 'pending': True,
                    'state': 'pending'}), 202


@inference_bp.get('/v1/inference/requests/<request_id>')
def status(request_id):
    body, code = jobs.ticket(request_id, kind='chat')
    return jsonify(body), code


@inference_bp.get('/v1/inference/requests/<request_id>/stream')
def stream(request_id):
    return jobs.stream(request_id, kind='chat')
