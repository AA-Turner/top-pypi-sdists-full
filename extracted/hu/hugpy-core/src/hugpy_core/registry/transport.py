"""Internal client for registered Wrappers; independent of Flask and toolserver.

Core services use the registration store for endpoints and credentials. Only
the owning Wrapper executes commands; database observations never become writes.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


def target(worker):
    """Resolve a worker reference against Core's durable registration store."""
    from hugpy_core.registry import registrations
    name = worker if isinstance(worker, str) else worker.get('name') or worker.get('id')
    configured = registrations.get(name) if name else None
    if configured is not None:
        return configured
    if isinstance(worker, dict) and worker.get('url'):
        return worker
    raise ValueError(f'Unknown worker: {name}')


def headers(worker, extra=None):
    """Resolve credentials only for the endpoint they belong to."""
    result = dict(extra or {})
    key = worker.get('key')
    if not key:
        name = worker.get('name') or worker.get('id')
        if name:
            from hugpy_core.registry import registrations
            configured = registrations.get(name)
            if configured and configured.get('url', '').rstrip('/') == worker.get('url', '').rstrip('/'):
                key = configured.get('key')
        # Compatibility for installations still using the folded router key.
        key = key or os.environ.get('HUGPY_CORE_ROUTER_KEY', '').strip()
    if key:
        result['Authorization'] = 'Bearer ' + key
    return result


def request(worker, path, body=None, *, timeout=30, method=None):
    """Exchange JSON with a Wrapper without passing through Core's own API."""
    if not path.startswith('/') or path.startswith('//'):
        raise ValueError('Wrapper request requires a relative absolute path')
    req = urllib.request.Request(
        worker['url'].rstrip('/') + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers=headers(worker, {'Content-Type': 'application/json'}), method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read(2000).decode(errors='replace')
        raise RuntimeError(f'Worker HTTP {exc.code}: {detail}') from exc
