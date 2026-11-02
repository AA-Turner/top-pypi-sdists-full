"""TASK RELAY: the wrapper's non-chat task routes, reachable through core like
/v1/chat/completions. Core picks the box holding ``model`` (the same pick() as
chat) and forwards the request to that box's hugpy_worker, which passes it to its
fitevict front door (placement, the task child, call_log). The body and the
answer pass through untouched (JSON or multipart in, JSON or bytes out), except
that a JSON body gets ``metadata.intent`` when the caller set none (intent.py)."""
from __future__ import annotations

import json
import os
import hmac
import re
import urllib.error
import urllib.request

from flask import Response, request

from hugpy_core.relay.openai import openai_error
from hugpy_core.relay.pick import NoWorker, pick, requested_worker_name, requested_worker_names

# The front door's task routes (fitevict engines/runners RunnerSpec.endpoint +
# extra routes). A protocol table: routes, not models.
TASK_ROUTES = ("/v1/embeddings", "/v1/summarize", "/v1/keywords",
               "/v1/audio/transcriptions", "/v1/audio/translations", "/v1/audio/speech",
               "/v1/images/generations", "/v1/images/edits", "/v1/videos/generations",
               "/v1/videos/upscale", "/v1/videos/interpolate")
TIMEOUT_S = 1800.0


def _model_of(raw: bytes, ctype: str) -> "str | None":
    if ctype.lower().startswith("multipart/"):
        m = re.search(rb'name="model"\r\n\r\n([^\r]+)\r\n', raw)
        return m.group(1).decode("utf-8", "replace") if m else None
    try:
        body = json.loads(raw.decode("utf-8", "replace") or "{}")
    except ValueError:
        return None
    return body.get("model") if isinstance(body, dict) else None


def _with_model(raw: bytes, ctype: str, model: str) -> bytes:
    """The request body with ``model`` set: a JSON key, or one more multipart field."""
    if ctype.lower().startswith("multipart/"):
        m = re.search(r'boundary="?([^";]+)"?', ctype)
        if not m:
            return raw
        b = m.group(1).encode()
        part = b"--" + b + b'\r\nContent-Disposition: form-data; name="model"\r\n\r\n' + model.encode() + b"\r\n"
        return part + raw
    try:
        body = json.loads(raw.decode("utf-8", "replace") or "{}")
    except ValueError:
        return raw
    if not isinstance(body, dict):
        return raw
    body["model"] = model
    return json.dumps(body).encode("utf-8")


def _relay(route: str, *, source=None):
    # Hosted arms can supply an internal request envelope. External routes keep
    # Flask's authenticated request, including public-demo placement restrictions.
    source = request if source is None else source
    raw = source.get_data()
    ctype = source.headers.get("Content-Type") or "application/json"
    model = _model_of(raw, ctype)
    chosen_worker = None
    # Public image jobs use the operator's service placement. The browser has
    # neither this key nor authority to choose a worker or a CPU override.
    service_key = os.environ.get("HUGPY_PUBLIC_API_KEY", "")
    public_image_worker = os.environ.get("HUGPY_PUBLIC_IMAGE_WORKER", "")
    if (service_key and public_image_worker and route in ("/v1/images/generations", "/v1/images/edits")
            and hmac.compare_digest(source.headers.get("Authorization", ""), "Bearer " + service_key)):
        from hugpy_core.config.model_preferences import public_models
        allowed = {key for surface in ("media", "video")
                   for task in ("text-to-image", "image-to-image")
                   for key in public_models(surface, task)}
        if model not in allowed:
            return openai_error("This model is unavailable in the public demo", 403)
        body = json.loads(raw)
        selection = body.get('alloc') if isinstance(body.get('alloc'), dict) else {}
        body["alloc"] = {"worker": public_image_worker, "alloc_mode": "gpu-only"}
        if 'workers' in selection:
            body['alloc']['workers'] = selection['workers']
        raw = json.dumps(body).encode()
    pin = source.args.get("worker") or None
    alloc = None
    if not ctype.lower().startswith("multipart/"):
        try:
            alloc = (json.loads(raw.decode("utf-8", "replace") or "{}") or {}).get("alloc")
        except (ValueError, AttributeError):
            pass
    elif source.form.get('alloc'):
        try:
            alloc = json.loads(source.form['alloc'])
        except ValueError:
            return openai_error('alloc must be a JSON object', 400)
    pin = pin or requested_worker_name(alloc)
    try:
        if model:
            worker = pick(model, pool=source.args.get("pool") or "", pin=pin,
                          workers=requested_worker_names(alloc))
        else:
            # no model named: central inference chooses (relay/central.py)
            from hugpy_core.relay.central import choose
            task = None
            if not ctype.lower().startswith("multipart/"):
                try:
                    task = (json.loads(raw.decode("utf-8", "replace") or "{}") or {}).get("task")
                except (ValueError, AttributeError):
                    task = None
            else:
                task = source.form.get("task")
            model, worker, _chosen = choose(task=task, route=route, pool=source.args.get("pool") or "",
                                            pin=pin, workers=requested_worker_names(alloc))
            raw = _with_model(raw, ctype, model)
    except NoWorker as exc:
        return openai_error(str(exc), exc.status)
    except ValueError as exc:
        return openai_error(str(exc), 400)
    if not ctype.lower().startswith("multipart/"):
        # the call's intent rides its own request (metadata.intent; intent.py)
        try:
            body = json.loads(raw.decode("utf-8", "replace") or "{}")
        except ValueError:
            body = None
        if isinstance(body, dict):
            from hugpy_core.brain.intent import stamp
            md = stamp(body.get("metadata"), body.get("intent"))
            if md != body.get("metadata"):
                body["metadata"] = md
                raw = json.dumps(body).encode("utf-8")
    url = worker["url"].rstrip("/") + route
    from hugpy_core.calllog.call_record import current, dispatch
    row = current()
    dispatch({}, worker)
    from hugpy_core.registry.transport import headers as worker_headers
    headers = worker_headers(worker, {"Content-Type": ctype})
    if row:
        headers["X-Hugpy-Parent-Request-Id"] = row["request_id"]
    # The chain's ROOT (the job that started it — a video job's engine request) rides
    # beside core's hop id, so that job can find the worker's call by its own id.
    root = (source.headers.get("X-Hugpy-Root-Request-Id")
            or ((row or {}).get("request_params") or {}).get("parent_request_id"))
    if root:
        headers["X-Hugpy-Root-Request-Id"] = root
    if source.headers.get("X-Task"):
        headers["X-Task"] = source.headers["X-Task"]
    req = urllib.request.Request(url, data=raw, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            data, status, out_type = r.read(), r.status, r.headers.get("Content-Type") or "application/json"
            execution_id = r.headers.get("X-Hugpy-Execution-Request-Id")
            worker_id = r.headers.get("X-Hugpy-Worker-Request-Id")
    except urllib.error.HTTPError as exc:
        data, status, out_type = exc.read(), exc.code, exc.headers.get("Content-Type") or "application/json"
        execution_id = exc.headers.get("X-Hugpy-Execution-Request-Id")
        worker_id = exc.headers.get("X-Hugpy-Worker-Request-Id")
    except Exception as exc:  # noqa: BLE001
        return openai_error(f"{worker.get('name')}: {type(exc).__name__}: {exc}", 502, "api_error")
    if row:
        row.setdefault("response_meta", {}).update(execution_request_id=execution_id, worker_request_id=worker_id)
    resp = Response(data, status=status, mimetype=out_type.split(";")[0])
    if execution_id:
        resp.headers["X-Hugpy-Execution-Request-Id"] = execution_id
    resp.headers["X-Hugpy-Worker"] = worker.get("name") or ""
    return resp
