"""The console Help panel's backend (HelpPanel.jsx → /api/llm/help/…).

LIFTED from legacy ``hugpy_server.app.routes.help_routes`` + ``help_agent`` into
core. Those routes 404'd on core since legacy central went off 2026-10-03; the
panel's "operator · logs, code, tests" tag showed HTTP 404 on every open.

WHAT THE HELP AGENT IS HERE
---------------------------
Legacy ran the agent on one of two backends (help_agent.py):

  * ``ClaudeArmBackend`` — a headless Claude Code session on an *abstract-claude
    serve* console API (:9125 / :9123), with file + shell tools, that could read
    logs and EDIT CODE under the source tree. Those serve ports are still
    reachable, BUT routing a help turn through them bypasses the call log, which
    the operator's call-record doctrine forbids. So this lift does NOT use the
    Claude arm: it is reported as a known, deliberate gap (the panel shows
    ``tools:false`` → "local model, read-only", honestly).
  * ``LocalModelBackend`` — hugpy's own /v1, chat only, read-only. THIS is what
    core serves: the turn rides core's own ``POST /v1/chat/completions`` so it
    lands in ``hugpy_wrapper.call_log`` with ``metadata.intent='help-agent'``
    (``_relay_chat``). The model is grounded with a bounded read-only snapshot
    of the live fleet (workers + recent errored calls) built from core's own
    registry and the call log — no canned text.

If no help model can be resolved (none configured, no online worker serving one)
the turn records an honest ``done`` error naming that — never a fake reply.

STATE lives in the core DB (help_store, sql/017_help.sql), not JSON files.

GATE: core's auth posture is "open" today (routes.auth_config; the console fakes
login, LAN/WG-only is enforced at nginx), so ``_gate`` allows every caller, the
same single-hook shape as settings.operator_only — central auth plugs in here
later. ``HUGPY_HELP_AGENT=0`` turns the whole surface off with an honest 503.
"""
from __future__ import annotations

import json
import os
import threading
import time
import uuid

from flask import Response, request, stream_with_context

from hugpy_core.help import help_store
from hugpy_core.registry import registry


MAX_PROMPT = 20000
MAX_CONTEXT = 6000
HELP_INTENT = "help-agent"
STREAM_MAX_S = float(os.environ.get("HUGPY_HELP_STREAM_MAX_S", "900"))
STREAM_POLL_S = float(os.environ.get("HUGPY_HELP_STREAM_POLL_S", "1.0"))
BACKEND_NAME = "local-model"
BACKEND_LABEL = "hugpy /v1 relay — read-only, no tools"


def _enabled() -> bool:
    return (os.environ.get("HUGPY_HELP_AGENT", "1") or "").strip().lower() not in (
        "0", "false", "no", "off")


def _gate():
    """None when the caller may use the help agent; a (payload, code) otherwise.
    Open today (see module docstring); only the disable flag denies. The payload
    is a JSON-able dict (the native registrar serves it bare, same 503 body)."""
    if not _enabled():
        return {"error": "the help agent is disabled on this deployment "
                         "(HUGPY_HELP_AGENT=0)"}, 503
    return None


def _disabled():
    """The keeper widget's disabled-gate as a plain dict (honest 503 text), or
    None when the help agent is enabled (open gate otherwise, see docstring)."""
    if not _enabled():
        return {"error": "the help agent is disabled on this deployment "
                         "(HUGPY_HELP_AGENT=0)"}
    return None


def _who() -> str:
    # No operator identity on the open gate; the console labels the session.
    return (request.headers.get("X-Operator-User") or "operator").strip() or "operator"


def _clamp_since(value) -> int:
    """A non-negative integer cursor from a ``since`` kwarg (query/body); 0 on
    anything non-numeric. Same clamp the legacy ``?since=`` read used."""
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _since() -> int:
    # The SSE stream is a raw-request proxy (it returns a streaming Response);
    # it reads its own ``?since=`` cursor here.
    return _clamp_since(request.args.get("since"))


def _clip(value, limit: int) -> str:
    text = value if isinstance(value, str) else ("" if value is None else str(value))
    text = text.strip()
    return text if len(text) <= limit else text[:limit]


def _format_context(context) -> str:
    if not context:
        return ""
    if isinstance(context, str):
        return _clip(context, MAX_CONTEXT)
    if isinstance(context, dict):
        lines = []
        for k, v in context.items():
            if v in (None, "", [], {}):
                continue
            if not isinstance(v, str):
                v = json.dumps(v, default=str)
            lines.append(f"- {k}: {v}")
        return _clip("\n".join(lines), MAX_CONTEXT)
    return _clip(str(context), MAX_CONTEXT)


def _no_session(sid: str):
    """404 body naming what was looked for and why (honest, not a bare 404)."""
    if not help_store.valid_id(sid):
        why = f"id does not match the session id format {help_store.ID_RX_PATTERN!r}"
    else:
        why = "no session row in help_sessions"
    return {"error": f"no help session {sid!r}: {why}", "session": sid}, 404


# ── read-only grounding (live fleet facts for the no-tools model) ─────────────
def _grounding_snapshot() -> str:
    workers = []
    try:
        for w in registry.all_workers():
            v = registry.public_view(w)
            workers.append({k: v.get(k) for k in ("id", "name", "status", "version", "pool")})
    except Exception:  # noqa: BLE001 — a read surface never raises into a turn
        workers = []
    errored = []
    try:
        from hugpy_core.calllog import calllog
        for c in calllog.calls(limit=60):
            if not c.get("error"):
                continue
            errored.append({"model": c.get("model_name"), "worker": c.get("worker"),
                            "http": c.get("http_status"),
                            "error": _clip(c.get("error"), 300),
                            "at": c.get("received_at")})
            if len(errored) >= 15:
                break
    except Exception:  # noqa: BLE001
        errored = []
    return json.dumps({"workers": workers, "recent_errored_calls": errored}, default=str)[:12000]


def _resolve_model() -> "str | None":
    """The Hugpy Keeper is Coder Next unless the operator explicitly changes it."""
    return (os.environ.get("HUGPY_HELP_MODEL") or "").strip() or "Qwen3-Coder-Next-Q4_K_M"


def _messages(history: list, text: str, ctx_text: str) -> list:
    sys_msg = ("You are the hugpy HELP AGENT in read-only mode: you have no tools, you "
               "cannot read files or run commands. Answer from the live fleet facts below; "
               "when the answer needs code or a log you cannot see, say so plainly and tell "
               "the operator exactly what to run.\n\nLIVE FLEET FACTS (read-only snapshot):\n"
               + _grounding_snapshot())
    msgs = [{"role": "system", "content": sys_msg}]
    buf = ""
    for r in history:
        if r.get("kind") == "user":
            if buf:
                msgs.append({"role": "assistant", "content": buf})
                buf = ""
            msgs.append({"role": "user", "content": r.get("text", "")})
        elif r.get("kind") == "event" and r.get("type") == "text":
            buf += r.get("text", "")
    if buf:
        msgs.append({"role": "assistant", "content": buf})
    user = text if not ctx_text else f"{text}\n\n(console context)\n{ctx_text}"
    msgs.append({"role": "user", "content": user})
    return msgs[-24:] if len(msgs) > 24 else msgs


def _relay_chat(model: str, messages: list, by: str) -> "tuple[str, str]":
    """Run one help turn through Core's direct chat service so it is logged
    in hugpy_wrapper.call_log (metadata.intent 'help-agent'). Returns (reply,
    model_that_answered). Raises RuntimeError with the real error text on failure."""
    body = {"model": model, "messages": messages, "max_tokens": 1200, "temperature": 0.2,
            "max_chunks": 1,
            "metadata": {"intent": HELP_INTENT, "help_by": by}}
    from hugpy_core.relay.internal import chat
    out, status = chat(body, caller="help")
    if status >= 400:
        error = out.get("error")
        message = error.get("message") if isinstance(error, dict) else error
        raise RuntimeError(f"Core relay {status}: {message}")
    choices = out.get("choices") or []
    reply = ((choices[0].get("message") or {}).get("content") if choices else "") or ""
    if not reply.strip():
        raise RuntimeError("the help model returned an empty reply")
    return reply, out.get("model") or model


def _run_turn(sid: str, text: str, ctx_text: str, history: list, mid: str, by: str) -> None:
    model = _resolve_model()
    if not model:
        help_store.append(sid, {"kind": "event", "type": "done", "rc": 1,
                                "error": "no help model is configured and no online worker "
                                         "serves one (set HUGPY_HELP_MODEL or bring a worker "
                                         "online)", "message_ids": [mid]})
        return
    try:
        reply, answered = _relay_chat(model, _messages(history, text, ctx_text), by)
    except Exception as exc:  # noqa: BLE001 — the error IS the recorded turn
        help_store.append(sid, {"kind": "event", "type": "done", "rc": 1,
                                "error": str(exc), "message_ids": [mid]})
        return
    help_store.append(sid,
                      {"kind": "event", "type": "text", "text": reply, "model": answered},
                      {"kind": "event", "type": "done", "rc": 0, "message_ids": [mid],
                       "model": answered})


def _start_turn(sid: str, text: str, ctx_text: str, by: str) -> None:
    """Append the inbound user record and run the reply in the background."""
    mid = uuid.uuid4().hex
    history = help_store.read(sid)
    help_store.append(sid, {"kind": "user", "text": text, "context": ctx_text,
                            "message_ids": [mid]})
    threading.Thread(target=_run_turn, args=(sid, text, ctx_text, history, mid, by),
                     daemon=True, name=f"help-{sid}").start()


# ── routes (exactly what HelpPanel.jsx calls) ────────────────────────────────
# Kwargs in (body/query fields + the URL path params, merged by the registrar),
# JSON-able out; the routes module registers each at response="native" so the
# bare shape and status code below are served verbatim. Operator identity rides
# the X-Operator-User header (_who), not a mergeable field, so it is read there.
def help_sessions_list():
    g = _gate()
    if g is not None:
        return g
    return {"sessions": help_store.list_sessions()}


def help_sessions_start(prompt=None, context=None, **_):
    g = _gate()
    if g is not None:
        return g
    prompt = _clip(prompt, MAX_PROMPT)
    if not prompt:
        return {"error": "prompt is required"}, 400
    by = _who()
    sid = help_store.create_session(by=by, backend=BACKEND_NAME, backend_label=BACKEND_LABEL,
                                    tools=False)
    help_store.append(sid, {"kind": "backend", "backend": BACKEND_NAME, "label": BACKEND_LABEL})
    _start_turn(sid, prompt, _format_context(context), by)
    return help_store.transcript(sid), 201


def help_session_get(sid, since=0, **_):
    g = _gate()
    if g is not None:
        return g
    try:
        return help_store.transcript(sid, since=_clamp_since(since))
    except KeyError:
        return _no_session(sid)


def help_session_delete(sid, **_):
    g = _gate()
    if g is not None:
        return g
    try:
        if not help_store.delete_session(sid):
            return _no_session(sid)
    except ValueError as exc:
        return {"error": str(exc)}, 409
    return {"deleted": sid}


def help_session_send(sid, text=None, context=None, **_):
    g = _gate()
    if g is not None:
        return g
    if not help_store.exists(sid):
        return _no_session(sid)
    text = _clip(text, MAX_PROMPT)
    if not text:
        return {"error": "text is required"}, 400
    _start_turn(sid, text, _format_context(context), _who())
    return help_store.transcript(sid)


def help_session_stop(sid, **_):
    g = _gate()
    if g is not None:
        return g
    if not help_store.exists(sid):
        return _no_session(sid)
    # No tools backend to interrupt here; the record flips the derived status so
    # a still-running /v1 turn's late reply is shown but the panel stops waiting.
    help_store.append(sid, {"kind": "stopped", "error": None})
    return help_store.transcript(sid)


def help_session_stream(sid):
    """SSE: every transcript record from ``since`` on as it lands, one ``status``
    frame per change; ends when the session leaves 'busy' (after a poll) or after
    HUGPY_HELP_STREAM_MAX_S. Shape verbatim of the legacy stream."""
    g = _gate()
    if g is not None:
        return g
    if not help_store.exists(sid):
        return _no_session(sid)
    start_at = _since()

    def gen():
        cursor = start_at
        last_status = None
        deadline = time.time() + STREAM_MAX_S
        idle_polls = 0
        while time.time() < deadline:
            t = help_store.transcript(sid, since=cursor)
            for rec in t["records"]:
                yield f"id: {rec['i']}\ndata: {json.dumps(rec, default=str)}\n\n"
                cursor = rec["i"] + 1
            if t["status"] != last_status:
                last_status = t["status"]
                yield f"event: status\ndata: {json.dumps({'status': last_status, 'count': t['count']})}\n\n"
            if last_status != "busy":
                idle_polls += 1
                if idle_polls >= 2:
                    return
            else:
                idle_polls = 0
                yield ": keepalive\n\n"
            time.sleep(STREAM_POLL_S)

    return Response(stream_with_context(gen()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── tickets (pre-existing approvals; empty until a filer is lifted) ───────────
def tickets_list(status=None, **_):
    """The approvals feed. ``?status=`` (now the ``status`` kwarg) filters it."""
    g = _gate()
    if g is not None:
        return g
    return {"tickets": help_store.list_tickets(status or None, 200),
            "pending": help_store.pending_count(), "keeper": False}


def help_ticket_act(tid, action=None, **_):
    """The operator's choice on one ticket. dismiss and discuss are served; the
    calibrate / keeper / approve actions depend on subsystems not lifted into
    core and return an honest 409 naming that (not a fake success)."""
    g = _gate()
    if g is not None:
        return g
    t = help_store.get_ticket(tid)
    if not t:
        return {"error": f"no help ticket {tid}"}, 404
    action = str(action or "").lower()
    if action == "dismiss":
        return help_store.set_ticket_status(tid, "dismissed", {"by": _who()})
    if action == "discuss":
        by = _who()
        detail = t.get("detail") or {}
        prompt = (f"A {t.get('kind')} ticket was filed: {t.get('title')}.\n"
                  f"model={t.get('model_key')} worker={t.get('worker_name') or t.get('worker_id')}\n"
                  f"detail={json.dumps(detail, default=str)[:2000]}\n"
                  "Explain the most likely cause and what should change.")
        sid = help_store.create_session(by=by, backend=BACKEND_NAME, backend_label=BACKEND_LABEL,
                                        tools=False)
        help_store.append(sid, {"kind": "backend", "backend": BACKEND_NAME, "label": BACKEND_LABEL})
        _start_turn(sid, prompt, _format_context({"ticket": t.get("id")}), by)
        out = help_store.set_ticket_status(tid, "acted", {"action": "discuss", "session": sid,
                                                          "by": by})
        return {"ticket": out, "session": help_store.transcript(sid)}
    if action == "approve" and t.get("kind") == "allocation":
        from hugpy_core.brain import brain
        ev = (t.get("detail") or {}).get("evaluation") or {}
        if ev.get("fix_kind") != "pull":
            return {"error": f"nothing to pull: {ev.get('reason') or 'no determination'}"}, 409
        res = brain.activate(t.get("model_key"), t.get("worker_name"))
        if not res.get("ok"):
            return {"error": res.get("why")}, 409
        out = help_store.set_ticket_status(tid, "acted", {"action": "pull", "by": _who(), **res})
        return {"ticket": out, "pull": res}
    if action == "approve" and t.get("kind") == "load-failure":
        # the operator approves the brain's fix → run the fix ladder (existing
        # environments → worker base + the packages); packages a below-threshold
        # brain left pending in an auto run are included
        from hugpy_core.brain import fix_ladder
        detail = t.get("detail") or {}
        ev = detail.get("evaluation") or {}
        lad = detail.get("ladder") or {}
        if lad.get("state") == "running" and fix_ladder.active_for(t.get("worker_name")) is not None:
            return {"error": "this ticket's fix ladder is already running — "
                             + (lad.get("now") or "see its progress on the ticket")}, 409
        pk = sorted(set(ev.get("packages") or []) | set(lad.get("need") or [])
                    | set(lad.get("pending_packages") or []))
        if not pk:
            return {"error": "the evaluation names no package to install — discuss it instead"}, 409
        started = fix_ladder.start(tid, worker=t.get("worker_name"), model_key=t.get("model_key"),
                                   packages=pk, by=_who())
        if not started.get("started"):
            return {"error": started.get("why"), "ladder": started}, 409
        return {"ticket": help_store.get_ticket(tid), "ladder": started}
    if action in ("calibrate", "keeper", "approve"):
        return {"error": f"the '{action}' ticket action is not available in core "
                         "(its subsystem is not lifted); dismiss or discuss it instead",
                "action": action}, 409
    return {"error": "action must be one of dismiss, discuss "
                     "(calibrate/keeper/approve are not available in core)"}, 400


# ── keeper widget (the floating Help widget: direct ask + file-a-fix) ─────────
# Plain kwargs handlers (the routes module registers these as the default
# callable leaf: GET+POST, answer wrapped as {"result": ...}). Moved here from
# help/routes.py so that module states only the URL tree.
def keeper_ask(question=None, text=None, context=None, history=None, operator="operator", **_):
    """The floating Help widget's direct, read-only Coder Next conversation."""
    d = _disabled()
    if d is not None:
        return d
    prompt = _clip(question or text, MAX_PROMPT)
    if not prompt:
        return {"ok": False, "error": "question is required"}
    messages = [{"role": "system", "content":
                 "You are the Hugpy Keeper and helper. Answer about this Hugpy fleet. "
                 "You have no tools or shell access; say when a fact needs checking. "
                 "Do not claim to have changed anything.\n\nLIVE FLEET FACTS:\n" + _grounding_snapshot()}]
    for row in (history if isinstance(history, list) else [])[-16:]:
        if isinstance(row, dict) and row.get("role") in ("user", "assistant"):
            value = _clip(row.get("content"), MAX_PROMPT)
            if value:
                messages.append({"role": row["role"], "content": value})
    ctx = _format_context(context)
    messages.append({"role": "user", "content": prompt + ("\n\n(console context)\n" + ctx if ctx else "")})
    model = _resolve_model()
    try:
        answer, served_model = _relay_chat(model, messages, operator or "operator")
    except RuntimeError as exc:
        return {"ok": False, "error": str(exc), "model": model}
    return {"ok": True, "answer": answer, "model": served_model,
            "why": "Hugpy Keeper uses Coder Next in read-only mode."}


def keeper_report(description=None, proposed_action=None, text=None, context=None, **_):
    """The widget's Request a fix form files a pending ticket for approval."""
    d = _disabled()
    if d is not None:
        return d
    description = _clip(description or text, MAX_PROMPT)
    if not description:
        return {"ok": False, "error": "description is required"}
    tid = help_store.file_operator_ticket(description, _clip(proposed_action, MAX_CONTEXT),
                                          _format_context(context))
    return {"ok": True, "ticket_id": tid, "status": "pending"}
