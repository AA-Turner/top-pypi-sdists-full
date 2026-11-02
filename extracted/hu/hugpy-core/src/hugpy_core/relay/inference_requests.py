"""Database-driven execution. Claim briefly, run outside the transaction.

Pending submissions survive restarts. An expired running lease is failed with
an uncertain outcome, never automatically dispatched twice. Wrapper fit/evict
remains responsible for scheduling GPU work.
"""
from __future__ import annotations

import logging
import json
import os
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from hugpy_core.imports.functions import core_dsn, listen_channel

log = logging.getLogger(__name__)
_lock = threading.Lock()
_started = False
_owner = uuid.uuid4().hex
_CONCURRENCY = max(1, min(32, int(os.environ.get('HUGPY_EXECUTOR_CONCURRENCY', '4'))))


def _conn(**kwargs):
    return psycopg.connect(core_dsn(), row_factory=dict_row, connect_timeout=5, **kwargs)


def submit(kind: str, payload: dict) -> str:
    if kind not in ('chat', 'video-assist') or not isinstance(payload, dict):
        raise ValueError('invalid inference submission')
    with _conn() as conn:
        return conn.execute('INSERT INTO inference_requests (kind,payload) VALUES (%s,%s) '
                            'RETURNING request_id', (kind, Jsonb(payload))).fetchone()['request_id']


def get(request_id: str, *, kind: str | None = None) -> dict | None:
    with _conn() as conn:
        return conn.execute('SELECT request_id,kind,state,created_at,started_at,finished_at,'
                            'result,http_status,error FROM inference_requests WHERE request_id=%s '
                            'AND (%s::text IS NULL OR kind=%s)',
                            (request_id, kind, kind)).fetchone()


def ticket(request_id: str, *, kind: str | None = None) -> tuple[dict, int]:
    row = get(request_id, kind=kind)
    if row is None:
        return {'error': 'unknown request'}, 404
    pending = row['state'] in ('pending', 'running')
    result = dict(row['result'] or {})
    result.update(ticket=request_id, request_id=request_id, pending=pending, state=row['state'])
    return result, 200 if pending else (row['http_status'] or 200)


def stream(request_id: str, *, kind: str | None = None):
    """Push state changes; reconnecting always reads the durable current state."""
    from flask import Response, stream_with_context
    if get(request_id, kind=kind) is None:
        return {'error': 'unknown request'}, 404

    def events():
        with _conn(autocommit=True) as conn:
            listen_channel(conn, 'inference_requests')
            previous = None
            while True:
                row, status = ticket(request_id, kind=kind)
                if row != previous:
                    yield 'data: ' + json.dumps({**row, 'http_status': status}) + '\n\n'
                    previous = row
                if not row.get('pending'):
                    return
                for _ in conn.notifies(timeout=15, stop_after=1):
                    break
                yield ': heartbeat\n\n'
    return Response(stream_with_context(events()), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


def _claim() -> dict | None:
    with _conn() as conn:
        return conn.execute("UPDATE inference_requests SET state='running',owner=%s,"
                            "started_at=now(),lease_until=now()+interval '120 seconds' "
                            "WHERE request_id=(SELECT request_id FROM inference_requests "
                            "WHERE state='pending' ORDER BY created_at,request_id "
                            "FOR UPDATE SKIP LOCKED LIMIT 1) RETURNING *", (_owner,)).fetchone()


def _settle(job: dict, result: dict, status: int):
    error = str(result.get('error')) if result.get('error') else None
    if status >= 400 and not error:
        error = f'execution failed (HTTP {status})'
    with _conn() as conn:
        conn.execute("UPDATE inference_requests SET state=%s,result=%s,http_status=%s,error=%s,"
                     "finished_at=now(),lease_until=NULL WHERE request_id=%s AND owner=%s "
                     "AND state='running'",
                     ('failed' if error else 'done', Jsonb(result), status, error,
                      job['request_id'], _owner))


def execute_chat(**kwargs) -> dict:
    """Use Core's router directly, without the engine's HTTP catalog registry."""
    from hugpy_core.web.routes import v1_chat
    from flask import current_app
    payload = dict(kwargs)
    payload['model'] = payload.pop('model_key', None) or payload.get('model')
    if not payload['model']:
        raise ValueError('queued chat requires an explicit model')
    payload['max_tokens'] = payload.pop('max_new_tokens', None) or payload.get('max_tokens')
    payload['stream'] = False
    response = current_app.make_response(v1_chat(**payload))
    data = response.get_json() or {}
    if response.status_code >= 400:
        error = data.get('error') or 'inference failed'
        if isinstance(error, dict):
            error = error.get('message') or str(error)
        return {'ok': False, 'error': error, 'model_key': payload['model']}
    return {'ok': True, 'text': data['choices'][0]['message'].get('content') or '',
            'model_key': data.get('model'), 'usage': data.get('usage'),
            'request_id': (data.get('hugpy') or {}).get('request_id')}


def _run(app, job):
    try:
        from hugpy_core.calllog.call_record import bound_call
        with _conn() as conn:
            row = conn.execute('SELECT to_jsonb(c) AS row FROM call_log c '
                               'WHERE request_id=%s', (job['request_id'],)).fetchone()['row']
        with app.app_context(), bound_call(row):
            if job['kind'] == 'video-assist':
                from hugpy_video.web.assist import _video_prompt_assist_impl
                response = app.make_response(_video_prompt_assist_impl(job['payload']))
                result, status = response.get_json() or {}, response.status_code
            else:
                result = execute_chat(**job['payload'])
                status = 200 if result.get('ok') else 502
            result['request_id'] = job['request_id']
            _settle(job, result, status)
    except Exception as exc:
        log.exception('Inference request %s failed', job['request_id'])
        _settle(job, {'error': f'{type(exc).__name__}: {exc}', 'request_id': job['request_id']}, 502)


def _maintain(request_ids):
    with _conn() as conn:
        conn.execute("UPDATE inference_requests SET lease_until=now()+interval '120 seconds' "
                     "WHERE state='running' AND owner=%s AND request_id=ANY(%s) AND lease_until>now()",
                     (_owner, request_ids))
        conn.execute("UPDATE inference_requests SET state='failed',finished_at=now(),http_status=503,"
                     "error='Executor lease expired; execution outcome is unknown. Not automatically retried.',"
                     "result=jsonb_build_object('error','Executor lease expired; execution outcome is unknown. "
                     "Not automatically retried.','request_id',request_id) "
                     "WHERE state='running' AND lease_until<now()")


def _loop(app):
    active = {}
    with ThreadPoolExecutor(max_workers=_CONCURRENCY, thread_name_prefix='inference') as pool:
        while True:
            try:
                with _conn(autocommit=True) as conn:
                    listen_channel(conn, 'inference_requests')
                    while True:
                        for future in list(active):
                            if future.done():
                                active.pop(future)
                                try:
                                    future.result()
                                except Exception:
                                    log.exception('Inference executor could not persist its result')
                        _maintain(list(active.values()))
                        while len(active) < _CONCURRENCY:
                            job = _claim()
                            if job is None:
                                break
                            active[pool.submit(_run, app, job)] = job['request_id']
                        # The periodic scan also recovers missed notifications.
                        for _ in conn.notifies(timeout=5, stop_after=1):
                            break
            except Exception:
                log.exception('Inference listener reconnecting')
                threading.Event().wait(2)


def start(app):
    global _started
    with _lock:
        if _started:
            return
        _started = True
    threading.Thread(target=_loop, args=(app,), name='inference-listen', daemon=True).start()
