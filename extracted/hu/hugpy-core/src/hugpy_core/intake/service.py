"""Independent, read-only HTTP telemetry collector. Run with python -m.

Worker registrations remain in the installed core registration store. Telemetry
and presence are committed to HUGPY_CORE_DB via abstract_database. This service
does not start Flask, scan drives, transfer weights, or push worker settings.
"""
from __future__ import annotations

import json
import logging
import signal
import threading
import time
import urllib.parse

from psycopg.types.json import Jsonb

from hugpy_core.imports.functions import notify_channel
from hugpy_core.intake import mirror
from hugpy_core.intake.presence import allocation as _allocation
from hugpy_core.intake.store import store
from hugpy_core.models.census import observe_worker

log = logging.getLogger(__name__)
PAGE = 2000


def registrations():
    from hugpy_core.registry.registrations import all as all_registrations
    return all_registrations()


def get(worker, path, timeout=30):
    from hugpy_core.registry.transport import request
    return request(worker, path, timeout=timeout)


def presence(worker, state, models, storage=None, resources=None):
    name = worker['name']
    inventory = [m for m in models if isinstance(m, dict) and m.get('id')
                 and not m.get('route') and not m.get('variant_of')]
    local = [m for m in inventory if m.get('storage_role') != 'central']
    host = (state.get('host_state') or [{}])[0]
    payload = {
        'id': name, 'name': name, 'url': worker['url'], 'last_seen': time.time(),
        'engine': {'name': 'fitevict', 'supports_gpu_offload': True},
        'ram_total': host.get('mem_total'), 'free_ram': host.get('mem_available'),
        'ram_free_bytes': host.get('mem_free'), 'swap_total': host.get('swap_total'), 'swap_free': host.get('swap_free'),
        'gpus': [{'index': g.get('device'), 'name': g.get('name'), 'uuid': g.get('uuid'),
                  'memory_total': g.get('total'), 'memory_free': g.get('free'),
                  'memory_used': g.get('used')} for g in state.get('gpu_state', [])],
        'cpu': (state.get('cpu_state') or [None])[0],
        'allocations': [_allocation(r) for r in state.get('residents', [])],
        'models': [m['id'] for m in inventory],
        'models_local': [m['id'] for m in local],
        'models_central': {m['id']: m for m in inventory if m.get('storage_role') == 'central'},
        'loaded_models': [m['id'] for m in inventory if m.get('resident')],
        'models_discovered': {m['id']: {k: v for k, v in m.items()
                                      if k not in ('id', 'object', 'owned_by')} for m in local},
    }
    advertised = state.get('data_service')
    if isinstance(advertised, dict) and advertised.get('protocol') == 'hugpy-wrapper-data':
        if advertised.get('version') != 1 or advertised.get('store_id') != state.get('store_id'):
            raise ValueError('Wrapper data service identity or protocol changed; retry collection')
        payload['data_service'] = advertised
    else:
        payload['data_service'] = {
            'protocol': 'hugpy-wrapper-data', 'version': 0, 'authority': 'wrapper',
            'store_id': state.get('store_id'), 'backend': None,
            'paths': {'state': '/v1/telemetry/state', 'log': '/v1/telemetry',
                      'pair_settings': '/v1/settings/pair', 'box_settings': '/v1/settings/box'},
        }
    if isinstance(state.get('settings_report'), dict):
        payload['settings_report'] = state['settings_report']
    if (payload['data_service'].get('capabilities') or {}).get('physical_inventory') is False:
        # A routable Discovery catalog is not a report of copies on this box.
        payload['catalog'] = inventory
        payload['models'] = [m['id'] for m in inventory if m.get('selectable') is not False]
        payload['models_discovered'] = None
        payload['models_local'] = []
        payload['models_central'] = {}
    if isinstance(storage, dict):
        payload['storage'] = storage
    if isinstance(resources, dict):
        payload['resources'] = {key: resources[key] for key in (
            'host_state', 'cpu_state', 'gpu_state', 'process_state', 'residents',
            'cards', 'gpu_policy', 'queue', 'sampled_at', 'active_requests') if key in resources}
        payload['cards'] = resources.get('cards') or []
        payload['gpu_policy'] = resources.get('gpu_policy') or {}
        payload['resources_sampled_at'] = resources.get('sampled_at')
    return payload


def collect(worker, since=-1, wait=30):
    name = worker['name']
    query = '?' + urllib.parse.urlencode({'wait': wait, 'since': since}) if since >= 0 else ''
    state = get(worker, '/v1/telemetry/state' + query, 60)
    capabilities = (state.get('data_service') or {}).get('capabilities') or {}
    health = get(worker, '/health', 5)
    store_id = str(state.get("store_id") or "")
    db = store()
    with db.connect() as conn:
        cols = mirror.Columns(conn)
        cursors = {table: mirror.cursor(conn, name, table, store_id) for table in mirror.LOG_TABLES}
    # Finish all network reads before opening the write transaction.
    logs = {}
    for table, cursor in cursors.items():
        rows = []
        while True:
            page = get(worker, '/v1/telemetry?' + urllib.parse.urlencode(
                {'table': table, 'since': cursor, 'limit': PAGE}), 60)
            if str(page.get('store_id') or '') != store_id:
                raise ValueError('worker store changed during telemetry collection; retrying')
            rows.extend(page.get('rows') or [])
            if not page.get('more'):
                break
            next_cursor = int(page.get('next') or 0)
            if next_cursor <= cursor:
                raise ValueError(f'{table}: telemetry cursor did not advance')
            cursor = next_cursor
        logs[table] = rows
    models = get(worker, '/v1/models').get('data')
    if not isinstance(models, list):
        raise ValueError('worker did not return a model inventory')
    try:
        # This is the worker's HTTP storage survey, not a local filesystem walk.
        storage = get(worker, '/storage', 30) if capabilities.get('storage') is not False else None
    except Exception as exc:
        log.warning('%s: storage survey unavailable: %s', name, exc)
        storage = None
    try:
        resources = get(worker, '/v1/telemetry/resources', 15)
    except Exception as exc:
        log.warning('%s: card ledger unavailable: %s', name, exc)
        resources = None
    from hugpy_core.registry.registrations import get as saved_connection, is_connected
    if not is_connected(saved_connection(name)):
        # disconnected while this poll was in flight: drop it, keep the mark
        return int(state.get('changes') or 0), {}
    payload = presence(worker, state, models, storage, resources)
    payload['wrapper_version'] = health.get('source_version') or health.get('version')
    payload['wrapper_deb_version'] = health.get('deb_version')
    with db.connect() as conn:
        counts = mirror.apply_state(conn, cols, name, state)
        if any(n < 0 for n in counts.values()):
            raise RuntimeError('state mirror failed; batch rolled back')
        for table, rows in logs.items():
            counts[table] = mirror.apply_log(conn, cols, name, table, rows, store_id)
        observe_worker(payload, conn=conn)
        from hugpy_core.intake.wrapper_settings import apply_report
        apply_report(conn, name, state.get("pair_settings"))
        conn.execute('INSERT INTO worker_presence(worker,payload) VALUES (%s,%s) '
                     'ON CONFLICT(worker) DO UPDATE SET payload=EXCLUDED.payload, observed_at=now()',
                     (name, Jsonb(mirror.without_nul(payload))))
        conn.execute('INSERT INTO intake_boxes(box,url,changes,heard_at,error) VALUES (%s,%s,%s,now(),NULL) '
                     'ON CONFLICT(box) DO UPDATE SET url=EXCLUDED.url,changes=EXCLUDED.changes, '
                     'heard_at=now(),error=NULL', (name, worker['url'], int(state.get('changes') or 0)))
        # HTTP listeners wake only after this complete batch commits.
        conn.execute('SELECT pg_notify(%s,%s)', (notify_channel('live'), name))
    # The standalone intake service is the active collector in this deployment.
    # Keep the per-worker model verdicts in step with the facts and budgets it
    # just committed; the planner coalesces unchanged inputs and writes the
    # model_worker_quants rows consumed directly by the console.
    try:
        from hugpy_core.brain import planner
        planner.maybe_refresh(payload)
    except Exception:  # noqa: BLE001 — planning must never interrupt telemetry
        log.exception('%s: planner refresh failed', name)
    try:
        from hugpy_core.intake.fact_exchange import schedule
        if capabilities.get('fact_exchange') is not False:
            schedule(worker)
    except Exception:
        log.exception('%s: identified fact exchange failed', name)
    # models-db-v1: when the Wrapper advertises a models DB, mirror its changed
    # per-model partitions off this loop (own thread, own transaction).
    try:
        from hugpy_core.intake import models_db
        service = state.get('data_service')
        models_db.schedule(worker, service.get('models_db') if isinstance(service, dict) else None)
    except Exception:  # noqa: BLE001 — the models DB mirror must never interrupt telemetry
        log.exception('%s: models-db sync scheduling failed', name)
    return int(state.get('changes') or 0), counts


def run_worker(worker, stop):
    since, failures = -1, 0
    while not stop.is_set():
        started = time.monotonic()
        try:
            since, counts = collect(worker, since)
            if since >= 0 and (failures or any(counts.values())):
                log.info('%s: committed %s', worker['name'], {k: v for k, v in counts.items() if v})
            failures = 0
            # Some worker versions answer long polls immediately. Avoid a hot loop.
            stop.wait(max(0, 2 - (time.monotonic() - started)))
        except Exception as exc:
            since = -1
            failures += 1
            log.warning('%s: %s: %s', worker['name'], type(exc).__name__, exc)
            try:
                store().sql('INSERT INTO intake_boxes(box,url,error,error_at) VALUES (%s,%s,%s,now()) '
                            'ON CONFLICT(box) DO UPDATE SET error=EXCLUDED.error,error_at=now()',
                            (worker['name'], worker['url'], f'{type(exc).__name__}: {exc}'[:2000]))
            except Exception:
                log.exception('Could not record intake failure')
            stop.wait(min(30, 2 ** min(failures, 5)))


def run(stop):
    """Run the collector independently or in an embedding process."""
    active = {}
    try:
        while not stop.is_set():
            try:
                from hugpy_core.registry.registrations import is_connected
                configs = {w['name']: w for w in registrations() if is_connected(w)}
                for name in list(active):
                    config, event, thread = active[name]
                    if configs.get(name) != config:
                        event.set()
                        thread.join(1)
                        if not thread.is_alive():
                            del active[name]
                for name, worker in configs.items():
                    if name not in active:
                        event = threading.Event()
                        thread = threading.Thread(target=run_worker, args=(worker, event), daemon=True)
                        active[name] = (worker, event, thread)
                        thread.start()
                        log.info('Collecting telemetry for %s', name)
            except Exception:
                log.exception('Could not refresh worker registrations')
            stop.wait(15)
    finally:
        for _, event, _ in active.values():
            event.set()


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    run(stop)


if __name__ == '__main__':
    main()
