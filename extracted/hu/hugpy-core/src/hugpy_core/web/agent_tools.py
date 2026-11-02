"""Authenticated Core relay to its existing toolserver; upstream credentials never leave Core."""
from abstract_flask import get_bp, register_categories, spec
from flask import request, jsonify
from hugpy_core.router.observability import store as routing
from hugpy_core.config import settings

agent_tools_bp, logger = get_bp('agent_tools_bp', __name__)


def relay(operation):
    # Toolserver access includes host files and privileged tools. A mere inference
    # use key must never inherit Core's operator identity. Reuse the management gate.
    class RequestView:
        client_address = (request.remote_addr or '', 0)
        headers = request.headers
        request = request.environ.get("werkzeug.socket")
    denied = routing.KEYS.check(RequestView(), 'admin')
    if denied:
        status, body = denied
        return jsonify(body), status
    body = request.get_json(silent=True)
    if body is None:
        body = {}
    if not isinstance(body, dict):
        return jsonify({'error': 'Expected a JSON object'}), 400
    if not settings.TOOLSERVER_TOKEN:
        return jsonify({'error': 'Core toolserver is not configured'}), 503
    if operation == 'call' and (not isinstance(body.get('name'), str) or not isinstance(body.get('arguments', {}), dict)):
        return jsonify({'error': 'name and object arguments are required'}), 400
    status, result = settings._ts('/ts/' + operation, body, operator=True,
                                  timeout=120 if operation == 'call' else 8)
    return jsonify(result), status


# The relay is a genuine raw-request proxy (it reads the caller's address and
# headers to re-check the management gate, then forwards the raw body), so each
# toolserver operation is a thin named adapter and the spec keeps ``inputs="path"``.
def ts_categories():
    return relay('categories')


def ts_list():
    return relay('list')


def ts_call():
    return relay('call')


# Dict nesting is the path: ``/ts/{categories,list,call}``.
ALL_CATEGORIES = {"ts": {
    "categories": spec(ts_categories, "POST", response="native", inputs="path"),
    "list": spec(ts_list, "POST", response="native", inputs="path"),
    "call": spec(ts_call, "POST", response="native", inputs="path"),
}}
register_categories(agent_tools_bp, ALL_CATEGORIES)
