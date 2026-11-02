"""Direct services for callers hosted by Core, including background threads.

External callers still enter through authenticated HTTP routes. These functions
are for trusted package code; only the selected worker crosses the network.
"""
from __future__ import annotations

_host_app = None


def configure(app):
    global _host_app
    _host_app = app


def application():
    from flask import current_app, has_app_context
    if has_app_context():
        return current_app._get_current_object()
    if _host_app is None:
        raise RuntimeError('Core internal services have not been configured')
    return _host_app



def app_context(app):
    from contextlib import nullcontext
    from flask import current_app, has_app_context
    if has_app_context() and current_app._get_current_object() is app:
        return nullcontext()
    return app.app_context()


def chat(payload, *, caller='internal'):
    """Return an OpenAI reply and HTTP-equivalent status, preserving call logs."""
    from hugpy_core.calllog import call_record
    from hugpy_core.web.routes import v1_chat
    body = dict(payload)
    if body.get('stream'):
        raise ValueError('internal chat expects a complete reply; use the streaming service')
    app = application()
    with app_context(app):
        parent = call_record.current()
        row = call_record.start(body, '/v1/chat/completions',
                                parent=(parent or {}).get('request_id'), caller=caller)
        try:
            with call_record.bound_call(row):
                response = app.make_response(v1_chat(**body))
                result = response.get_json(silent=True)
                if not isinstance(result, dict):
                    raise RuntimeError('Core chat returned a non-JSON reply')
                error = result.get('error')
                if isinstance(error, dict):
                    error = error.get('message') or str(error)
                call_record.finish(row, response.status_code, error, result)
                return result, response.status_code
        except Exception as exc:
            call_record.finish(row, 502, f'{type(exc).__name__}: {exc}')
            raise


def execute_prompt(*, caller='internal', **kwargs):
    """Adapt hosted prompt kwargs to Core's chat or task relay."""
    from hugpy_engine.task_endpoints import TASK_ROUTES, build_endpoint_request
    from hugpy_core.relay.video_transport import execute_task
    task = kwargs.get('task')
    if not task:
        from hugpy_core.relay.central import infer_task
        task = infer_task(kwargs.get('messages'), kwargs) or 'text-generation'
    model = kwargs.get('model_key') or kwargs.get('model') or ''
    if not isinstance(model, str):
        raise ValueError('model_key must be a string')
    if task in ('text-generation', 'image-text-to-text'):
        from hugpy_engine.resolvers.categories.builders import _build_chat_request
        chat_kwargs = dict(kwargs)
        if chat_kwargs.get('max_new_tokens') is None:
            limit = chat_kwargs.get('max_tokens', chat_kwargs.get('max_completion_tokens'))
            if limit is not None:
                chat_kwargs['max_new_tokens'] = limit
        request = _build_chat_request(chat_kwargs, model.strip())
        body = request.model_dump(exclude_none=True)
        body['model'] = body.pop('model_key', model.strip())
        body['task'] = task
        body['stream'] = False
        if 'max_new_tokens' in body:
            body['max_tokens'] = body.pop('max_new_tokens')
        for name in ('metadata', 'alloc', 'knobs', 'pool', 'max_chunks', 'chat_template_kwargs'):
            if kwargs.get(name) is not None:
                body[name] = kwargs[name]
        payload, status = chat(body, caller=caller)
        error = payload.get('error')
        if isinstance(error, dict):
            error = error.get('message') or str(error)
        choices = payload.get('choices') or []
        return {**payload, 'ok': status < 400, 'error': error,
                'model_key': payload.get('model') or model,
                'text': ((choices[0].get('message') or {}).get('content') or '') if choices else ''}
    endpoint = TASK_ROUTES.get(task)
    if endpoint is None:
        raise ValueError(f'Core has no task route for {task!r}')
    route, output = endpoint
    req = build_endpoint_request(kwargs, model.strip(), task=task, route=route, output=output)
    req.body['task'] = task
    for name in ('metadata', 'alloc', 'knobs'):
        if kwargs.get(name) is not None:
            req.body[name] = kwargs[name]
    return execute_task(application(), req, caller=caller)
