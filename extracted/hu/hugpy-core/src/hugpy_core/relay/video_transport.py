"""Private, in-process task handoff from hosted Video to Core's worker relay."""
import json
from types import SimpleNamespace


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
    from hugpy_core.registry import registrations
    from hugpy_core.registry.transport import request, target
    with registrations._connect() as conn:
        row = conn.execute(
            "SELECT worker FROM call_log WHERE worker IS NOT NULL AND "
            "(request_params->>'parent_request_id'=%s OR request_params->>'root_request_id'=%s) "
            "ORDER BY received_at DESC LIMIT 1", (request_id, request_id)).fetchone()
    if row is None:
        return None
    return request(target(row['worker']), path, timeout=3)


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
