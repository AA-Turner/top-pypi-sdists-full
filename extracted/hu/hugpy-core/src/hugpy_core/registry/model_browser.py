"""Wrapper model-browser facts and live limits through Core's registered transport.

No Flask context, local model files, sizing logic or database credentials cross
this boundary. Settings writes continue through the confirmed pair command.
"""
from urllib.parse import urlencode

from .transport import request, target


def _read(worker_id, path, body=None):
    try:
        configured = target(worker_id)
    except ValueError as exc:
        return {'ok': False, 'error': str(exc)}, 404
    try:
        return request(configured, path, body)
    except (OSError, RuntimeError, ValueError) as exc:
        return {'ok': False, 'error': 'Worker model browser unavailable: ' + str(exc)}, 502


def catalog(worker_id):
    return _read(worker_id, '/v1/models')


def pair(worker_id, model_key=''):
    if not isinstance(model_key, str) or not model_key.strip():
        return {'ok': False, 'error': 'model_key is required'}, 400
    return _read(worker_id, '/v1/settings/pair?' + urlencode({'model_key': model_key}))


def limits(worker_id):
    return _read(worker_id, '/limits')


def report(worker_id, section=''):
    """Fixed Wrapper reports used by the shared terminal settings editor."""
    paths = {'residents': '/residents', 'health': '/health', 'runtime': '/v1/settings/runtime',
             'keys': '/v1/keys?all=1', 'schema': '/v1/settings/schema'}
    if section not in paths:
        return {'ok': False, 'error': 'Unknown settings report'}, 400
    return _read(worker_id, paths[section])


def set_limits(worker_id, changes=None):
    """Forward only supplied caps, then require the owning Wrapper's readback."""
    patch = changes
    allowed = {'gpu_limit', 'ram_limit', 'storage_limit', 'cpu_limit', 'protected'}
    if not isinstance(patch, dict) or not patch or set(patch) - allowed:
        return {'ok': False, 'error': 'Choose a live resource limit'}, 400
    try:
        configured = target(worker_id)
        receipt = request(configured, '/limits', patch)
        if not isinstance(receipt, dict) or receipt.get('error') or receipt.get('ok') is False:
            raise ValueError('Wrapper rejected the live limit')
        saved = request(configured, '/limits')
        from hugpy_settings.settings_delivery import agrees
        if any(not agrees(value, saved.get(key)) for key, value in patch.items()):
            raise ValueError('Wrapper readback differs for the live limit')
        return {**saved, 'source': 'wrapper'}
    except (OSError, RuntimeError, ValueError) as exc:
        return {'ok': False, 'error': 'Worker limit unconfirmed: ' + str(exc)}, 502


def preview(worker_id, model_key='', settings=None):
    if not isinstance(model_key, str) or not model_key.strip():
        return {'ok': False, 'error': 'model_key is required'}, 400
    if not isinstance(settings, dict) or set(settings) - {model_key}:
        return {'ok': False, 'error': 'settings must describe only the selected model'}, 400
    if any(not isinstance(value, dict) for value in settings.values()):
        return {'ok': False, 'error': 'model settings must be an object'}, 400
    # Preview computes a verdict at the owning Wrapper; it never saves settings
    # or submits an operator action and never loads a model.
    return _read(worker_id, '/v1/verdicts/plan', {'model_key': model_key, 'settings': settings})


def processes(worker_id):
    return _read(worker_id, '/v1/telemetry/processes')


def terminate_process(worker_id, pid=None, identity=None):
    if type(pid) is not int or pid <= 1 or not isinstance(identity, str) or not identity:
        return {'ok': False, 'error': 'PID and observed process identity are required'}, 400
    return _read(worker_id, '/v1/operator/terminate-process', {'pid': pid, 'identity': identity})


def browse_drives(worker_id, path='/', offset=0):
    return _read(worker_id, '/v1/drives/browse?' + urlencode({'path': path, 'offset': offset}))


def browse_central_drives(path='/', offset=0):
    from fitevict.serve.directory_browser import browse
    try:
        return browse(path, int(offset))
    except (OSError, ValueError) as exc:
        return {'ok': False, 'error': str(exc)}, 400
