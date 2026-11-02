"""Harness session registry and per-session proxy: a named session's one route
from the fleet.

Direction (operator 2026-10-20): the harness is the client; it only calls out.
hugpy-agent is the inbound arm: it registers each harness session with Core
(`POST /api/sessions/register`), keeps it fresh (`/beat`) and withdraws it
(`/remove`). Core then exposes the session as

    GET  /api/sessions                      the registry (online = seen within TTL)
    GET  /api/sessions/<sid>                the record (never the serve token)
    ANY  /api/sessions/<sid>/<rest>         proxied to <serve_url>/api/sessions/<sid>/<rest>

so a web page, another arm or an operator script reaches "session X" through
Core without knowing which box, port or token the serve is on. The proxied hop
carries the serve's Bearer token from the record; a loopback-only serve
(`local_only`) is listed but not proxied (409 with the reason).

Access control is the /api gate the rest of Core's routes sit behind (the box
registers with its fleet key, exactly as the agent node registry does).
Records live in Core's own database (sql/044_agent_sessions.sql).
"""
from __future__ import annotations

import json
import socket
import time
from contextlib import contextmanager

import psycopg
from psycopg.types.json import Jsonb
import requests
from flask import Response, request, stream_with_context
from abstract_flask import get_bp, register_categories, spec

agent_sessions_bp, logger = get_bp("agent_sessions_bp", __name__)

ONLINE_TTL_S = 90.0          # three missed 30 s beats = offline
PROXY_TIMEOUT = (5, 120)
# Hop-by-hop headers, the caller's own credentials, AND the browser's origin
# headers: the proxied hop is Core talking to a serve, not the browser — a
# forwarded Origin makes the harness's same-origin check (loopback, no token)
# refuse every POST from the console.
_HOP_HEADERS = {"connection", "content-length", "host", "transfer-encoding", "keep-alive",
                "proxy-authenticate", "proxy-authorization", "te", "trailer", "upgrade", "authorization",
                "origin", "referer", "cookie"}
_FIELDS = ("locus", "name", "route", "serve_url", "serve_token", "local_only", "model", "base", "mode", "pin", "status")


@contextmanager
def _connect():
    from hugpy_core.imports.functions import core_dsn
    with psycopg.connect(core_dsn(), connect_timeout=5) as conn:
        yield conn


def _same_host(row: dict) -> bool:
    """A loopback-only serve IS reachable when it runs on Core's own box: the
    Core host's helper sessions (the console's Station tab, the brain) register
    from 127.0.0.1 with the box's hostname; Core compares it with its own."""
    host = str((row.get("doc") or {}).get("host") or "")
    return bool(host) and host == socket.gethostname()


def _public(row: dict) -> dict:
    out = {k: v for k, v in row.items() if k != "serve_token"}
    out["has_token"] = bool(row.get("serve_token"))
    out["online"] = (time.time() - float(row.get("seen_at") or 0)) <= ONLINE_TTL_S
    out["routable"] = not row.get("local_only") or _same_host(row)
    return out


class Store:
    """SQL-backed registry; tests swap in a MemoryStore with the same methods."""

    def upsert(self, rec: dict) -> dict:
        now = time.time()
        with _connect() as conn:
            conn.execute(
                "INSERT INTO agent_sessions(session_id, locus, name, route, serve_url, serve_token, local_only,"
                " model, base, mode, pin, status, registered_at, seen_at, doc)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                " ON CONFLICT (session_id) DO UPDATE SET locus=EXCLUDED.locus, name=EXCLUDED.name,"
                " route=EXCLUDED.route, serve_url=EXCLUDED.serve_url, serve_token=EXCLUDED.serve_token,"
                " local_only=EXCLUDED.local_only, model=EXCLUDED.model, base=EXCLUDED.base, mode=EXCLUDED.mode,"
                " pin=EXCLUDED.pin, status=EXCLUDED.status, seen_at=EXCLUDED.seen_at, doc=EXCLUDED.doc",
                (rec["session_id"], rec["locus"], rec["name"], rec["route"], rec["serve_url"], rec["serve_token"],
                 rec["local_only"], rec["model"], rec["base"], rec["mode"], rec["pin"], rec["status"], now, now,
                 Jsonb(rec.get("doc") or {})))
            conn.commit()
        return self.get(rec["session_id"])

    def beat(self, session_id: str, updates: dict) -> dict | None:
        with _connect() as conn:
            row = conn.execute("SELECT 1 FROM agent_sessions WHERE session_id=%s", (session_id,)).fetchone()
            if not row:
                return None
            conn.execute(
                "UPDATE agent_sessions SET seen_at=%s, status=COALESCE(%s, status), model=COALESCE(%s, model),"
                " name=COALESCE(%s, name) WHERE session_id=%s",
                (time.time(), updates.get("status"), updates.get("model"), updates.get("name"), session_id))
            conn.commit()
        return self.get(session_id)

    def remove(self, session_id: str) -> bool:
        with _connect() as conn:
            cur = conn.execute("DELETE FROM agent_sessions WHERE session_id=%s", (session_id,))
            conn.commit()
            return cur.rowcount > 0

    def get(self, session_id: str) -> dict | None:
        with _connect() as conn:
            cur = conn.execute("SELECT * FROM agent_sessions WHERE session_id=%s", (session_id,))
            row = cur.fetchone()
            if not row:
                return None
            return dict(zip([d[0] for d in cur.description], row))

    def list(self, locus: str = "") -> list[dict]:
        with _connect() as conn:
            if locus:
                cur = conn.execute("SELECT * FROM agent_sessions WHERE locus=%s ORDER BY seen_at DESC", (locus,))
            else:
                cur = conn.execute("SELECT * FROM agent_sessions ORDER BY seen_at DESC")
            names = [d[0] for d in cur.description]
            return [dict(zip(names, r)) for r in cur.fetchall()]


class MemoryStore:
    """Same contract, in memory (tests and the showroom)."""

    def __init__(self):
        self.rows = {}

    def upsert(self, rec):
        now = time.time()
        prior = self.rows.get(rec["session_id"]) or {}
        self.rows[rec["session_id"]] = {**rec, "doc": rec.get("doc") or {},
                                        "registered_at": prior.get("registered_at", now), "seen_at": now}
        return dict(self.rows[rec["session_id"]])

    def beat(self, session_id, updates):
        row = self.rows.get(session_id)
        if not row:
            return None
        row["seen_at"] = time.time()
        for k in ("status", "model", "name"):
            if updates.get(k) is not None:
                row[k] = updates[k]
        return dict(row)

    def remove(self, session_id):
        return self.rows.pop(session_id, None) is not None

    def get(self, session_id):
        row = self.rows.get(session_id)
        return dict(row) if row else None

    def list(self, locus=""):
        rows = [dict(r) for r in self.rows.values() if not locus or r.get("locus") == locus]
        return sorted(rows, key=lambda r: -r["seen_at"])


_STORE = None


def store():
    global _STORE
    if _STORE is None:
        _STORE = Store()
    return _STORE


def _record(body: dict) -> dict:
    sid = body.get("session_id")
    if not isinstance(sid, str) or not sid.strip() or len(sid) > 128:
        raise ValueError("session_id is required")
    url = body.get("serve_url")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        raise ValueError("serve_url must be an http(s) URL")
    rec = {"session_id": sid.strip(), "serve_url": url.rstrip("/"),
           "local_only": bool(body.get("local_only", False)), "doc": dict(body.get("doc") or {})}
    if isinstance(rec["doc"], dict) and isinstance(body.get("host"), str):
        rec["doc"]["host"] = body["host"][:255]
    for key in ("locus", "name", "route", "serve_token", "model", "base", "mode", "pin", "status"):
        value = body.get(key, "")
        if value is None:
            value = ""
        if not isinstance(value, str) or len(value) > 512:
            raise ValueError(key + " must be a short string")
        rec[key] = value
    rec["route"] = rec["route"] or "session:" + rec["session_id"]
    rec["status"] = rec["status"] or "idle"
    if not isinstance(rec["doc"], dict):
        raise ValueError("doc must be an object")
    return rec


def register_session(**body):
    try:
        rec = _record(body)
    except ValueError as exc:
        return {"error": str(exc)}, 400
    return _public(store().upsert(rec)), 200


def beat_session(session_id=None, status=None, model=None, name=None):
    if not isinstance(session_id, str) or not session_id:
        return {"error": "session_id is required"}, 400
    row = store().beat(session_id, {"status": status, "model": model, "name": name})
    if row is None:
        return {"error": "Unknown session; register it first"}, 404
    return _public(row), 200


def remove_session(session_id=None):
    if not isinstance(session_id, str) or not session_id:
        return {"error": "session_id is required"}, 400
    return {"ok": True, "removed": store().remove(session_id)}, 200


def create_session(**body):
    """Create a named session ON a registered serve and record it at once.

    The console's Station tab (and the helper) need a session without waiting
    for the box's next registration beat. Body: {name?, profile?, directive?,
    init_prompt?, settings?, locus?, via?}. The serve is chosen from the
    registry: `via` = an existing session_id on the wanted serve, else the first
    routable record for `locus`, else the first routable record on Core's own
    host. The new record copies that serve's url/token/host/locus; the box's
    registrar beats it from then on."""
    rows = store().list(str(body.get("locus") or ""))
    template = None
    if body.get("via"):
        template = store().get(str(body["via"]))
    if template is None:
        candidates = [r for r in rows if not r.get("local_only") or _same_host(r)]
        if not body.get("locus"):
            candidates.sort(key=lambda r: (not _same_host(r), -float(r.get("seen_at") or 0)))
        template = candidates[0] if candidates else None
    if template is None:
        return {"error": "No routable session serve is registered%s; start `hugpy-agent serve --central` on a box"
                         % (" for locus " + body["locus"] if body.get("locus") else "")}, 404
    payload = {k: body[k] for k in ("name", "profile", "directive", "init_prompt", "settings") if body.get(k) is not None}
    headers = {"Content-Type": "application/json"}
    if template.get("serve_token"):
        headers["Authorization"] = "Bearer " + template["serve_token"]
    try:
        upstream = requests.post(template["serve_url"] + "/api/sessions", json=payload, headers=headers, timeout=(5, 30))
    except requests.RequestException as exc:
        return {"error": "Session serve unreachable: %s" % exc}, 502
    try:
        created = upstream.json()
    except ValueError:
        created = {}
    if upstream.status_code != 201 or not isinstance(created, dict) or not created.get("id"):
        return {"error": (created or {}).get("error") or "serve refused: HTTP %s" % upstream.status_code}, 502
    rec = {"session_id": created["id"], "serve_url": template["serve_url"], "serve_token": template.get("serve_token") or "",
           "local_only": bool(template.get("local_only")), "locus": template.get("locus") or "",
           "name": created.get("name") or "", "route": created.get("route") or "session:" + created["id"],
           "model": created.get("model") or "", "base": (created.get("settings") or {}).get("base") or "",
           "mode": (created.get("settings") or {}).get("mode") or "", "pin": "",
           "status": created.get("status") or "idle", "doc": dict(template.get("doc") or {})}
    return _public(store().upsert(rec)), 201


def list_sessions(locus="", online=None):
    rows = [_public(r) for r in store().list(locus or "")]
    if str(online) in ("1", "true", "yes"):
        rows = [r for r in rows if r["online"]]
    return {"sessions": rows}, 200


def get_session(sid):
    row = store().get(sid)
    if row is None:
        return {"error": "Unknown session"}, 404
    return _public(row), 200


def proxy_session(sid, rest):
    row = store().get(sid)
    if row is None:
        return {"error": "Unknown session"}, 404
    if row.get("local_only") and not _same_host(row):
        return {"error": "This session's serve is loopback-only on its box; it is listed, not routable. "
                         "Start the serve with a token on a reachable address to route it."}, 409
    url = row["serve_url"] + "/api/sessions/" + sid + ("/" + rest if rest else "")
    if request.query_string:
        url += "?" + request.query_string.decode("ascii", "replace")
    headers = {k: v for k, v in request.headers if k.lower() not in _HOP_HEADERS}
    if row.get("serve_token"):
        headers["Authorization"] = "Bearer " + row["serve_token"]
    try:
        upstream = requests.request(request.method, url, headers=headers, data=request.get_data(),
                                    stream=True, timeout=PROXY_TIMEOUT, allow_redirects=False)
    except requests.RequestException as exc:
        return {"error": "Session serve unreachable: %s" % exc}, 502
    response_headers = [(k, v) for k, v in upstream.headers.items() if k.lower() not in _HOP_HEADERS]

    def body():
        try:
            yield from upstream.raw.stream(65536, decode_content=False)
        finally:
            upstream.close()

    return Response(stream_with_context(body()), status=upstream.status_code,
                    headers=response_headers, direct_passthrough=True)


# ── a session as a /v1 model (operator 2026-10-24) ───────────────────────────
# A named session is a dedicated, dynamic endpoint: `model: "session:<ref>"` on
# Core's /v1/chat/completions runs ONE turn in that session — its own model,
# directive and context — and answers in the OpenAI shape. <ref> is the session
# id, its unique name, or <locus>/<name>. /v1/models lists the online sessions.
SESSION_PREFIX = "session:"
TURN_POLL_S = 0.3
TURN_MAX_S = 1800.0


class SessionCallError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def _reachable(rows):
    return [r for r in rows if _public(r)["online"] and (not r.get("local_only") or _same_host(r))]


def _model_id(row, rows):
    name = str(row.get("name") or "").strip()
    if not name:
        return SESSION_PREFIX + row["session_id"]
    same = [r for r in rows if str(r.get("name") or "").strip().casefold() == name.casefold()]
    return SESSION_PREFIX + (name if len(same) == 1 else "%s/%s" % (row.get("locus") or "", name))


def resolve_session(ref: str) -> dict:
    """The online, routable session a `session:<ref>` model names."""
    ref = ref[len(SESSION_PREFIX):] if ref.startswith(SESSION_PREFIX) else ref
    ref = ref.strip()
    if not ref:
        raise SessionCallError("Name a session: session:<name>, session:<locus>/<name> or session:<id>")
    rows = _reachable(store().list(""))
    exact = [r for r in rows if r["session_id"] == ref]
    if not exact and "/" in ref:
        locus, name = ref.split("/", 1)
        exact = [r for r in rows if (r.get("locus") or "") == locus
                 and str(r.get("name") or "").casefold() == name.casefold()]
    if not exact:
        exact = [r for r in rows if str(r.get("name") or "").casefold() == ref.casefold()]
    if len(exact) > 1:
        raise SessionCallError("Ambiguous session %r; use one of: %s" % (
            ref, ", ".join(_model_id(r, rows) + " (" + SESSION_PREFIX + r["session_id"] + ")" for r in exact)), 409)
    if not exact:
        raise SessionCallError("No online session %r (GET /api/sessions lists them)" % ref, 404)
    return exact[0]


def session_models() -> list:
    rows = _reachable(store().list(""))
    return [{"id": _model_id(r, rows), "object": "model", "created": 0, "owned_by": "hugpy-session",
             "available": True, "session": SESSION_PREFIX + r["session_id"], "locus": r.get("locus"),
             "name": r.get("name"), "model": r.get("model"), "tasks": ["text-generation"]}
            for r in rows]


def _serve(row, method, rest="", body=None, params=None):
    headers = {"Content-Type": "application/json"}
    if row.get("serve_token"):
        headers["Authorization"] = "Bearer " + row["serve_token"]
    url = row["serve_url"] + "/api/sessions/" + row["session_id"] + ("/" + rest if rest else "")
    r = requests.request(method, url, json=body, params=params, headers=headers, timeout=PROXY_TIMEOUT)
    try:
        doc = r.json()
    except ValueError:
        doc = {}
    if r.status_code >= 400:
        raise SessionCallError("session %s: %s" % (row["session_id"], doc.get("error") or r.text[:300]),
                               r.status_code if r.status_code < 500 else 502)
    return doc


def _prompt(messages) -> str:
    """The turn's text: the last user message. The session keeps its own
    history, so earlier messages are context the caller already gave it."""
    for m in reversed(messages or []):
        if isinstance(m, dict) and m.get("role") == "user":
            c = m.get("content")
            if isinstance(c, list):
                c = "\n".join(p.get("text", "") for p in c if isinstance(p, dict) and p.get("type") == "text")
            if isinstance(c, str) and c.strip():
                return c
    raise SessionCallError("A session turn needs a user message")


def session_turn(row, text):
    """Run one turn and yield ("delta"|"final"|"question"|"error", value)."""
    view = _serve(row, "GET")
    if view.get("status") == "running":
        raise SessionCallError("Session %s is busy with another turn" % _model_id(row, [row]), 409)
    after = int(view.get("cursor") or 0)
    _serve(row, "POST", "messages", {"text": text, "by": "v1"})
    started, began = time.monotonic(), False
    while time.monotonic() - started < TURN_MAX_S:
        view = _serve(row, "GET", params={"after": after})
        for ev in view.get("events") or []:
            after = max(after, int(ev.get("id") or 0))
            kind, data = ev.get("kind"), ev.get("data")
            began = True
            if kind == "delta" and data:
                yield "delta", data if isinstance(data, str) else str(data)
            elif kind in ("final", "assistant", "reply"):
                answer = data if isinstance(data, str) else (data or {}).get("answer", "")
                if answer:
                    yield "final", answer
            elif kind == "error":
                yield "error", data if isinstance(data, str) else json.dumps(data)
        if view.get("pending"):
            yield "question", view["pending"]
            return
        if view.get("status") != "running" and (began or time.monotonic() - started > 5):
            return
        time.sleep(TURN_POLL_S)
    yield "error", "the session turn did not finish within %ds" % TURN_MAX_S


def _question_text(q, row, rows):
    opts = ", ".join(str(o) for o in q.get("options") or [])
    return ("\n[%s is waiting for an answer: %s%s — answer it in the Station or POST "
            "/api/sessions/%s/answer {id: %s, choice}]" % (
                _model_id(row, rows), q.get("question", ""), (" (" + opts + ")") if opts else "",
                row["session_id"], q.get("id")))


def session_chat(payload: dict):
    """/v1/chat/completions for `model: "session:<ref>"`."""
    import uuid
    from flask import jsonify
    from hugpy_core.relay.openai import openai_error

    def _err(message, status, err_type="invalid_request_error"):
        resp, code = openai_error(message, status, err_type)
        resp.status_code = code
        return resp

    # A session runs a tool-capable agent on its box: operator surface, the same
    # management gate as the Station terminal — a guest or "use" key never reaches it.
    from hugpy_core.router.observability import store as routing

    class RequestView:
        client_address = (request.remote_addr or "", 0)
        headers = request.headers
    denied = routing.KEYS.check(RequestView(), "admin")
    # The admin gate passes this box's own address before it reads a key, and
    # guest/public passes arrive from this box (nginx, GuestAccess) carrying their
    # "use" key: any key that IS presented must be an admin key.
    auth = request.headers.get("Authorization", "")
    key = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
    if not denied and key and routing.KEYS.scope_of(key) != "admin":
        denied = (403, {"error": "session models require an operator (admin) key"})
    if denied:
        status, body = denied
        err = body.get("error")
        return _err((err.get("message") if isinstance(err, dict) else err)
                    or "session models require an operator key", status, "permission_error")

    try:
        row = resolve_session(payload["model"])
        text = _prompt(payload.get("messages"))
    except SessionCallError as exc:
        return _err(str(exc), exc.status)
    rows = _reachable(store().list(""))
    model = _model_id(row, rows)
    cid, created = "chatcmpl-" + uuid.uuid4().hex, int(time.time())
    served = {"session": SESSION_PREFIX + row["session_id"], "locus": row.get("locus"),
              "session_model": row.get("model")}

    if payload.get("stream"):
        def chunk(delta, finish=None):
            body = {"id": cid, "object": "chat.completion.chunk", "created": created, "model": model,
                    "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}
            if finish:
                body["hugpy"] = served
            return ("data: " + json.dumps(body, ensure_ascii=False) + "\n\n").encode("utf-8")

        def sse():
            yield chunk({"role": "assistant", "content": ""})
            streamed = False
            try:
                for kind, value in session_turn(row, text):
                    if kind == "delta":
                        streamed = True
                        yield chunk({"content": value})
                    elif kind == "final" and not streamed:
                        yield chunk({"content": value})
                    elif kind == "question":
                        yield chunk({"content": _question_text(value, row, rows)})
                    elif kind == "error":
                        yield chunk({"content": "\n[error: %s]" % value})
            except SessionCallError as exc:
                yield chunk({"content": "\n[error: %s]" % exc})
            yield chunk({}, finish="stop")
            yield b"data: [DONE]\n\n"

        return Response(stream_with_context(sse()), mimetype="text/event-stream",
                        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    parts, final, errors = [], None, []
    try:
        for kind, value in session_turn(row, text):
            if kind == "delta":
                parts.append(value)
            elif kind == "final":
                final = value
            elif kind == "question":
                parts.append(_question_text(value, row, rows))
            elif kind == "error":
                errors.append(value)
    except SessionCallError as exc:
        return _err(str(exc), exc.status)
    content = final if final is not None else "".join(parts)
    if errors and not content:
        return _err("; ".join(errors), 502, "api_error")
    return jsonify({"id": cid, "object": "chat.completion", "created": created, "model": model,
                    "choices": [{"index": 0, "message": {"role": "assistant", "content": content},
                                 "finish_reason": "stop"}],
                    "hugpy": {**served, **({"errors": errors} if errors else {})}})


_METHODS = ["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
# Dict nesting is the path. The registry/lifecycle endpoints parse only query or
# JSON-body fields, so they are plain kwargs-form handlers answering bare JSON
# (``response="native"``). The per-session proxy is the one raw-request
# passthrough: it reads the live method/headers/body and streams the serve's
# reply, so it keeps ``inputs="path"`` and returns a Flask ``Response``.
ALL_CATEGORIES = {
    "sessions": {
        "": spec(list_sessions, "GET", response="native"),            # /sessions?locus=&online=
        "register": spec(register_session, "POST", response="native"),
        "beat": spec(beat_session, "POST", response="native"),
        "remove": spec(remove_session, "POST", response="native"),
        "create": spec(create_session, "POST", response="native"),
        "<sid>": {
            "": spec(get_session, "GET", response="native"),          # /sessions/<sid>
            "<path:rest>": spec(proxy_session, _METHODS, response="native",
                                inputs="path", strict_slashes=True),  # /sessions/<sid>/<path:rest>
        },
    },
}
register_categories(agent_sessions_bp, ALL_CATEGORIES)
