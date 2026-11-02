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


def command(worker, key, sets, unset):
    """Send only edited keys, then read the wrapper's own confirmed state."""
    from hugpy_settings.settings_delivery import command as deliver
    from hugpy_core.registry.transport import request, target
    configured = target(worker)
    patch = {**sets, **{name: None for name in unset}}
    return deliver(lambda path, body=None: request(configured, path, body),
                   patch, model=key, requested_by='fleet')


def box_command(worker, settings):
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
