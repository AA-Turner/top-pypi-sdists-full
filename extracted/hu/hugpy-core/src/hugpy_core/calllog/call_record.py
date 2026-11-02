"""Core owns its call row; downstream calls own different IDs linked in params.

Uses the existing call_log table and wrapper's jsonb_populate_record UPSERT
pattern. No execution side store or copied engine measurements.
"""
import datetime
import json
import logging
import os
import time
import uuid
from contextlib import contextmanager
from contextvars import ContextVar

_background_call = ContextVar('core_background_call', default=None)

log = logging.getLogger(__name__)
_COLS = {'request_id', 'model_name', 'received_at', 'forwarded_at', 'responded_at',
         'task', 'caller', 'callee', 'worker', 'endpoint', 'from_ip', 'request_body',
         'request_params', 'response_body', 'response_meta', 'call_state', 'http_status', 'error'}

def create_request_id(key):
  return f"{key}-{uuid.uuid4().hex}"

def write(row):
    from hugpy_core.calllog.calllog_db import store
    data = {k: v for k, v in row.items() if k in _COLS}
    for key in ('received_at', 'forwarded_at', 'responded_at'):
        if isinstance(data.get(key), (float, int)):
            data[key] = datetime.datetime.fromtimestamp(data[key], datetime.timezone.utc).isoformat()
    cols = ', '.join(data)
    updates = ', '.join(f'{k}=EXCLUDED.{k}' for k in data if k != 'request_id')
    try:
        store().sql(f'INSERT INTO call_log ({cols}) SELECT {cols} FROM '
                    'jsonb_populate_record(NULL::call_log, %s::jsonb) '
                    f'ON CONFLICT (request_id) DO UPDATE SET {updates}',
                    (json.dumps(data, default=str),))
    except Exception:
        log.exception('Could not record core call %s', row.get('request_id'))


def start(body, endpoint, *, request_id=None, parent=None, caller=None):
    row = {'request_id': request_id or 'core-' + uuid.uuid4().hex,
           'model_name': body.get('model_key') or body.get('model') or
                         (body['models'][0] if isinstance(body.get('models'), list) and len(body['models']) == 1 else None),
           'task': body.get('task'), 'received_at': time.time(),
           'caller': caller, 'callee': 'core', 'endpoint': endpoint,
           'request_body': body, 'request_params': {'hop': 'core', 'parent_request_id': parent},
           'call_state': 'pending'}
    write(row)
    return row


def finish(row, status=200, error=None, response=None):
    row.update(responded_at=time.time(), http_status=status, error=error,
               call_state='cancelled' if status == 499 else ('failed' if error or status >= 400 else 'done'))
    if response is not None:
        row['response_body'] = response
    write(row)


def close_orphans(started):
    """Core's own rows still pending from an EARLIER core process cannot be
    running: close them as failed, so nothing reads them as in flight. Not the
    benchmark run row (benchmark_log closes it with its run status) and not a
    box's pull row (the box owns it and may still be pulling)."""
    from hugpy_core.calllog.calllog import query
    rows = query("SELECT to_jsonb(c) FROM call_log c WHERE call_state = 'pending' "
                 "AND request_params->>'hop' = 'core' AND endpoint IS DISTINCT FROM '/llm/benchmark/run' "
                 "AND received_at < to_timestamp(%s)", (started,))
    for (row,) in rows:
        finish(row, 500, 'core restarted before the call finished')
    return len(rows)


def current():
    from flask import g, has_request_context
    bound = _background_call.get()
    if bound is not None:
        return bound
    return getattr(g, 'call_row', None) if has_request_context() else None


@contextmanager
def bound_call(row):
    """Give a durable executor the same forwarding/logging context as HTTP."""
    token = _background_call.set(row)
    try:
        yield row
    finally:
        _background_call.reset(token)


def dispatch(body, worker):
    """Record core's forwarding edge; pass its ID as the downstream parent."""
    row = current()
    if row is not None:
        body = dict(body)
        body['request_id'] = row['request_id']
        body['metadata'] = {**(body.get('metadata') or {}), 'parent_request_id': row['request_id']}
        row.update(forwarded_at=time.time(), worker=worker.get('name'))
        if body.get('task'):
            row['task'] = body['task']
        row['response_meta'] = {'worker_url': worker.get('url')}
        write(row)
    return body


def attach(app):
    from flask import g, request
    from hugpy_core.brain.intent import stamp
    from hugpy_core.relay.taskrelay import TASK_ROUTES
    routes = set(TASK_ROUTES) | {'/v1/chat/completions', '/chat/stream', '/llm/benchmark/run'}

    @app.before_request
    def begin_call():
        route = request.path.removeprefix('/api')
        if request.method != 'POST' or route not in routes:
            return
        body = request.get_json(silent=True) if request.is_json else None
        body = dict(body) if isinstance(body, dict) else {'content_type': request.content_type,
                                                        'content_length': request.content_length}
        md = stamp(body.get('metadata'), body.get('intent') or
                   ('grading' if route == '/llm/benchmark/run' else None))
        body['metadata'] = md
        g.call_row = start(body, route, parent=request.headers.get('X-Hugpy-Parent-Request-Id') or
                           md.get('parent_request_id'), caller=request.remote_addr)

    @app.after_request
    def end_call(response):
        row = getattr(g, 'call_row', None)
        if row is None:
            return response
        response.headers['X-Hugpy-Request-Id'] = row['request_id']
        chosen = getattr(g, 'model_chosen', None)
        if chosen:
            response.headers['X-Hugpy-Model'] = chosen.get('model_key') or ''
            response.headers['X-Hugpy-Model-Chosen-Via'] = f"{chosen.get('chosen_via') or 'ranked'}; task={chosen.get('task')}"
        if getattr(g, 'call_async', False):
            return response
        if response.mimetype == 'text/event-stream':
            source = response.response
            def logged():
                error, status = None, response.status_code
                pending = ''
                try:
                    for chunk in source:
                        pending += chunk.decode('utf-8', 'replace') if isinstance(chunk, bytes) else chunk
                        while '\n' in pending:
                            line, pending = pending.split('\n', 1)
                            if not line.startswith('data:'):
                                continue
                            try:
                                event = json.loads(line[5:])
                            except ValueError:
                                continue
                            if isinstance(event, dict) and (event.get('type') == 'error' or event.get('error')):
                                error = str(event.get('message') or event.get('error'))
                                status = 502
                        yield chunk
                except GeneratorExit:
                    status, error = 499, 'client disconnected'
                    raise
                except Exception as exc:
                    status, error = 500, repr(exc)
                    raise
                finally:
                    close = getattr(source, 'close', None)
                    if close:
                        try:
                            close()
                        except Exception:
                            log.exception('Closing core call stream failed')
                    # Relay records semantic errors even if the public stream encodes them as text.
                    finish(row, max(status, row.get('http_status', 0)), error or row.get('error'))
            response.response = logged()
        else:
            body = response.get_json(silent=True) if response.is_json else None
            error = str(body.get('error')) if isinstance(body, dict) and body.get('error') else None
            finish(row, response.status_code, error, body)
        return response

def pull_start(
    model=None,
    worker=None,
    parent_request_id=None,
    for_request_id=None
    ):
  if not model or not worker:
      return {"error": "model and worker required"}
  key = "pull"; callee = "central"; task = f"{callee}-{key}"; request_id = create_request_id(key)
  row = start(
      {
          "model": model,
          "worker": worker
          },
      "/llm/central/pulls",
      request_id=request_id,
      parent=parent_request_id,
      caller=worker
      )
  row.update(worker=worker,
             task=task,
             callee=callee
             )
  row["request_params"].update(hop=task,
                               for_request_id=for_request_id)
  write(row)
  return {"request_id": row["request_id"]}

def pull_finish(request_id=None, ok=None, error=None, **body):
  from .calllog import query
  rows = query("SELECT to_jsonb(c) FROM call_log c WHERE request_id=%s "
               "AND request_params->>'hop'='central-pull'", (request_id,))
  if not rows:
      return {"error": "pull call not found"}
  row = rows[0][0]
  finish(row, 502 if error or ok is False else 200, error, {"ok": ok, "error": error, **body})
  return {
      "request_id": request_id,
      "call_state": row["call_state"]
      }
