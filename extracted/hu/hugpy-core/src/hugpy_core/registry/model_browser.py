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


def model_preferences(worker_id, model_key='', settings=None):
    """Read/write the SQL Wrapper preferences with an independent owner readback."""
    if not isinstance(model_key, str) or not model_key:
        return {'ok': False, 'error': 'model_key is required'}, 400
    if settings is not None and not isinstance(settings, dict):
        return {'ok': False, 'error': 'settings must be an object'}, 400
    try:
        configured = target(worker_id)
        path = '/v1/model-settings?' + urlencode({'model': model_key})
        if settings is not None:
            receipt = request(configured, '/v1/model-settings', {'model': model_key, 'settings': settings})
            if not isinstance(receipt, dict) or receipt.get('error'):
                raise ValueError('Wrapper refused model preferences')
        saved = request(configured, path)
        if settings is not None and saved != receipt:
            raise ValueError('Wrapper preferences changed before readback; refresh and retry')
        return {**saved, 'source': 'wrapper'}
    except (OSError, RuntimeError, ValueError) as exc:
        return {'ok': False, 'error': str(exc)}, 502


# The Wrapper's own configuration (hugpy-wrapper 0.1.183, migrations 0057-0060): what a
# model is to that device (attributions), where every layer goes (placements), the
# evict-to-fit decisions and the stored decision queries. Core relays reads as they are;
# a write is answered only after the owning Wrapper's readback carries it.
DECLARED_SOURCES = ('operator', 'auto', 'core')


def _query(path, **params):
    query = {key: value for key, value in params.items() if value not in (None, '')}
    return path + ('?' + urlencode(query) if query else '')


def attributions(worker_id, model_key='', model_uid='', device=''):
    """What a model is to the worker's device: declared and derived rows from the Wrapper's own store."""
    if not (model_key or model_uid):
        return {'ok': False, 'error': 'model_key or model_uid is required'}, 400
    return _read(worker_id, _query('/v1/attributions', model_key=model_key, model_uid=model_uid, device=device))


def declare_attribution(worker_id, model_key='', model_uid='', attribute='', value=None, unit_id='',
                        device='', source='', basis=None, retract=False):
    """Declare (or retract) one attribute of a model on the worker's device, then require the
    Wrapper's readback to carry the declaration (or no longer carry the retracted one)."""
    if not (model_key or model_uid):
        return {'ok': False, 'error': 'model_key or model_uid is required'}, 400
    if not isinstance(attribute, str) or not attribute.strip():
        return {'ok': False, 'error': 'attribute is required'}, 400
    if source and source not in DECLARED_SOURCES:
        return {'ok': False, 'error': 'source is one of operator, auto, core'}, 400
    if basis is not None and not isinstance(basis, dict):
        return {'ok': False, 'error': 'basis must be an object'}, 400
    attribute, source = attribute.strip(), source or 'operator'
    body = {'attribute': attribute, 'value': value, 'retract': bool(retract), 'source': source}
    body.update({key: item for key, item in (('model_key', model_key), ('model_uid', model_uid), ('unit_id', unit_id),
                                             ('device', device), ('basis', basis)) if item})
    try:
        configured = target(worker_id)
        receipt = request(configured, '/v1/attributions', body)
        if not isinstance(receipt, dict) or receipt.get('error') or receipt.get('ok') is False:
            raise ValueError('Wrapper refused the attribution')
        identity = receipt.get('model_uid') or model_uid
        saved = request(configured, _query('/v1/attributions', model_uid=identity, model_key='' if identity else model_key))
        if not isinstance(saved, dict) or saved.get('error'):
            raise ValueError('Wrapper attributions could not be read back')
        scope = device or receipt.get('device') or saved.get('device')
        rows = [row for row in saved.get('attributions') or []
                if row.get('attribute') == attribute and row.get('source') == source
                and (row.get('unit_id') or '') == (unit_id or '') and row.get('device') == scope]
        from hugpy_settings.settings_delivery import agrees
        if retract and rows:
            raise ValueError('Wrapper readback still carries the retracted attribution')
        if not retract and not any(agrees(value, row.get('value')) for row in rows):
            raise ValueError('Wrapper readback differs for the attribution')
        return {'ok': True, 'source': 'wrapper', 'worker': saved.get('worker'), 'device': scope,
                'model_uid': saved.get('model_uid'), 'declaration': receipt, 'readback': rows}
    except (OSError, RuntimeError, ValueError) as exc:
        return {'ok': False, 'error': 'Worker attribution unconfirmed: ' + str(exc)}, 502


def derive_attributions(worker_id):
    """Materialize every derived attribute on the worker from its stored query."""
    return _read(worker_id, '/v1/attributions/derive', {})


def layer_placements(worker_id, model_key='', unit_id='', representation='', context='', gpu_resource=''):
    """The sorted fill of a weights unit on the worker: every layer component, its bytes, fill rank and tier."""
    if not (model_key or unit_id):
        return {'ok': False, 'error': 'model_key or unit_id is required'}, 400
    return _read(worker_id, _query('/v1/placements/layers', model_key=model_key, unit_id=unit_id,
                                   representation=representation, context=context, gpu_resource=gpu_resource))


def pin_layers(worker_id, model_key='', unit_id='', layer_tiers=None, representation='', context_tokens=None,
               gpu_resource='', source=''):
    """Pin layer components to tiers (a declared attribution on the worker), then require the
    re-planned fill to carry every pin; a null tier clears a pin and is not verified."""
    if not (model_key or unit_id):
        return {'ok': False, 'error': 'model_key or unit_id is required'}, 400
    if not isinstance(layer_tiers, dict) or not layer_tiers:
        return {'ok': False, 'error': 'layer_tiers must name at least one layer'}, 400
    for components in layer_tiers.values():
        if components is not None and (not isinstance(components, dict) or any(
                not isinstance(component, str) or (tier is not None and not isinstance(tier, str))
                for component, tier in components.items())):
            return {'ok': False, 'error': 'layer_tiers maps a layer to {component: tier}'}, 400
    if source and source not in DECLARED_SOURCES:
        return {'ok': False, 'error': 'source is one of operator, auto, core'}, 400
    body = {'layer_tiers': layer_tiers}
    body.update({key: item for key, item in (('model_key', model_key), ('unit_id', unit_id), ('representation', representation),
                                             ('context_tokens', context_tokens), ('gpu_resource', gpu_resource), ('source', source)) if item})
    try:
        configured = target(worker_id)
        plan = request(configured, '/v1/placements/layers', body)
        if not isinstance(plan, dict) or plan.get('error') or not isinstance(plan.get('layers'), list):
            raise ValueError('Wrapper refused the layer pins')
        placed = {(row.get('layer_key'), row.get('component')): row for row in plan['layers']}
        for layer, components in layer_tiers.items():
            for component, tier in (components or {}).items():
                if tier is None:
                    continue
                keys = [key for key in placed if key[1] == component and (layer == '*' or key[0] == layer)]
                if not keys and layer != '*':
                    raise ValueError(f'the plan has no {component} component for {layer}')
                for key in keys:
                    row = placed[key]
                    if row.get('tier_source') != 'declared:layer_tiers' or (layer != '*' and row.get('tier') != tier):
                        raise ValueError(f'the re-planned fill does not carry the pin for {key[0]} {component}')
        return {**plan, 'source': 'wrapper'}
    except (OSError, RuntimeError, ValueError) as exc:
        return {'ok': False, 'error': 'Worker layer pins unconfirmed: ' + str(exc)}, 502


def eviction_decisions(worker_id, limit=''):
    """The worker's evict-to-fit decisions, newest first: snapshot, victims, spared and blocking keys."""
    return _read(worker_id, _query('/v1/evictions/decisions', limit=limit))


def stored_queries(worker_id, limit=''):
    """The worker's stored decision queries with their parameters, and its recent execution receipts."""
    return _read(worker_id, _query('/v1/sql/queries', limit=limit))


def run_query(worker_id, name='', params=None):
    """Run one stored decision query on the worker, over its store with Discovery attached read-only."""
    if not isinstance(name, str) or not name.strip():
        return {'ok': False, 'error': 'name is required'}, 400
    if params is not None and not isinstance(params, dict):
        return {'ok': False, 'error': 'params must be an object'}, 400
    return _read(worker_id, '/v1/sql/query', {'name': name.strip(), 'params': params or {}})
