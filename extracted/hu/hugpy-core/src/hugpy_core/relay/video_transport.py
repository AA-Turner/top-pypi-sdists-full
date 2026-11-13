"""Private, in-process task handoff from hosted Video to Core's worker relay."""
import json
from types import SimpleNamespace

# One hop id per observed job: video's request id -> the wrapper queue row id
# already found for it, so follow-up polls fetch exactly one cursor row.
_NATIVE_ROWS = {}


def _native_call_rows(worker_name, request_id, hop_id):
    """The native wrapper's call_log row for this call, shaped like the old
    descending browse reply ({"rows": [row]}).

    The wrapper keeps core's hop id as the row's ``caller`` (it drops the root
    header), and its telemetry pages ascending by id only — so the first find
    seeds a cursor from the live queue's ids, and the row id is remembered for
    the next polls. The row's values are computed live from the queue table, so
    a re-read carries current stage timestamps.
    """
    from hugpy_core.registry.transport import request, target
    configured = target(worker_name)
    row_id = _NATIVE_ROWS.get(request_id)
    if row_id is None:
        queue = request(configured, '/v1/queue', timeout=3)
        active = [r['id'] for r in (queue.get('waiting') or []) + (queue.get('turn') or [])
                  if isinstance(r, dict) and isinstance(r.get('id'), int)]
        recent = [r['id'] for r in (queue.get('recent') or [])
                  if isinstance(r, dict) and isinstance(r.get('id'), int)]
        since = min(active) - 1 if active else (min(recent) - 1 if recent else 0)
        page = request(configured, f'/v1/telemetry?table=call_log&since={max(0, since)}&limit=5000',
                       timeout=5)
        matches = [r for r in page.get('rows') or [] if r.get('caller') == hop_id]
        if not matches:
            return None
        row_id = max(r['id'] for r in matches)
        if len(_NATIVE_ROWS) > 512:
            _NATIVE_ROWS.clear()
        _NATIVE_ROWS[request_id] = row_id
    page = request(configured, f'/v1/telemetry?table=call_log&since={row_id - 1}&limit=1', timeout=3)
    rows = [r for r in page.get('rows') or [] if r.get('id') == row_id]
    if not rows:
        _NATIVE_ROWS.pop(request_id, None)
        return None
    # The observer's caller matches on its own id; the wrapper row carries only
    # core's hop id, so the chain is restored here — an id rewrite, not a fact.
    row = {**rows[0], 'request_params': {'parent_request_id': request_id,
                                         'root_request_id': request_id}}
    return {'rows': [row], 'store_id': page.get('store_id')}


def observe_task(request_id, path):
    """Read live progress at this call's selected Wrapper with its credentials.

    Core's own HTTP base and mirrored call rows cannot substitute for the live
    worker's per-step record. No inference is started by this observer.
    """
    allowed = {
        '/v1/telemetry/rows?table=call_log&sort=id&direction=desc&limit=50',
        '/v1/telemetry/state',
    }
    if path not in allowed:
        raise ValueError('Unsupported task observation path')
    from hugpy_core.registry import registrations, registry
    from hugpy_core.registry.transport import request, target
    from hugpy_core.relay.relay import is_native
    with registrations._connect() as conn:
        row = conn.execute(
            "SELECT worker, request_id FROM call_log WHERE worker IS NOT NULL AND "
            "(request_params->>'parent_request_id'=%s OR request_params->>'root_request_id'=%s) "
            "ORDER BY received_at DESC LIMIT 1", (request_id, request_id)).fetchone()
    if row is None:
        return None
    live = registry.lookup_worker(row['worker'])
    if path.startswith('/v1/telemetry/rows') and live is not None and is_native(live):
        # The native wrapper serves no descending browse; translate the same
        # intent through its ascending cursor. An absent observation stays
        # "not recorded yet", never a fabricated progress row.
        try:
            return _native_call_rows(row['worker'], request_id, row['request_id'])
        except Exception:  # noqa: BLE001 — observation is best-effort, never a fault
            return None
    return request(target(row['worker']), path, timeout=3)


def cancel_task(request_id):
    """Cancel the call's wrapper-side row, best-effort (the mid-flight seam).

    The wrapper resolves POST /v1/requests/<id>/cancel by the id the caller sent
    with the call — core's hop id. A waiting row is cancelled outright; a row at
    its turn gets cancel_requested_at and the run stops at its next step
    boundary. Returns the wrapper's recorded outcome ({queue_id, state, when?}),
    or None when the call is unknown here or the wrapper could not be asked.
    """
    from urllib.parse import quote
    from hugpy_core.registry import registrations
    from hugpy_core.registry.transport import request, target
    with registrations._connect() as conn:
        row = conn.execute(
            "SELECT worker, request_id FROM call_log WHERE worker IS NOT NULL AND "
            "(request_params->>'parent_request_id'=%s OR request_params->>'root_request_id'=%s) "
            "ORDER BY received_at DESC LIMIT 1", (request_id, request_id)).fetchone()
    if row is None:
        return None
    try:
        return request(target(row['worker']),
                       '/v1/requests/' + quote(row['request_id'], safe='') + '/cancel',
                       {}, timeout=5)
    except RuntimeError as exc:
        if 'HTTP 409' in str(exc):
            # the wrapper's recorded outcome for a finished row, not a fault
            return {'state': 'finished', 'when': 'already finished; nothing to cancel'}
        return None
    except (OSError, ValueError):
        return None


def execute_task(app, req, *, caller="video"):
    from hugpy_core.calllog import call_record
    from hugpy_core.relay.taskrelay import _relay
    from hugpy_engine.task_endpoints import TaskEndpointRunner
    body = {**req.body, 'model': req.model_key}
    raw = json.dumps(body).encode('utf-8')
    source = SimpleNamespace(
        get_data=lambda: raw,
        headers={'Content-Type': 'application/json', 'X-Hugpy-Root-Request-Id': req.request_id},
        args={'pool': req.pool or ''}, form={},
    )
    row = call_record.start(body, req.route, parent=req.request_id, caller=caller)
    try:
        with app.app_context(), call_record.bound_call(row):
            if req.route == '/v1/chat/completions':
                from hugpy_core.web.routes import v1_chat
                response = app.make_response(v1_chat(**{**body, 'pool': req.pool or '', 'stream': False}))
            else:
                response = app.make_response(_relay(req.route, source=source))
            payload = response.get_json(silent=True)
            if payload is None:
                payload = {'error': 'Task relay returned a non-JSON response'}
            if req.route == '/v1/chat/completions' and isinstance(payload, dict):
                choices = payload.get('choices') or []
                payload['text'] = ((choices[0].get('message') or {}).get('content') or '') if choices else ''
            result = TaskEndpointRunner(None)._result(req, response.status_code, payload)
            call_record.finish(row, response.status_code, result.error, payload)
            return result
    except Exception as exc:
        call_record.finish(row, 502, f'{type(exc).__name__}: {exc}')
        raise
