"""The hot path: one call in, one box chosen, the answer streamed back.

decide (by central's allocation when it is here) → forward to the FIRST box only
(its key, X-Hugpy-Parent-Request-Id = this call's id) → the box refuses before the
first byte (a load error, won't fit, a profile still building, model not there,
502/503/504, unreachable)? That is a FACT against the allocation (operator
2026-10-14: allocation is known before placement; a refused call is never bounced
to another box): recorded through central (REFUSED) and returned to the caller
with the reason. Otherwise stream status, headers and body back as they arrive.
Never re-routed after the first byte. One route_log row per call holds the
decision and the attempt.
"""
from __future__ import annotations

import json
import time
import uuid
from typing import Optional, Tuple

import aiohttp
from aiohttp import web

from hugpy_core.router.core.decide import decide
from hugpy_core.router.core.types import CallSpec
from hugpy_core.router.imports import constants as C
from hugpy_core.router.imports.classes import RequestView
from hugpy_core.router.imports.functions import split_model
from hugpy_core.router.observability import store as S
from hugpy_core.router.serve.keys import ALLOCATION, CONTRACTS, REFUSED, REGISTRY, SESSION
from hugpy_core.router.serve.queue import QUEUE, free_by_registry

PASS_RESPONSE_HEADERS = ("Content-Type", "Content-Disposition", "X-Hugpy-Execution-Request-Id", "Cache-Control")


def call_fields(body: bytes, ctype: str) -> Tuple[Optional[str], Optional[str]]:
    """(model, pinned box) from a JSON body ({"model", "alloc": {"worker"}}) or a
    multipart form's `model` field."""
    if "multipart/form-data" in (ctype or "").lower():
        import re
        m = re.search(rb'name="model"\r\n\r\n([^\r\n]*)\r\n', body or b"")
        return (m.group(1).decode("utf-8", "replace").strip() if m else None), None
    try:
        data = json.loads(body or b"{}")
    except ValueError:
        return None, None
    if not isinstance(data, dict):
        return None, None
    alloc = data.get("alloc") if isinstance(data.get("alloc"), dict) else {}
    pin = alloc.get("worker") if isinstance(alloc.get("worker"), str) and alloc["worker"].strip() else None
    return (data.get("model") if isinstance(data.get("model"), str) else None), (pin.strip() if pin else None)


def _err(status: int, message: str, typ: str = "invalid_request_error", **extra) -> web.Response:
    return web.json_response({"error": {"message": message, "type": typ, "code": status, **extra}}, status=status)


def execution_request(body: bytes, ctype: str) -> CallSpec:
    """Snapshot existing JSON knobs without interpreting Wrapper policy.

    The original request body still goes to Wrapper. This immutable copy is for
    resident matching and the decision receipt; multipart retains suffix syntax.
    """
    model, pin = call_fields(body, ctype)
    if not model:
        raise ValueError("the call names no model")
    base, options = split_model(model)
    knobs = {}
    if 'multipart/form-data' not in (ctype or '').lower():
        data = json.loads(body or b'{}')
        knobs = data.get('knobs')
        if knobs is None:
            knobs = {}
        if not isinstance(knobs, dict):
            raise ValueError('knobs must be a JSON object')
    return CallSpec(model=base, options=options, pin=pin,
                    knobs_json=json.dumps(knobs, sort_keys=True, separators=(',', ':'), allow_nan=False))


def _refusal(status: int, raw: bytes) -> Optional[str]:
    """The box's refusal reason when this error is a refusal of the call (the box
    could not serve it now), else None (the error then goes back to the client as
    the box sent it)."""
    try:
        payload = json.loads(raw or b"{}")
    except ValueError:
        payload = {}
    err = payload.get("error") if isinstance(payload, dict) else None
    typ = err.get("type") if isinstance(err, dict) else None
    msg = err.get("message") if isinstance(err, dict) else None
    if status in (502, 503, 504) or typ in C.REFUSAL_TYPES:
        return f"{status} {typ or ''}: {msg or ''}".strip()
    return None


def _stamped(body: bytes, ctype: str) -> bytes:
    """The JSON body with metadata.intent set (the caller's own label wins), so the
    box records the call's intent; any other body passes through untouched."""
    if "json" not in (ctype or "").lower() and ctype:
        return body
    try:
        data = json.loads(body or b"{}")
    except ValueError:
        return body
    if not isinstance(data, dict):
        return body
    from hugpy_core.brain.intent import stamp
    md = stamp(data.get("metadata"), data.get("intent"))
    if md == data.get("metadata"):
        return body
    data["metadata"] = md
    return json.dumps(data).encode("utf-8")


async def handle(request: web.Request) -> web.StreamResponse:
    app = request.app
    denied = S.KEYS.check(RequestView(request), "use")
    if denied is not None:
        return web.json_response(denied[1], status=denied[0])
    body = await request.read()
    ctype = request.headers.get("Content-Type", "")
    body = _stamped(body, ctype)
    try:
        call = execution_request(body, ctype)
    except ValueError as exc:
        return _err(400, str(exc))
    base, opts, pin = call.model, call.options, call.pin
    rid = "rt-" + uuid.uuid4().hex
    S.open_call(rid, request.path, base, opts, pin, request.remote or "")
    registry, contracts, session = app[REGISTRY], app[CONTRACTS], app[SESSION]
    attempts = []

    d = decide(call, registry.boxes(), contracts, allocation=app.get(ALLOCATION))
    receipt = {"boxes": d.boxes, "why": d.why, "refused": d.refused,
               "execution_request": call.execution_request()}
    S.update_call(rid, path=d.path, decision=receipt)
    if not d.ok:
        S.update_call(rid, state="refused", http_status=503, attempts=attempts, responded_at=time.time(),
                      error="no box could take the call")
        return _err(503, "no box could take the call", "no_box", reasons=dict(d.refused), path=d.path, request_id=rid)
    name = d.boxes[0]
    # central's queue: no allocated box free for this model → a ticket, not a pile-on
    queue, ticket, free = app.get(QUEUE), None, free_by_registry(registry)
    if queue is not None and not any(free(b, call.model) for b in d.boxes):
        try:
            data = json.loads(body or b"{}") if "json" in ctype.lower() or not ctype else {}
        except ValueError:
            data = {}
        ticket = queue.ticket(rid, call.model, call.options, request.headers.get("X-Hugpy-Group") or request.remote or "",
                              d.boxes, body=data if isinstance(data, dict) else {})
        S.update_call(rid, path="queue", decision={**receipt, "ticket": ticket.id})
        box = await queue.wait(ticket, free)
        if box is None:
            S.update_call(rid, state="refused", http_status=503, responded_at=time.time(),
                          error=f"queue: {ticket.reason}")
            return _err(503, f"no allocated box freed within {ticket.max_wait_s:.0f}s", "queue_timeout",
                        ticket=ticket.id, boxes=d.boxes, reasons=dict(d.refused), request_id=rid)
        name = box
    link = registry.link(name)
    selected = next((box for box in registry.boxes() if box.name == name), None)
    dispatch_identity = selected.observation_identity if selected is not None else None
    link.last_picked = time.time()
    headers = {"Content-Type": ctype, "X-Hugpy-Parent-Request-Id": rid, **link.headers()}
    if request.headers.get("Accept"):
        headers["Accept"] = request.headers["Accept"]

    def refused(reason: str, status):
        """The allocated box refused the call: a fact, recorded by central, returned as is."""
        attempts.append({"box": name, "status": status, "error": reason, "at": time.time()})
        record = app.get(REFUSED)
        if record is not None:
            record(name, call.model, call.options, reason, status, rid)
        S.update_call(rid, box=name, state="refused", http_status=503, attempts=attempts,
                      responded_at=time.time(), error=f"{name} refused: {reason}")
        return _err(503, f"box {name!r} refused the call it was allocated: {reason}", "box_refused",
                    reasons={name: reason}, path=d.path, why=d.why.get(name), request_id=rid)

    try:
        if selected is None or not selected.online:
            S.update_call(rid, box=name, state='refused', http_status=503,
                          responded_at=time.time(), error='worker observation expired before dispatch')
            return _err(503, 'worker observation expired before dispatch', 'stale_observation',
                        request_id=rid, worker=name)
        try:
            upstream = await session.post(link.url + request.path, data=body, headers=headers,
                                          timeout=aiohttp.ClientTimeout(total=None,
                                                                        sock_connect=C.CONNECT_TIMEOUT_S,
                                                                        sock_read=C.FIRST_BYTE_TIMEOUT_S))
        except (aiohttp.ClientError, OSError) as exc:
            return refused(f"unreachable: {exc}", None)
        if upstream.status >= 400:
            raw = await upstream.read()
            upstream.release()
            reason = _refusal(upstream.status, raw)
            if reason is not None:
                return refused(reason, upstream.status)
            attempts.append({"box": name, "status": upstream.status, "at": time.time()})
            S.update_call(rid, box=name, state="failed", http_status=upstream.status, attempts=attempts,
                          responded_at=time.time(), bytes_out=len(raw), error=f"box answered {upstream.status}")
            return web.Response(body=raw, status=upstream.status,
                                content_type=(upstream.headers.get("Content-Type") or "application/json").split(";")[0])
        attempts.append({"box": name, "status": upstream.status, "at": time.time()})
        extra = {}
        if ticket is not None:
            extra = {"X-Hugpy-Queue-Ticket": ticket.id, "X-Hugpy-Queue-Wait": f"{time.time() - ticket.arrived_at:.3f}"}
        return await _stream(request, upstream, rid, name, attempts, call, contracts, extra,
                             dispatch_identity=dispatch_identity)
    finally:
        if queue is not None and ticket is not None:
            queue.leave(ticket, free)


async def _stream(request, upstream, rid, name, attempts, call, contracts, extra=None,
                  *, dispatch_identity=None) -> web.StreamResponse:
    resp = web.StreamResponse(status=upstream.status)
    for h in PASS_RESPONSE_HEADERS:
        if h in upstream.headers:
            resp.headers[h] = upstream.headers[h]
    resp.headers["X-Hugpy-Router-Request-Id"] = rid
    resp.headers["X-Hugpy-Box"] = name
    for k, v in (extra or {}).items():
        resp.headers[k] = v
    sent, first_byte, state, error = 0, None, "done", None
    try:
        await resp.prepare(request)
        async for chunk in upstream.content.iter_any():
            if first_byte is None:
                first_byte = time.time()
            await resp.write(chunk)
            sent += len(chunk)
        await resp.write_eof()
        # Bind to the identity seen before dispatch, never to a later restart.
        contracts[(name, call.model)] = (*call.contract_key, dispatch_identity)
    except (ConnectionResetError, aiohttp.ClientError) as exc:
        state, error = "failed", f"stream cut: {exc}"
    finally:
        upstream.release()
        S.update_call(rid, box=name, state=state, http_status=upstream.status, attempts=attempts,
                      first_byte_at=first_byte, responded_at=time.time(), bytes_out=sent, error=error)
    return resp


async def models(request: web.Request) -> web.Response:
    """GET /v1/models: the union of the boxes' catalogs (which boxes hold each)."""
    denied = S.KEYS.check(RequestView(request), "use")
    if denied is not None:
        return web.json_response(denied[1], status=denied[0])
    seen: dict = {}
    for b in request.app[REGISTRY].boxes():
        if not b.online:
            continue
        resident = {r.key for r in b.residents}
        for k in sorted(b.models | resident):
            m = seen.setdefault(k, {"id": k, "object": "model", "owned_by": "hugpy", "boxes": [], "resident_on": []})
            m["boxes"].append(b.name)
            if k in resident:
                m["resident_on"].append(b.name)
    return web.json_response({"object": "list", "data": list(seen.values())})
