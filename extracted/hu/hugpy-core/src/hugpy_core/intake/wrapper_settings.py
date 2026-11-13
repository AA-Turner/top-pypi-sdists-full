"""Wrapper settings are authoritative; Core stores only reported observations."""
from __future__ import annotations

import json
from psycopg.types.json import Jsonb


def apply_report(conn, worker, rows):
    """Mirror a complete pair-settings snapshot, including removed overrides.

    None means an older wrapper omitted the table: retain its last observation.
    An empty list means the wrapper explicitly reports no overrides.
    """
    if rows is None:
        return
    reported = {}
    for row in rows:
        key = row.get('model_key')
        if not key or key == '*':
            continue
        settings = row.get('settings') or {}
        if isinstance(settings, str):
            settings = json.loads(settings)
        if not isinstance(settings, dict):
            raise ValueError('wrapper pair settings must be an object')
        from hugpy_core.intake.schema import settings as canonical_settings
        reported[key] = (canonical_settings(settings), row.get('env_profile'))
    for key in reported:
        conn.execute('INSERT INTO model_workers(model_key,worker_id) VALUES (%s,%s) ON CONFLICT DO NOTHING', (key, worker))
    pairs = conn.execute('SELECT model_key,user_settings FROM model_workers WHERE worker_id=%s', (worker,)).fetchall()
    for pair in pairs:
        key = pair[0]
        settings, env = reported.get(key, ({}, None))
        # Activation progress and automatic routing exclusions are Core metadata,
        # not saved wrapper knobs. Keep them outside the observed knob replacement.
        metadata = {k: v for k, v in (pair[1] or {}).items() if k in ('activate', 'auto_blocked')}
        settings = {**metadata, **settings}
        conn.execute('UPDATE model_workers SET user_settings=%s,env_profile=%s,updated_at=now() '
                     'WHERE worker_id=%s AND model_key=%s '
                     'AND (user_settings,env_profile) IS DISTINCT FROM (%s::jsonb,%s::text)',
                     (Jsonb(settings), env, worker, key, Jsonb(settings), env))


# Core knob -> native wrapper option (POST /v1/models/options), and back. The
# native wrapper keeps one explicit choice per unit (placement/limits, bnb4,
# moe, goal, ctx, quant); every other legacy pair knob has no backing there.
_NATIVE_SET = {'alloc_mode': 'placement', 'bnb_4bit': 'bnb4', 'moe': 'moe', 'auto_goal': 'goal',
               'ctx': 'ctx', 'ctx_min': 'ctx_min', 'limit_gib': 'limit_gib', 'gguf_file': 'quant'}
_NATIVE_BACK = {'placement': 'alloc_mode', 'bnb4': 'bnb_4bit', 'moe': 'moe', 'goal': 'auto_goal',
                'ctx': 'ctx', 'ctx_min': 'ctx_min', 'limit_gib': 'limit_gib'}


def _native_worker(worker):
    """The live worker when its wrapper is the native build, else None."""
    from hugpy_core.registry import registry
    from hugpy_core.relay.relay import is_native
    live = registry.lookup_worker(worker if isinstance(worker, str) else worker.get('name') or worker.get('id'))
    return live if live and is_native(live) else None


def native_command(worker, key, sets, unset):
    """Deliver placement knobs to a native wrapper's options surface and read back."""
    from hugpy_core.registry.transport import request, target
    unknown = [k for k in sets if k not in _NATIVE_SET]
    if unknown:
        raise ValueError('this wrapper keeps only placement choices (' + ', '.join(sorted(_NATIVE_SET))
                         + '); it has no setting named: ' + ', '.join(sorted(unknown)))
    if unset and sets:
        raise ValueError('this wrapper keeps one choice per model: clear it (unset alone) or replace it, not both')
    configured = target(worker)
    body = {'model': key}
    if unset:
        body['clear'] = True
    body.update({_NATIVE_SET[k]: ('moe' if k == 'alloc_mode' and v == 'moe' else v)
                 for k, v in sets.items()})
    if body.get('placement') == 'moe':
        body.pop('placement')
        body.setdefault('moe', True)
    offered = request(configured, '/v1/models/options', body)
    chosen = offered.get('chosen') or {}
    settings = {_NATIVE_BACK[k]: v for k, v in chosen.items() if k in _NATIVE_BACK}
    quant = next((q.get('variation') for q in offered.get('quants') or [] if q.get('chosen')), None)
    if quant:
        settings['gguf_file'] = quant
    return {'settings': settings, 'source': 'wrapper',
            'confirmation': {'status': 'confirmed', 'requested': sets,
                             'cleared': bool(unset), 'actual': settings}}


def command(worker, key, sets, unset):
    """Send only edited keys, then read the wrapper's own confirmed state."""
    native = _native_worker(worker)
    if native is not None:
        return native_command(worker, key, sets, unset)
    from hugpy_settings.settings_delivery import command as deliver
    from hugpy_core.registry.transport import request, target
    configured = target(worker)
    patch = {**sets, **{name: None for name in unset}}
    return deliver(lambda path, body=None: request(configured, path, body),
                   patch, model=key, requested_by='fleet')


def box_command(worker, settings):
    native = _native_worker(worker)
    if native is not None:
        # The native wrapper's box-wide surface is the "*" options row.
        return native_command(worker, '*', settings, [])
    from hugpy_settings.settings_delivery import command as deliver
    from hugpy_core.registry.transport import request, target
    configured = target(worker)
    return deliver(lambda path, body=None: request(configured, path, body),
                   settings, requested_by='fleet')


def apply_confirmed_pair(conn, worker, key, settings):
    """Mirror one wrapper readback without clearing any other pair's settings."""
    if not isinstance(settings, dict):
        raise ValueError('wrapper pair settings must be an object')
    # Match apply_report's metadata preservation, but replace only this pair's
    # observed knobs. A command readback is not a complete worker snapshot.
    conn.execute(
        "UPDATE model_workers SET user_settings="
        "jsonb_strip_nulls(jsonb_build_object("
        "'activate',user_settings->'activate',"
        "'auto_blocked',user_settings->'auto_blocked')) || %s::jsonb,"
        "updated_at=now() WHERE worker_id=%s AND model_key=%s",
        (Jsonb(settings), worker, key))
