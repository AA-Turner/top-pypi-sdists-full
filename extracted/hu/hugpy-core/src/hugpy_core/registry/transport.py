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


def health(worker, timeout=5):
    """A Wrapper's /health document, also when it answers 503: a degraded Wrapper (its catalog stale, Discovery
    not built yet on a fresh box) still says who it is and what is wrong, and is still a worker to keep polling
    (2026-11-14: a 503 here failed Core's whole poll of that worker, and connect refused it)."""
    req = urllib.request.Request(worker['url'].rstrip('/') + '/health', headers=headers(worker, {'Accept': 'application/json'}))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 503:
            try:
                return json.load(exc)
            except ValueError:
                pass
        detail = exc.read(2000).decode(errors='replace')
        raise RuntimeError(f'Worker HTTP {exc.code}: {detail}') from exc


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
