"""
Chat router — POST /api/chat (SSE) and WS /api/ws/chat.

v3.3.6 — Rewritten to emit the dashboard's CURRENT event vocabulary
(``text`` / ``tool_start`` / ``tool_result`` / ``status`` / ``done`` /
``turn_start`` with monotonic ``seq`` and ``turn_id``), not the legacy
v2.x wire format (``assistant.delta`` / ``tool.started`` /
``tool.completed``) that the dashboard's ChatEvent type no longer
understands.

Sources of truth for the dashboard contract:
  - cvc/web/src/lib/types.ts   ``ChatEvent`` interface  (single source)
  - cvc/web/src/lib/api.ts     ``ChatWS`` class        (consumer)
  - cvc/gateway_chat.py        ``stream_unified_chat`` (legacy translator)

Sources of truth for the upstream agent loop:
  - cvc/agent/_vendor/hermes/run_agent.py      ``AIAgent``
  - cvc/agent/_vendor/hermes/gateway/platforms/api_server.py
        ``APIServerAdapter._run_agent`` / ``_write_sse_chat_completion``

The flow:
  1. Extract workspace_path from request (header or body field).
  2. Build AIAgent via ``cvc.gateway.agent.create_agent`` (cached, 1.8s
     amortized over the worker).
  3. Wire all 4 upstream callbacks (stream_delta, tool_start,
     tool_complete, tool_progress) into a single
     ``_enqueue_outbox_event()`` that normalizes them into the
     dashboard's ChatEvent vocabulary.
  4. Run the agent in a thread executor. Stream events from the
     outbox to the client as SSE / WS frames. Each frame carries a
     monotonic ``seq`` and the turn's ``turn_id`` (so the dashboard
     can dedup, resume on reconnect, and order the activity strip).
  5. Emit a ``ping`` keepalive every 30s so the dashboard's
     ``lastEventAt`` watchdog never shows the misleading
     "no stream events for 105s" banner during long tool calls.
  6. Emit ``done`` with final assistant text on agent completion.
  7. On disconnect, call ``agent.interrupt()`` so upstream LLM
     calls stop.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import threading
import time
import uuid
from typing import Any, AsyncIterator, Optional

from fastapi import APIRouter, Header, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

logger = logging.getLogger("cvc.gateway.chat")

router = APIRouter()


# Per-event keepalive — matches the upstream api_server's
# CHAT_COMPLETIONS_SSE_KEEPALIVE_SECONDS=30. Keeps the dashboard's
# activity strip honest and prevents the "95 seconds of silence"
# watchdog banner from firing during genuinely long tool calls.
_KEEPALIVE_SECONDS = 30.0


# v3.3.26 — Per-process delta instrumentation counters. Mutable single-element
# lists so the closure inside _on_delta can update them without ``global``.
# Tracked per-instance-of-daemon; resets on restart. Read by the
# ``/api/chat/diagnostics`` route below so the dashboard (and curl-based
# tests) can verify the gateway is actually streaming real deltas vs.
# delivering one big text event with the whole response.
_DELTA_COUNT: "list[int]" = [0]
_DELTA_TOTAL_CHARS: "list[int]" = [0]
_TOOL_COUNT: "list[int]" = [0]
_TURN_COUNT: "list[int]" = [0]


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

async def _resolve_workspace(
    body: dict[str, Any],
    x_cvc_workspace: Optional[str],
) -> Optional[str]:
    """Find the workspace the user is currently in.

    v3.4.13 — Resolution order:
      1. ``X-CVC-Workspace`` header (server-set by some channel adapters)
      2. ``body.workspace_path`` (set by the dashboard chat on every send)
      3. ``None`` — falls back to ``$HOME`` inside ``run_chat_turn``

    If we resolve to None we LOG A WARNING. Previously the request would
    silently fall back to ``$HOME``, the agent would treat ``$HOME`` as
    the workspace, and the user would see answers about a directory
    they never selected.
    """
    if x_cvc_workspace:
        return x_cvc_workspace
    ws = body.get("workspace_path")
    if ws:
        return str(ws)
    logger.warning(
        "chat request arrived WITHOUT workspace_path or X-CVC-Workspace; "
        "agent will fall back to $HOME. Frontend may have regressed."
    )
    return None


def _extract_user_message(messages: list[dict[str, Any]]) -> str:
    if not messages:
        return ""
    for m in reversed(messages):
        if m.get("role") == "user":
            content = m.get("content", "")
            if isinstance(content, list):
                return "".join(
                    c.get("text", "") for c in content if c.get("type") == "text"
                )
            return str(content)
    return ""


def _extract_conversation_history(messages: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Convert dashboard message format to vendored {role, content} pairs."""
    history: list[dict[str, str]] = []
    for m in messages:
        role = m.get("role")
        if role not in ("user", "assistant"):
            continue
        content = m.get("content", "")
        if isinstance(content, list):
            content = "".join(
                c.get("text", "") for c in content if c.get("type") == "text"
            )
        if content:
            history.append({"role": role, "content": str(content)})
    return history


def _sse(payload: dict[str, Any]) -> bytes:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode("utf-8")


def _sse_keepalive() -> bytes:
    return b": keepalive\n\n"


def _build_run_id(session_id: str) -> str:
    return f"run_{session_id[:12]}" if session_id else f"run_{uuid.uuid4().hex[:12]}"


# -----------------------------------------------------------------------------
# Callback wiring — upstream AIAgent callbacks → dashboard ChatEvent shapes.
# -----------------------------------------------------------------------------
#
# The upstream AIAgent (cvc/agent/_vendor/hermes/run_agent.py) exposes
# four callbacks that fire during a run:
#
#   stream_delta_callback(delta: str)
#       Fires for every text chunk the model emits. The model may emit
#       ``None`` as a sentinel between phases (e.g. before tool execution)
#       — the upstream api_server's SSE writer DROPS the None sentinel so
#       the HTTP response isn't prematurely closed. We do the same.
#
#   tool_start_callback(call_id, name, args)
#       Fires when the agent invokes a tool. ``call_id`` is the
#       provider-assigned tool_call_id (or auto-generated if missing).
#
#   tool_complete_callback(call_id, name, args, result)
#       Fires when the tool returns. ``result`` may be a string or a
#       structured dict depending on the tool.
#
#   tool_progress_callback(event_type, tool_name, preview, **kwargs)
#       The legacy "fire hose" emit. Fires for tool.started,
#       tool.completed, tool.failed, and progress events. Carries less
#       structure than the *_callback trio. We use it as a fallback
#       (when tool_start/complete didn't fire — they always do, so this
#       is a safety net).
#
# All four callbacks must marshal through the same outbox queue so the
# SSE / WS writer sees a strictly-ordered stream of dashboard events.

# -----------------------------------------------------------------------------
# Approval gate — v3.3.22
# -----------------------------------------------------------------------------
#
# Per-turn gate that holds ONE pending tool approval. Consulted inside
# ``_attach_outbox_callbacks``'s ``_on_tool_start`` BEFORE the upstream
# agent runs the tool. When the dashboard's ApprovalModeSwitcher pill is
# set to "Default", every non-safe tool call yields a ``tool_confirm``
# SSE event, blocks until the dashboard resolves it (via WS
# ``{"type":"confirm","result":...}`` or HTTP ``POST /api/chat/confirm``),
# and proceeds only on allow. On deny the agent sees a synthetic deny
# tool_result.
#
# Mode + safe-tools lookup:
#   ``cvc.gateway_legacy._approval_mode`` — "default" | "bypass" | "autopilot"
#   ``cvc.gateway_legacy._SAFE_TOOLS``     — read-only tool set (auto-allow)
#
# Shared with the dashboard's ApprovalModeSwitcher pill so flipping the
# pill to "Default" affects both the legacy and new chat paths simultaneously.

_VALID_DECISIONS = {
    "allow",
    "allow_once",
    "allow_always",
    "trust_all",
    "deny",
    "deny_suggest",
}


# v3.3.22 — Module-level registry of active per-turn approval gates.
# The HTTP ``/api/chat/confirm`` route uses this to reach a gate that lives
# inside a request handler's scope (and isn't directly accessible from
# outside that scope). Each chat endpoint registers its gate at construction
# time and unregisters on turn-end. The WS confirm path already has direct
# access to the gate via closure — this registry is the HTTP fallback.
_ACTIVE_GATES: dict[str, "_ApprovalGate"] = {}


def _register_gate(turn_id: str, gate: "_ApprovalGate") -> None:
    _ACTIVE_GATES[turn_id] = gate


def _unregister_gate(turn_id: str) -> None:
    _ACTIVE_GATES.pop(turn_id, None)


def _resolve_active_gate(turn_id: str | None = None) -> "_ApprovalGate | None":
    """Pick the gate to resolve via HTTP. Prefers the most recently registered
    one (matches the "current turn" heuristic the legacy confirm endpoint uses).
    If ``turn_id`` matches a known gate, that one wins.
    """
    if turn_id and turn_id in _ACTIVE_GATES:
        return _ACTIVE_GATES[turn_id]
    if _ACTIVE_GATES:
        return next(reversed(_ACTIVE_GATES.values()))
    return None


class _ApprovalGate:
    """One pending tool approval per turn. Single-slot, single-shot.

    Lifecycle:
        ``wait(call_id, tool_name, outbox)`` — emit ``tool_confirm`` to the
            outbox, block the agent thread until ``resolve()`` is called
            (from the WS reader or the HTTP confirm endpoint), then return
            the decision string.
        ``resolve(decision)`` — set the event + decision. Decision is
            normalised through ``_VALID_DECISIONS``.

    Threading: ``wait()`` is called from the agent's worker thread. It
    blocks on a ``threading.Event`` proxy while the asyncio loop drives
    the wire protocol. Matches the legacy agent_chat pattern.
    """

    __slots__ = (
        "loop",
        "_thread_evt",
        "_decision",
        "active_call_id",
        "active_tool_name",
        "timeout_s",
    )

    def __init__(self, loop: asyncio.AbstractEventLoop, timeout_s: float = 120.0) -> None:
        self.loop = loop
        self._thread_evt = threading.Event()
        self._decision: str = ""
        self.active_call_id: str = ""
        self.active_tool_name: str = ""
        self.timeout_s = timeout_s

    def wait(self, *, call_id: str, tool_name: str, outbox: "_ChatOutbox") -> str:
        """Block the calling thread until the user resolves the approval.

        Emits a ``tool_confirm`` event into the outbox so the dashboard can
        render the approval card. Returns one of the ``_VALID_DECISIONS``
        strings; ``"allow_once"`` is the default when the user doesn't
        explicitly choose (matches the v2.92.14 "full autonomy on timeout"
        rule from legacy gateway_legacy.py:7603).
        """
        self.active_call_id = call_id
        self.active_tool_name = tool_name
        outbox.put({
            "type": "tool_confirm",
            "call_id": call_id,
            "name": tool_name,
            "timeout_s": int(self.timeout_s),
        })
        resolved = self._thread_evt.wait(timeout=self.timeout_s)
        if not resolved:
            self._decision = "allow_once"
            outbox.put({
                "type": "tool_timeout",
                "call_id": call_id,
                "name": tool_name,
                "timeout_s": int(self.timeout_s),
            })
            logger.info(
                "approval gate: timeout tool=%s → default allow_once", tool_name,
            )
        decision = self._decision or "allow_once"
        self.active_call_id = ""
        self.active_tool_name = ""
        return decision

    def resolve(self, decision: str) -> None:
        """Resolve the pending approval. Called from WS reader + HTTP route."""
        if decision not in _VALID_DECISIONS:
            decision = "deny"
        self._decision = decision
        self._thread_evt.set()

    @property
    def is_pending(self) -> bool:
        return bool(self.active_call_id)


def _resolve_approval_mode() -> tuple[str, frozenset[str]]:
    """Read the current approval mode + safe-tool set from legacy state.

    Returns ``(mode, safe_tools)``. Falls back to
    ``("default", frozenset())`` if the legacy module isn't importable.
    """
    try:
        from cvc.gateway_legacy import _approval_mode as mode  # type: ignore
        from cvc.gateway_legacy import _SAFE_TOOLS as safe  # type: ignore
    except Exception:
        return ("default", frozenset())
    return (str(mode), frozenset(safe))


class _ChatOutbox:
    """Thread-safe ordered outbox of ChatEvent dicts for one turn.

    The upstream agent runs in a thread executor; the SSE/WS writer
    runs in the asyncio loop. ``put()`` is safe from both threads.
    """

    def __init__(self) -> None:
        self._queue: asyncio.Queue[dict | None] = asyncio.Queue()
        self._loop: asyncio.AbstractEventLoop | None = None
        # Streamed text accumulator — the agent populates the result
        # dict's ``response`` on completion, but the dashboard renders
        # BOTH the streaming text AND the completion event, so the
        # completion event's content must match what the user saw.
        self.streamed_text: list[str] = []
        # Cached turn_id (assigned on the first event for the turn)
        self.turn_id: str = ""
        # Monotonic seq counter (assigned per-event by the writer)
        self._seq: int = 0
        # Mirror of every event pushed via put(). The auto-skill
        # reflection hook replays this list AFTER the agent finishes
        # to extract a TurnSignal. Kept here (not computed inline)
        # so the reflection logic stays decoupled from event emission.
        # Tools that don't add signal (ping, keepalive, status text
        # deltas) are filtered out to keep the list short.
        self.tool_events: list[dict] = []

    def bind_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def put(self, event: dict | None) -> None:
        """Enqueue an event (or ``None`` sentinel) from any thread."""
        if self._loop is None:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                # Best-effort fallback: if we can't find a loop, drop
                # the event. This shouldn't happen because we always
                # call bind_loop() before the agent starts.
                if isinstance(event, dict):
                    logger.warning("Outbox: no running loop, dropping event %s", event.get("type"))
                return
        # Mirror events useful for post-turn reflection. Status/keepalive
        # are noise; tool_start/tool_result carry the signal.
        if isinstance(event, dict):
            et = event.get("type")
            if et in ("tool_start", "tool_result", "tool_progress", "error"):
                self.tool_events.append(dict(event))
        try:
            running = asyncio.get_running_loop()
        except RuntimeError:
            running = None
        if running is self._loop:
            self._queue.put_nowait(event)
        else:
            self._loop.call_soon_threadsafe(self._queue.put_nowait, event)

    async def get(self) -> dict | None:
        return await self._queue.get()

    def get_nowait(self) -> dict | None:
        """Non-blocking pop. Returns ``None`` on empty OR on end-of-run sentinel."""
        try:
            return self._queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    def empty(self) -> bool:
        return self._queue.empty()

    def qsize(self) -> int:
        return self._queue.qsize()


def _attach_outbox_callbacks(
    agent,
    outbox: _ChatOutbox,
    gate: _ApprovalGate,
) -> None:
    """Wire the upstream AIAgent's 4 callbacks to the outbox.

    Each callback translates the upstream event into a dashboard
    ChatEvent and pushes it into the outbox. The SSE/WS writer adds
    the monotonic ``seq`` and the turn's ``turn_id`` on the way out.

    v3.3.22 — Approval gate wired into ``_on_tool_start`` BEFORE the
    tool runs. The gate blocks the agent thread on a threading.Event
    proxy while the asyncio loop drives the wire protocol. The user
    resolves via WS ``{"type":"confirm","result":...}`` or HTTP
    ``POST /api/chat/confirm``. On deny, the gate returns the deny
    decision and the agent continues without executing the tool.
    """
    # Lazy import to avoid circular / heavy boot cost
    from cvc.agent._vendor.hermes.agent.display import (
        build_tool_preview,
        get_tool_emoji,
    )

    # Per-call start time lookup, keyed by call_id. Populated in
    # ``_on_tool_start``, consumed in ``_on_tool_complete``. The client
    # uses these to render accurate durations — without them a tool
    # that finishes inside the same WS frame round-trip shows as
    # ``0.00s`` because client-clock Date.now() returns the same
    # value for both events.
    _call_started_at: dict[str, int] = {}

    def _now_ms() -> int:
        # ``time.time()`` from the agent's worker thread; the unit is
        # seconds-since-epoch in float, but we want monotonic-ish
        # ms for the dashboard. Use ``monotonic()``-derived ms
        # instead so two events with the same wall-clock time still
        # get distinct deltas if they were a few µs apart.
        return int(time.monotonic() * 1000)

    def _on_delta(delta):
        # Match the upstream api_server's _on_delta: drop the None
        # sentinel that the agent fires between phases. Forwarding
        # None would prematurely close the SSE response and the
        # dashboard would miss the final answer after tool calls.
        if delta is None:
            return
        if not delta:
            return
        # v3.3.26 — Instrumentation. One log line per text delta.
        # Counts and samples are how we tell the difference between
        # "the gateway is delivering chunks and the renderer is
        # skipping them" vs "the agent never produced chunks in the
        # first place". Without this we'd be guessing.
        try:
            _DELTA_COUNT[0] += 1
            _DELTA_TOTAL_CHARS[0] += len(delta)
            if _DELTA_COUNT[0] <= 3 or _DELTA_COUNT[0] % 10 == 0:
                logger.info(
                    "cvc.chat._on_delta #%d chars=%d sample=%r cumulative_chars=%d",
                    _DELTA_COUNT[0],
                    len(delta),
                    delta[:60],
                    _DELTA_TOTAL_CHARS[0],
                )
        except Exception:
            pass
        outbox.streamed_text.append(delta)
        outbox.put({"type": "text", "content": delta})

    def _on_tool_start(call_id, name, args):
        # Mirror the upstream api_server's _on_tool_start: skip
        # internal tools (those starting with ``_``) and tools with
        # no call_id.
        if not call_id or (isinstance(name, str) and name.startswith("_")):
            return
        # v3.3.26 — Instrumentation
        try:
            _TOOL_COUNT[0] += 1
            logger.info(
                "cvc.chat._on_tool_start #%d name=%s call_id=%s args_keys=%s",
                _TOOL_COUNT[0],
                name,
                call_id[:8],
                list((args or {}).keys()),
            )
        except Exception:
            pass
        try:
            label = build_tool_preview(name, args or {}) or name
        except Exception:
            label = name
        try:
            emoji = get_tool_emoji(name)
        except Exception:
            emoji = "⚡"
        _call_started_at[call_id] = _now_ms()
        # v3.3.22 — Approval gate consult. Runs BEFORE the tool_start
        # event lands on the dashboard so the user sees the approval
        # card first, then the tool_start card once they allow. Mode
        # "default" + non-safe tool → block; otherwise → proceed.
        try:
            mode, safe_tools = _resolve_approval_mode()
        except Exception:
            mode, safe_tools = "default", frozenset()
        if mode == "default" and name not in safe_tools:
            decision = gate.wait(call_id=call_id, tool_name=name, outbox=outbox)
            if decision in ("deny", "deny_suggest"):
                # The agent thread has been blocked on the gate; now it
                # returns with deny. The upstream agent's tool_executor
                # handles the synthetic deny result internally via the
                # _set_tool_guardrail_halt path (already wired in the
                # v3.3.21 tool-loop guardrail hotfix). We surface a
                # marker event so the dashboard can render an inline
                # deny banner instead of a generic tool_result.
                outbox.put({
                    "type": "tool_denied",
                    "call_id": call_id,
                    "name": name,
                    "reason": decision,
                })
                logger.info("approval gate: denied tool=%s reason=%s", name, decision)
                # Note: we still emit the tool_start event below so the
                # activity strip shows the call. The deny is rendered
                # alongside. If you want to hide the card entirely, set
                # ``return`` here instead — but losing the visual breadcrumb
                # makes debugging harder, so we keep it.
        outbox.put({
            "type": "tool_start",
            "call_id": call_id,
            "name": name,
            "args": args or {},
            "label": label,
            "emoji": emoji,
            "started_at_ms": _call_started_at[call_id],
        })

    def _on_tool_complete(call_id, name, args, result):
        if not call_id:
            return
        # Result may be a string, dict, list, or other JSON shape.
        # Normalize to a string for the dashboard's tool_result pane
        # (it renders text by default; structured results pass through).
        if isinstance(result, (dict, list)):
            try:
                content = json.dumps(result, ensure_ascii=False)
            except Exception:
                content = str(result)
        else:
            content = str(result) if result is not None else ""
        ended_at_ms = _now_ms()
        started_at_ms = _call_started_at.pop(call_id, ended_at_ms)
        duration_ms = max(0, ended_at_ms - started_at_ms)
        outbox.put({
            "type": "tool_result",
            "call_id": call_id,
            "name": name,
            "output": content,
            "started_at_ms": started_at_ms,
            "ended_at_ms": ended_at_ms,
            "duration_ms": duration_ms,
        })

    def _on_tool_progress(event_type, tool_name=None, preview=None, **kwargs):
        # Fire-hose emit. Used as a safety net if the structured
        # tool_start / tool_complete callbacks somehow didn't fire
        # (e.g. internal tools, or a model provider that doesn't
        # carry tool_call_id). Most events will be deduped at the
        # dashboard level because they share the same tool_name.
        payload = {"type": event_type or "tool_progress"}
        if tool_name:
            payload["tool"] = tool_name
        if preview:
            payload["preview"] = preview
        for k, v in kwargs.items():
            if k in ("args", "result", "error", "call_id") and v is not None:
                payload[k] = v
        outbox.put(payload)

    # Attach to the agent. AIAgent stores these as plain attributes
    # so we can swap them per-request — this is exactly how the
    # upstream api_server does it (per-turn callback injection).
    agent.stream_delta_callback = _on_delta
    agent.tool_start_callback = _on_tool_start
    agent.tool_complete_callback = _on_tool_complete
    agent.tool_progress_callback = _on_tool_progress


# -----------------------------------------------------------------------------
# Agent builder (sync, runs in thread executor)
# -----------------------------------------------------------------------------

def _build_agent_sync(
    *,
    session_id: str,
    workspace_path: Optional[str],
    outbox: _ChatOutbox,
    gate: _ApprovalGate,
    ephemeral_system_prompt: Optional[str] = None,
    portal_session_id: Optional[str] = None,
):
    """Build the AIAgent and attach outbox callbacks. Runs in a thread.

    CRITICAL (v3.3.12 hotfix): the outbox callbacks MUST be passed into
    ``create_agent(...)`` as constructor arguments, not assigned after the
    fact via ``agent.<cb> = ...``.

    Why: ``cvc.gateway.agent.create_agent`` caches the AIAgent per
    (model, provider, base_url, api_key, toolsets, workspace). On a cache
    HIT it executes::

        cached.stream_delta_callback   = stream_delta_callback   # caller arg
        cached.tool_progress_callback  = tool_progress_callback  # caller arg
        cached.tool_start_callback     = tool_start_callback     # caller arg
        cached.tool_complete_callback  = tool_complete_callback  # caller arg

    — and ``create_agent`` was being called with ``stream_delta_callback=None``
    and friends because the chat layer used to do the post-assign pattern.
    Assigning ``None`` to a cached agent that may belong to ANOTHER in-flight
    request kills BOTH requests' streaming AND tool event visibility — the
    exact "flash out completely, no tool dropdown" symptom.

    Constructing callbacks here (in the same thread, before
    ``create_agent``) and forwarding them through the constructor is the
    only path that survives the cache. We also call
    ``_attach_outbox_callbacks`` after the fact as a belt-and-braces
    re-bind for any code path that bypasses the constructor args (and to
    keep the started_at_ms / duration_ms accounting in one place).
    """
    from cvc.gateway.agent import create_agent

    def _noop_delta(_delta):
        return None

    def _noop_tool_start(*_a, **_kw):
        return None

    def _noop_tool_complete(*_a, **_kw):
        return None

    def _noop_tool_progress(*_a, **_kw):
        return None

    # CRITICAL (v3.3.12): pass non-None no-ops into create_agent so the
    # cache-hit path in cvc.gateway.agent does not overwrite the
    # previously-attached callbacks with None. _attach_outbox_callbacks
    # below replaces these with the real outbox-pushing closures (which
    # carry the started_at_ms / duration_ms accounting).
    #
    # v3.5.0 — TIME PORTAL: if portal_session_id is set, build a historical
    # soul context block and prepend it to the ephemeral system prompt.
    # This is the cleanest hook: ephemeral_system_prompt already flows
    # through build_system_prompt(... extra=...) and is rebuilt per turn
    # (the cache key is workspace+model, not prompt content), so each
    # portal-mode turn gets the right historical frame without rebuilding
    # the agent. The portal block is bounded to ~6KB to keep turns cheap.
    portal_context = ""
    if portal_session_id:
        logger.info(
            "v3.5.0 portal lookup: portal_id=%s (received from chat layer)",
            portal_session_id[:12],
        )
        try:
            from cvc.gateway.soul import (
                _load_portal_sessions,
                format_portal_chat_context,
                format_portal_day_context,
            )
            sessions = _load_portal_sessions()
            sess = sessions.get(portal_session_id)
            if sess:
                sess_scope = sess.get("scope", "snapshot")
                if sess_scope == "day":
                    portal_context = format_portal_day_context(
                        sess.get("date", sess.get("iso_date", "")),
                        max_chars=8000,
                    )
                else:
                    portal_context = format_portal_chat_context(
                        sess.get("snapshot_id", ""),
                        max_chars=6000,
                    )
                logger.info(
                    "v3.5.0 portal context built: snapshot=%s iso_date=%s chars=%d",
                    sess.get("snapshot_id", "")[:12],
                    time.strftime(
                        "%Y-%m-%d %H:%M",
                        time.localtime(float(sess.get("snapshot_timestamp", 0))),
                    )
                    if sess.get("snapshot_timestamp")
                    else "?",
                    len(portal_context),
                )
            else:
                logger.warning(
                    "v3.5.0 portal_session_id=%s provided but no active session — "
                    "falling back to current soul. Known sessions: %s",
                    portal_session_id[:12],
                    list(sessions.keys())[:3],
                )
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "v3.5.0 portal context lookup FAILED (non-fatal): %s", exc,
                exc_info=True,
            )

    merged_ephemeral = portal_context
    if ephemeral_system_prompt:
        merged_ephemeral = (
            (portal_context + "\n\n" if portal_context else "")
            + ephemeral_system_prompt
        )

    # When portal mode is active, ALSO inject the portal framing as a
    # user/assistant prefill pair. System-prompt tail instructions are
    # easy for models to ignore (especially when the cached stable
    # identity layer contradicts them — e.g. "be Sofia" vs "be the
    # soul as of X"). A prefill pair is treated as established context
    # the model continues from, which is the most reliable way to lock
    # the temporal frame.
    portal_prefill: list[dict[str, str]] = []
    if portal_session_id and portal_context:
        try:
            from cvc.gateway.soul import _load_portal_sessions
            _sess = _load_portal_sessions().get(portal_session_id) or {}
            iso_date = _sess.get("iso_date") or "the selected date"
        except Exception:
            iso_date = "the selected date"
        portal_prefill = [
            {
                "role": "user",
                "content": (
                    "[System context — Time Portal is ACTIVE]\n\n"
                    f"{portal_context}\n\n"
                    "Acknowledge the portal frame in one short sentence, "
                    "then wait for the user's message."
                ),
            },
            {
                "role": "assistant",
                "content": (
                    "Time Portal active — I'm answering as the soul knew on "
                    f"{iso_date}. What would you like to talk about?"
                ),
            },
        ]
        logger.info(
            "v3.5.0 portal prefill: %d messages queued (iso_date=%s)",
            len(portal_prefill), iso_date,
        )

    agent = create_agent(
        session_id=session_id,
        workspace_path=workspace_path,
        ephemeral_system_prompt=merged_ephemeral,
        stream_delta_callback=_noop_delta,
        tool_progress_callback=_noop_tool_progress,
        tool_start_callback=_noop_tool_start,
        tool_complete_callback=_noop_tool_complete,
        prefill_messages=portal_prefill or None,
    )
    _attach_outbox_callbacks(agent, outbox, gate)
    return agent


# -----------------------------------------------------------------------------
# One-shot run_chat_turn — non-streaming entry point for channel adapters
# -----------------------------------------------------------------------------
#
# Channels (Telegram, Discord, Slack, webhook, …) need to take a single
# inbound message, run the SAME agent the dashboard uses, and return the
# final reply as a plain string. They do NOT want SSE, WebSocket framing,
# approval gates, or an outbox. This is that path.
#
# Reuses cvc.gateway.agent.create_agent — so it benefits from the LRU
# cache (one AIAgent per worker, ~1.8s amortised build cost) and uses
# the same provider/model/api_key/toolsets the user already configured.
# No re-implementation of the chat loop, no duplicate provider wiring,
# no risk of drift between the dashboard and the channels.
#
# Concurrency: the AIAgent is *not* asyncio-native — run_conversation
# blocks. We dispatch it through ``loop.run_in_executor`` so the channel
# adapter's async handler doesn't stall other adapters while one bot
# user is being answered. Multiple inbound messages run on the executor
# pool; the agent cache itself is process-global and lock-protected.
#
# Channel sessions are stable per (channel, chat_id) so a user DMing the
# Telegram bot five times in a row sees a single coherent conversation.
# Threads share their parent chat_id's session.


async def run_chat_turn(
    *,
    workspace_path: Optional[str],
    channel: str,
    chat_id: str,
    user_id: str,
    user_name: Optional[str],
    thread_id: Optional[str],
    text: str,
    portal_session_id: Optional[str] = None,
) -> str:
    """Run one user message through the CVC AIAgent and return the final
    reply as a plain string. Designed for channel adapters (Telegram,
    Discord, Slack, webhook, …) that need a non-streaming one-shot.

    Args:
        workspace_path: CVC workspace root (passed to ``create_agent``).
            When ``None``, falls back to the user's last-active workspace
            so we still hit the same persistent agent cache.
        channel: channel name (e.g. ``"telegram"``). Used in the session
            id so two channels never share conversation history.
        chat_id: the platform-specific conversation id (Telegram chat_id,
            Discord channel id, Slack thread_ts, etc).
        user_id: the platform-specific user id. Currently used for
            logging + session id derivation; future: per-user RBAC.
        user_name: human-readable display name. Used for log lines only.
        thread_id: optional sub-conversation id (Telegram topics, Slack
            thread_ts). When present we route to a thread-scoped session
            that inherits the parent chat's history.
        text: the user's message text.

    Returns:
        The agent's final assistant response as a plain string. Never
        raises — agent failures are caught and returned as a friendly
        ⚠️ message so the channel never silently swallows an error.
    """
    from cvc.gateway.agent import create_agent

    if not text or not text.strip():
        return ""

    # Build a stable session id per (channel, chat_id[, thread_id]).
    # This is what lets a multi-turn DM work: every inbound message
    # from the same Telegram chat hits the same AIAgent.session_id,
    # and the conversation loop loads the prior history.
    sid_parts = [f"cvc_ch_{channel}", str(chat_id)]
    if thread_id:
        sid_parts.append(str(thread_id))
    session_id = "_".join(sid_parts)

    # Workspace fallback — channel users almost never set one explicitly.
    # We re-use the same default the dashboard uses so the cache key
    # matches and we get the cached AIAgent back instead of building
    # a fresh one for every inbound.
    ws = workspace_path
    if not ws:
        # Channels (Telegram, Discord, …) get FULL machine access — not
        # locked to one project workspace like the dashboard. The agent's
        # tools (terminal, file, etc.) can reach anywhere on the machine.
        from pathlib import Path
        ws = str(Path.home())

    loop = asyncio.get_running_loop()
    log = logger.getChild("run_chat_turn")

    def _run() -> str:
        """Build + run the agent. Synchronous — runs in the executor."""
        # v3.5.0 — TIME PORTAL: load historical-soul context if a portal
        # session is active. Channel adapters don't currently expose a
        # portal picker UI (no Telegram "enter the portal" command yet)
        # but if a portal_session_id IS provided, we honor it.
        portal_ephemeral = ""
        portal_prefill: list[dict[str, str]] = []
        if portal_session_id:
            try:
                from cvc.gateway.soul import (
                    _load_portal_sessions,
                    format_portal_chat_context,
                    format_portal_day_context,
                )
                sessions = _load_portal_sessions()
                sess = sessions.get(portal_session_id)
                if sess:
                    sess_scope = sess.get("scope", "snapshot")
                    if sess_scope == "day":
                        portal_ephemeral = format_portal_day_context(
                            sess.get("date", sess.get("iso_date", "")),
                            max_chars=8000,
                        )
                    else:
                        portal_ephemeral = format_portal_chat_context(
                            sess.get("snapshot_id", ""), max_chars=6000,
                        )
                    # Same prefill pattern as _build_agent_sync — see
                    # comment there for rationale.
                    iso_date = sess.get("iso_date") or "the selected date"
                    portal_prefill = [
                        {
                            "role": "user",
                            "content": (
                                "[System context — Time Portal is ACTIVE]\n\n"
                                f"{portal_ephemeral}\n\n"
                                "Acknowledge the portal frame in one short "
                                "sentence, then wait for the user's message."
                            ),
                        },
                        {
                            "role": "assistant",
                            "content": (
                                f"Time Portal active — I'm answering as the "
                                f"soul knew on {iso_date}. What would you "
                                f"like to talk about?"
                            ),
                        },
                    ]
            except Exception as exc:  # noqa: BLE001
                logger.debug("portal context lookup failed (non-fatal): %s", exc)

        agent = create_agent(
            session_id=session_id,
            workspace_path=ws,
            ephemeral_system_prompt=portal_ephemeral or None,
            # Noop callbacks: the channel adapter doesn't want SSE
            # events. We pass non-None noops (never None) because the
            # cache-hit path in create_agent re-binds whatever we pass
            # — if we passed None, we could wipe the dashboard's
            # already-attached callbacks. See v3.3.12 hotfix in
            # _build_agent_sync above for the full reasoning.
            stream_delta_callback=lambda *_: None,
            tool_progress_callback=lambda *_, **__: None,
            tool_start_callback=lambda *_, **__: None,
            tool_complete_callback=lambda *_, **__: None,
            prefill_messages=portal_prefill or None,
        )
        result = agent.run_conversation(
            user_message=text,
            conversation_history=None,
            task_id=session_id,
        )
        return str(result.get("final_response", "") or "")

    try:
        reply = await loop.run_in_executor(None, _run)
    except Exception as exc:  # noqa: BLE001
        log.exception("run_chat_turn: agent crashed (channel=%s chat=%s)", channel, chat_id)
        return (
            "⚠️ CVC chat turn failed. The error has been logged — "
            "check the gateway logs for details. "
            f"({type(exc).__name__})"
        )

    log.info(
        "run_chat_turn: ok channel=%s chat=%s user=%s reply_len=%d",
        channel, chat_id, user_id, len(reply),
    )
    return reply


# -----------------------------------------------------------------------------
# Streaming run_chat_turn_streaming — async generator for channel adapters
# -----------------------------------------------------------------------------
#
# Channels with streaming-edit capability (Telegram, Discord, …) want live
# word-by-word updates — the same experience the dashboard gets via SSE.
# This generator reuses the SAME _ChatOutbox + _build_agent_sync pipeline
# as the dashboard's SSE endpoint, but instead of writing SSE frames it
# yields plain dicts that the adapter consumes:
#
#   {"type": "text",       "content": "delta"}     — streaming text
#   {"type": "tool_start",  "name": "...", ...}     — tool invocation
#   {"type": "tool_result", "name": "...", ...}     — tool result
#   {"type": "status",      "content": "..."}        — status / info
#   {"type": "done",        "content": "full text"}  — turn finished
#   {"type": "error",       "message": "..."}        — failure
#
# The adapter is free to ignore tool/status events and only listen for
# "text" + "done" (simplest case) or surface them as status messages.
#
# Workspace: defaults to the user's home directory so the Telegram bot
# has FULL machine access (not locked to one project workspace like the
# dashboard). Callers can override via workspace_path.


async def run_chat_turn_streaming(
    *,
    workspace_path: Optional[str] = None,
    channel: str = "telegram",
    chat_id: str = "",
    user_id: str = "",
    user_name: Optional[str] = None,
    thread_id: Optional[str] = None,
    text: str = "",
    bypass_approval: bool = True,
    portal_session_id: Optional[str] = None,
) -> AsyncIterator[dict[str, Any]]:
    """Streaming version of :func:`run_chat_turn`.

    Yields events (see module docstring above) as an async generator.
    The agent runs in a thread executor; events are marshalled through
    a thread-safe :class:`_ChatOutbox` queue — the same mechanism the
    dashboard SSE endpoint uses.

    When ``bypass_approval`` is True (default), all tool calls are
    auto-approved — the Telegram bot is a fully-autonomous agent with
    no human-in-the-loop gate. This matches Jai's requirement that the
    bot "just responds to whatever the user asks" without friction.
    """
    from pathlib import Path

    if not text or not text.strip():
        yield {"type": "done", "content": ""}
        return

    # Session ID — stable per (channel, chat_id[, thread_id]).
    sid_parts = [f"cvc_ch_{channel}", str(chat_id)]
    if thread_id:
        sid_parts.append(str(thread_id))
    session_id = "_".join(sid_parts)

    # Workspace — default to HOME for full machine access.
    ws = workspace_path or str(Path.home())

    loop = asyncio.get_running_loop()
    log_s = logger.getChild("run_chat_turn_streaming")

    # C3: spine capture for channel adapters (Telegram/Slack/etc.).
    try:
        from cvc.events.chat_capture import ChatCapture
        chat_cap = ChatCapture(
            workspace=workspace_path,
            channel=channel,
            actor=str(user_id) if user_id is not None else None,
            session_id=chat_id,
            turn_id=None,
        )
        chat_cap.session_start(user_message=text)
    except Exception as exc:  # noqa: BLE001
        log_s.debug("ChatCapture init failed: %s", exc)
        chat_cap = None

    outbox = _ChatOutbox()
    outbox.turn_id = session_id
    outbox.bind_loop(loop)

    # Approval gate — bypass mode for channels (fully autonomous).
    gate = _ApprovalGate(loop=loop, timeout_s=300.0)
    if bypass_approval:
        # Force bypass: pre-resolve any gate check to "allow_always".
        _orig_wait = gate.wait

        def _auto_allow(*, call_id, tool_name, outbox):
            return "allow_always"

        gate.wait = _auto_allow  # type: ignore[method-assign]

    # Build agent in thread (heavy imports).
    try:
        agent = await loop.run_in_executor(
            None,
            lambda: _build_agent_sync(
                session_id=session_id,
                workspace_path=ws,
                outbox=outbox,
                gate=gate,
            ),
        )
    except Exception as exc:
        log_s.exception("streaming: agent build failed")
        yield {"type": "error", "message": f"Agent init failed: {exc}"}
        yield {"type": "done", "content": ""}
        return

    # Run agent in executor thread.
    run_holder: dict[str, Any] = {}

    def _run_agent() -> None:
        try:
            result = agent.run_conversation(
                user_message=text,
                conversation_history=None,
                task_id=session_id,
            )
            run_holder["result"] = result
        except Exception as exc:
            run_holder["error"] = exc
        finally:
            # Sentinel — signals the consumer loop that no more events
            # will arrive from the agent callbacks.
            outbox.put(None)

    # Dispatch the agent run (don't await — we consume the outbox concurrently).
    agent_future = loop.run_in_executor(None, _run_agent)

    # Consume outbox events → yield to caller.
    while True:
        try:
            event = await asyncio.wait_for(outbox.get(), timeout=180.0)
        except asyncio.TimeoutError:
            log_s.warning("streaming: outbox timeout (180s no event)")
            yield {"type": "error", "message": "Response timed out."}
            break

        if event is None:
            # Sentinel — agent finished.
            break

        yield event

    # Ensure the executor task is done (should be, since sentinel was sent).
    try:
        await asyncio.wait_for(asyncio.shield(agent_future), timeout=5.0)
    except Exception:
        pass

    # Check for agent errors.
    if "error" in run_holder:
        exc = run_holder["error"]
        log_s.exception("streaming: agent crashed", exc_info=exc)
        yield {"type": "error", "message": f"Agent error: {exc}"}

    # Final done event with accumulated text.
    final_text = "".join(outbox.streamed_text)
    yield {"type": "done", "content": final_text}

    # C3: spine capture finalization for channel adapters.
    if chat_cap is not None:
        try:
            chat_cap.assistant_message(text=final_text)
            chat_cap.session_end(
                status="err" if "error" in run_holder else "ok",
            )
        except Exception as exc:  # noqa: BLE001
            log_s.debug("ChatCapture final capture failed: %s", exc)

    log_s.info(
        "streaming: ok channel=%s chat=%s reply_len=%d deltas=%d tools=%d",
        channel, chat_id, len(final_text),
        _DELTA_COUNT[0], _TOOL_COUNT[0],
    )


# -----------------------------------------------------------------------------
# POST /api/chat — streaming SSE
# -----------------------------------------------------------------------------

@router.post("/chat")
async def chat_endpoint(
    request: Request,
    x_cvc_workspace: Optional[str] = Header(default=None),
):
    """OpenAI-style chat completion endpoint, streaming SSE events.

    SSE event types (dashboard ChatEvent vocabulary — cvc/web/src/lib/types.ts):
        turn_start      - chat turn has begun            (control)
        status          - status / progress / info       (text msg)
        text            - streaming assistant delta      (content)
        tool_start      - tool invocation                (name, args, label, emoji)
        tool_result     - tool finished                  (call_id, name, output)
        error           - something went wrong           (message)
        done            - turn finished                  (control, full content)
    """
    body = await request.json()
    messages = body.get("messages") or []
    if not messages:
        raise HTTPException(status_code=400, detail="No messages in body")

    workspace_path = await _resolve_workspace(body, x_cvc_workspace)
    user_message = _extract_user_message(messages)
    if not user_message:
        raise HTTPException(status_code=400, detail="No user message found")

    conversation_history = _extract_conversation_history(messages[:-1])
    session_id = body.get("session_id") or f"cvc_{uuid.uuid4().hex[:12]}"
    turn_id = _build_run_id(session_id)
    # v3.5.0 — TIME PORTAL: when set, the chat turn is augmented with a
    # historical-soul context block (see _build_agent_sync). We also use
    # this to skip per-turn soul updates below so talking to past-Jai
    # doesn't write new facts into the present soul. Stays None for
    # normal traffic.
    portal_session_id = body.get("portal_session_id") if isinstance(body, dict) else None
    if portal_session_id and not isinstance(portal_session_id, str):
        portal_session_id = None

    async def event_stream() -> AsyncIterator[bytes]:
        loop = asyncio.get_running_loop()
        outbox = _ChatOutbox()
        outbox.turn_id = turn_id
        outbox.bind_loop(loop)
        # v3.3.22 — Per-turn approval gate. Consulted inline before each
        # non-safe tool runs. The gate's ``wait()`` blocks the agent
        # thread while the asyncio loop drives the wire protocol.
        gate = _ApprovalGate(loop=loop, timeout_s=120.0)
        _register_gate(turn_id, gate)
        # v3.3.26 — Instrumentation
        _TURN_COUNT[0] += 1
        logger.info("cvc.chat.chat_endpoint turn #%d turn_id=%s session_id=%s workspace=%s",
                    _TURN_COUNT[0], turn_id[:12], session_id, workspace_path or "<none>")

        # ── C3: event spine capture ─────────────────────────────────
        # Best-effort, never raises. Records the user message + every
        # tool call/result + the assistant's final reply.
        try:
            from cvc.events.chat_capture import ChatCapture
            chat_cap = ChatCapture(
                workspace=workspace_path,
                channel="web",
                actor="Jai",
                session_id=session_id,
                turn_id=turn_id,
            )
            chat_cap.session_start(user_message=user_message)
        except Exception as exc:  # noqa: BLE001
            logger.debug("ChatCapture init failed (non-fatal): %s", exc)
            chat_cap = None

        # Emit turn_start immediately so the dashboard can adopt the
        # turn_id for dedup / resume logic.
        yield _sse({
            "type": "turn_start",
            "turn_id": turn_id,
            "seq": 0,
        })

        # Build the agent in a thread (it imports a lot)
        try:
            agent = await loop.run_in_executor(
                None,
                lambda: _build_agent_sync(
                    session_id=session_id,
                    workspace_path=workspace_path,
                    outbox=outbox,
                    gate=gate,
                    portal_session_id=portal_session_id,
                ),
            )
        except Exception as e:
            logger.exception("Failed to build AIAgent")
            yield _sse({
                "type": "error",
                "message": f"agent init failed: {e}",
                "seq": outbox.next_seq(),
            })
            yield _sse({
                "type": "done",
                "turn_id": turn_id,
                "content": "",
                "seq": outbox.next_seq(),
            })
            return

        agent_ref: list = [None]
        run_done = asyncio.Event()
        run_result_holder: dict = {}

        def _run() -> None:
            agent_ref[0] = agent
            try:
                result = agent.run_conversation(
                    user_message=user_message,
                    conversation_history=conversation_history,
                    task_id=session_id,
                )
                run_result_holder["result"] = result
            except Exception as e:
                run_result_holder["error"] = e
            finally:
                # Wake the SSE loop exactly once when the run ends.
                try:
                    loop.call_soon_threadsafe(run_done.set)
                except RuntimeError:
                    pass
                # Sentinel into the outbox so the writer's blocking
                # ``get()`` returns immediately even if the agent
                # died before emitting the final event.
                try:
                    outbox.put(None)
                except Exception:
                    pass

        loop.run_in_executor(None, _run)

        # Stream events from the outbox until the agent finishes.
        last_activity = time.monotonic()
        try:
            while True:
                # Block for the next event, but wake periodically to
                # emit a keepalive if the run is genuinely idle
                # (e.g. a long-running tool that emits no events).
                evt: dict | None = None
                try:
                    evt = await asyncio.wait_for(
                        outbox.get(),
                        timeout=_KEEPALIVE_SECONDS,
                    )
                except asyncio.TimeoutError:
                    # No event for KEEPALIVE_SECONDS — emit SSE
                    # keepalive and continue waiting. The dashboard's
                    # lastEventAt watchdog resets on every SSE
                    # comment line, so this prevents the misleading
                    # "no stream events for 105s" banner.
                    yield _sse_keepalive()
                    last_activity = time.monotonic()
                    continue

                last_activity = time.monotonic()
                if evt is None:
                    # End-of-run sentinel from _run().
                    break

                # Add monotonic seq + turn_id on the way out.
                evt.setdefault("seq", outbox.next_seq())
                evt.setdefault("turn_id", turn_id)

                # C3: spine capture per SSE event (best-effort).
                if chat_cap is not None:
                    try:
                        etype = evt.get("type")
                        if etype == "tool_start":
                            chat_cap.tool_call(
                                name=evt.get("name", "?"),
                                call_id=evt.get("call_id", ""),
                                args=evt.get("args"),
                            )
                        elif etype == "tool_result":
                            err = evt.get("error")
                            chat_cap.tool_result(
                                name=evt.get("name", "?"),
                                call_id=evt.get("call_id", ""),
                                output=evt.get("output"),
                                status="err" if err else "ok",
                                error=err,
                            )
                        elif etype == "error":
                            chat_cap.error(message=evt.get("message", ""))
                    except Exception as exc:  # noqa: BLE001
                        logger.debug("ChatCapture per-event failed: %s", exc)

                yield _sse(evt)

                # If the agent finished, exit after draining.
                if run_done.is_set():
                    # Drain any remaining events.
                    while not outbox.empty():
                        extra = outbox.get_nowait()
                        if extra is None:
                            continue
                        extra.setdefault("seq", outbox.next_seq())
                        extra.setdefault("turn_id", turn_id)
                        yield _sse(extra)
                    break

        except asyncio.CancelledError:
            try:
                if agent_ref[0] is not None:
                    agent_ref[0].interrupt()
            except Exception:
                pass
            raise

        # Terminal event: ``done`` with the final assistant text.
        # Prefer result.response (the agent's authoritative final
        # message); fall back to the streamed-text accumulator.
        final_text = ""
        if "result" in run_result_holder:
            result = run_result_holder["result"] or {}
            final_text = (
                result.get("response")
                or result.get("final_response")
                or "".join(outbox.streamed_text)
            )
            if result.get("failed"):
                yield _sse({
                    "type": "error",
                    "message": result.get("error") or "Agent run failed",
                    "seq": outbox.next_seq(),
                    "turn_id": turn_id,
                })
            # v3.3.21 — If the agent stopped itself because the tool-loop
            # guardrail halted a runaway sequence, surface that to the
            # dashboard BEFORE the done event. The user sees a clear
            # explanation ("X read_file calls with identical args were
            # blocked") instead of an unexplained silence. Mirror the
            # same shape as the WebSocket path further down.
            guardrail = result.get("guardrail")
            if guardrail:
                yield _sse({
                    "type": "guardrail_halt",
                    "turn_id": turn_id,
                    "tool_name": guardrail.get("tool_name", ""),
                    "code": guardrail.get("code", ""),
                    "message": guardrail.get("message", ""),
                    "count": guardrail.get("count", 0),
                    "seq": outbox.next_seq(),
                })
        elif "error" in run_result_holder:
            yield _sse({
                "type": "error",
                "message": str(run_result_holder["error"]),
                "seq": outbox.next_seq(),
                "turn_id": turn_id,
            })

        yield _sse({
            "type": "done",
            "turn_id": turn_id,
            "content": final_text,
            "seq": outbox.next_seq(),
        })

        # C3: capture the assistant's final message + session_end.
        if chat_cap is not None:
            try:
                tokens_in = 0
                tokens_out = 0
                # Try to grab token counts from the result if available
                result_for_tokens = run_result_holder.get("result") or {}
                if isinstance(result_for_tokens, dict):
                    tokens_in = int(result_for_tokens.get("tokens_in") or 0)
                    tokens_out = int(result_for_tokens.get("tokens_out") or 0)
                chat_cap.assistant_message(
                    text=final_text,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                )
                chat_cap.session_end(
                    status="err" if run_result_holder.get("error") or run_result_holder.get("result", {}).get("failed") else "ok",
                )
            except Exception as exc:  # noqa: BLE001
                logger.debug("ChatCapture final capture failed: %s", exc)

        # v3.3.22 — Unregister the gate so HTTP /api/chat/confirm doesn't
        # resolve a gate that already finished. Idempotent.
        _unregister_gate(turn_id)

        # ── Auto-skill reflection hook ─────────────────────────────
        # Runs AFTER the terminal `done` event so the user always
        # sees the answer first, then gets a `skill_drafted` event
        # if a reusable pattern was detected. Failures here must
        # never break the response — wrap defensively.
        try:
            from cvc.agent.auto_skill import maybe_create_draft
            draft_result = maybe_create_draft(
                session_id=session_id,
                turn_id=turn_id,
                user_message=user_message,
                outbox_events=outbox.tool_events,
                final_response=final_text,
                workspace_path=workspace_path,
            )
            if draft_result and draft_result.get("drafted"):
                logger.info(
                    "auto-skill: drafted %s (confidence=%.2f) from turn %s",
                    draft_result.get("name"),
                    draft_result.get("confidence", 0.0),
                    turn_id,
                )
                yield _sse({
                    "type": "skill_drafted",
                    "turn_id": turn_id,
                    "name": draft_result.get("name"),
                    "path": draft_result.get("path"),
                    "confidence": draft_result.get("confidence", 0.0),
                    "seq": outbox.next_seq(),
                })
        except Exception as e:  # pragma: no cover — best-effort
            logger.debug("auto-skill reflection failed: %s", e)

        # ── Per-turn soul auto-encoder (H2 wiring) ──────────────────
        # hotfix/soul-wiring-2026-06-30 — the dashboard chat path used
        # to drop on the floor every chat turn's contribution to the
        # soul. The hook was only wired into the legacy SSE-proxy path
        # (cvc/gateway_chat.py), which most dashboard chats bypass in
        # favour of /api/chat + /api/ws/chat in this file. Fire the
        # same heuristic pass after the response is fully streamed so
        # every turn incrementally teaches the active workspace's
        # <workspace>/.cvc/user_model.json — which is what the Soul
        # page reads from. Best-effort, never breaks the response.
        #
        # v3.5.0 → v3.5.1 — TIME PORTAL: changed from "skip in portal mode" to
        # "always write, but label portal-mode turns with [portal:{date}]".
        # Jai's framing: the soul should never lose information — even a
        # time-travel conversation belongs in the present soul's audit
        # trail. The label lets future filtering separate portal-mode
        # dialogue from regular chat without losing either.
        try:
            from cvc.operations.per_turn_soul import fire_and_forget_update
            user_msg_for_soul = user_message
            assistant_text_for_soul = final_text
            if portal_session_id:
                try:
                    from cvc.gateway.soul import _load_portal_sessions
                    _psess = _load_portal_sessions().get(portal_session_id) or {}
                    _pdate = (
                        _psess.get("date")
                        or _psess.get("iso_date")
                        or "unknown"
                    )
                    _pscope = _psess.get("scope", "snapshot")
                    _plabel = f"[portal:{_pdate}][{_pscope}] "
                    user_msg_for_soul = _plabel + (user_message or "")
                    assistant_text_for_soul = _plabel + (final_text or "")
                    logger.info(
                        "v3.5.1 portal-labeled soul write: portal_id=%s date=%s scope=%s",
                        portal_session_id[:12], _pdate, _pscope,
                    )
                except Exception as _lab_exc:  # noqa: BLE001
                    logger.debug("portal label lookup failed (non-fatal): %s", _lab_exc)
            fire_and_forget_update(
                user_message=user_msg_for_soul,
                assistant_text=assistant_text_for_soul,
                workspace_path=workspace_path,
            )
        except Exception as e:  # pragma: no cover — best-effort
            logger.debug("per-turn soul hook failed: %s", e)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
            "X-CVC-Turn-Id": session_id,
        },
    )


# Note: gate is unregistered inside event_stream() via a finally-equivalent
# (see the unregister call before the StreamingResponse returns above).


# -----------------------------------------------------------------------------
# WS /api/ws/chat — same flow, WebSocket transport
# -----------------------------------------------------------------------------

@router.websocket("/ws/chat")
async def ws_chat_endpoint(
    websocket: WebSocket,
    x_cvc_workspace: Optional[str] = Header(default=None),
):
    """WebSocket chat endpoint. Same event flow as POST /api/chat, JSON over WS.

    Adds:
      - monotonic ``seq`` per frame
      - ``turn_id`` on the first frame of each turn (so the
        dashboard's ChatWS can dedup / resume)
      - ``ping`` keepalive every KEEPALIVE_SECONDS so the dashboard's
        lastEventAt watchdog never fires during long tool calls
      - bounded ``send_json`` (asyncio.wait_for 5s) so a wedged
        socket can't stall the agent forever
    """
    await websocket.accept()
    try:
        init = await websocket.receive_json()
    except Exception:
        await websocket.close(code=4000)
        return

    messages = init.get("messages") or []
    if not messages:
        await websocket.send_json({"type": "error", "message": "no messages"})
        await websocket.close()
        return

    workspace_path = init.get("workspace_path") or x_cvc_workspace
    if not workspace_path:
        # v3.4.13 — Log loudly so a regression in the frontend is visible.
        logger.warning(
            "ws_chat_endpoint: NO workspace_path in init and no X-CVC-Workspace header. "
            "Falling back to $HOME. Frontend may have regressed."
        )
    session_id = init.get("session_id") or f"cvc_{uuid.uuid4().hex[:12]}"
    turn_id = _build_run_id(session_id)
    user_message = _extract_user_message(messages)
    conversation_history = _extract_conversation_history(messages[:-1])
    # v3.5.0 — TIME PORTAL: extract portal_session_id from init and
    # thread it through to _build_agent_sync so the chat turn is augmented
    # with the historical soul context. Skips per-turn soul updates below.
    portal_session_id = init.get("portal_session_id") if isinstance(init, dict) else None
    if portal_session_id and not isinstance(portal_session_id, str):
        portal_session_id = None

    loop = asyncio.get_running_loop()
    outbox = _ChatOutbox()
    outbox.turn_id = turn_id
    outbox.bind_loop(loop)
    seq = {"n": 0}
    # v3.3.22 — Per-turn approval gate. Same instance is reachable from
    # the WS reader (``_watch_ws_messages`` below) and from the agent
    # thread (via ``_attach_outbox_callbacks``). The gate is single-slot,
    # so each tool call gets one decision cycle.
    gate = _ApprovalGate(loop=loop, timeout_s=120.0)
    _register_gate(turn_id, gate)
    # v3.3.26 — Instrumentation
    _TURN_COUNT[0] += 1
    logger.info("cvc.chat.ws_chat_endpoint turn #%d turn_id=%s session_id=%s workspace=%s",
                _TURN_COUNT[0], turn_id[:12], session_id, workspace_path or "<none>")

    # ── C3: event spine capture (WS path) ───────────────────────────
    try:
        from cvc.events.chat_capture import ChatCapture
        chat_cap = ChatCapture(
            workspace=workspace_path,
            channel="web",
            actor="Jai",
            session_id=session_id,
            turn_id=turn_id,
        )
        chat_cap.session_start(user_message=user_message)
    except Exception as exc:  # noqa: BLE001
        logger.debug("ChatCapture init failed (non-fatal): %s", exc)
        chat_cap = None

    def _send(payload: dict) -> None:
        """Send one frame with seq + turn_id. Bounded wait to avoid stall."""
        seq["n"] += 1
        payload.setdefault("seq", seq["n"])
        payload.setdefault("turn_id", turn_id)
        # C3: spine capture per WS event (best-effort).
        if chat_cap is not None:
            try:
                etype = payload.get("type")
                if etype == "tool_start":
                    chat_cap.tool_call(
                        name=payload.get("name", "?"),
                        call_id=payload.get("call_id", ""),
                        args=payload.get("args"),
                    )
                elif etype == "tool_result":
                    err = payload.get("error")
                    chat_cap.tool_result(
                        name=payload.get("name", "?"),
                        call_id=payload.get("call_id", ""),
                        output=payload.get("output"),
                        status="err" if err else "ok",
                        error=err,
                    )
                elif etype == "error":
                    chat_cap.error(message=payload.get("message", ""))
            except Exception as exc:  # noqa: BLE001
                logger.debug("ChatCapture per-event failed: %s", exc)
        # 5s cap — if the socket is wedged, don't block the agent.
        try:
            # websocket.send_json is a coroutine — schedule it
            coro = websocket.send_json(payload)
            fut = asyncio.run_coroutine_threadsafe(coro, loop)
            fut.result(timeout=5.0)
        except Exception as exc:
            logger.debug("ws send_json failed: %s", exc)

    async def _send_async(payload: dict) -> None:
        seq["n"] += 1
        payload.setdefault("seq", seq["n"])
        payload.setdefault("turn_id", turn_id)
        try:
            await asyncio.wait_for(websocket.send_json(payload), timeout=5.0)
        except Exception as exc:
            logger.debug("ws send_json failed: %s", exc)

    # turn_start first
    await _send_async({"type": "turn_start", "turn_id": turn_id, "seq": 0})

    # Build the agent in a thread.
    try:
        agent = await loop.run_in_executor(
            None,
            lambda: _build_agent_sync(
                session_id=session_id,
                workspace_path=workspace_path,
                outbox=outbox,
                gate=gate,
                portal_session_id=portal_session_id,
            ),
        )
    except Exception as e:
        await _send_async({"type": "error", "message": f"agent init failed: {e}"})
        await _send_async({"type": "done", "turn_id": turn_id, "content": ""})
        await websocket.close()
        return

    agent_ref: list = [None]
    run_done = asyncio.Event()
    run_result_holder: dict = {}

    def _run() -> None:
        agent_ref[0] = agent
        try:
            result = agent.run_conversation(
                user_message=user_message,
                conversation_history=conversation_history,
                task_id=session_id,
            )
            run_result_holder["result"] = result
        except Exception as e:
            run_result_holder["error"] = e
        finally:
            try:
                loop.call_soon_threadsafe(run_done.set)
            except RuntimeError:
                pass
            try:
                outbox.put(None)
            except Exception:
                pass

    run_task = loop.run_in_executor(None, _run)

    # Reader: detect client disconnect + interactive messages
    # (abort / confirm). For now just detect disconnect.
    # v3.3.22 — Extended to parse ``{"type":"confirm","result":...}``
    # frames so the dashboard's approval card can resolve the gate
    # without an HTTP round-trip. The first ``type: "abort"`` frame
    # interrupts the agent immediately.
    # v3.3.26 — A separate event that fires when the WS is closed.
    # _watch_ws_messages sets it on disconnect (or raises WebSocketDisconnect
    # via ``await websocket.receive_text()``); the main loop races on
    # this event without ever cancelling the long-running task.
    # The previous implementation passed the same ``Task`` object to
    # ``asyncio.wait`` via ``asyncio.ensure_future(disconnect_task)`` and
    # then called ``disconnect_wait.cancel()`` in the keepalive path. In
    # CPython 3.10+ ``ensure_future`` on a running Task returns the Task
    # itself, so cancelling the wrapper killed the underlying
    # ``_watch_ws_messages`` coroutine — the WS reader died after the
    # first 30-second keepalive, and any outbox events that arrived
    # afterwards were silently dropped.
    disconnect_event = asyncio.Event()

    async def _watch_ws_messages() -> None:
        try:
            while True:
                raw = await websocket.receive_text()
                try:
                    msg = json.loads(raw)
                except Exception:
                    continue
                if not isinstance(msg, dict):
                    continue
                mtype = msg.get("type")
                if mtype == "confirm":
                    decision = str(msg.get("result", "deny"))
                    gate.resolve(decision)
                    logger.info("ws: confirm received decision=%s", decision)
                elif mtype == "abort":
                    try:
                        if agent_ref[0] is not None:
                            agent_ref[0].interrupt()
                    except Exception:
                        pass
                    try:
                        gate.resolve("deny")
                    except Exception:
                        pass
                    disconnect_event.set()
                    raise WebSocketDisconnect
        except WebSocketDisconnect:
            disconnect_event.set()
            try:
                if agent_ref[0] is not None:
                    agent_ref[0].interrupt()
            except Exception:
                pass
            raise

    disconnect_task = asyncio.create_task(_watch_ws_messages())
    try:
        while True:
            # Wait for the next outbox event with a keepalive timeout.
            # Using ``wait_for(outbox.get())`` avoids a subtle asyncio.Queue
            # bug: when we previously used ``asyncio.wait({create_task(outbox.get())})``
            # and then cancelled the task on timeout, the cancel would
            # discard any event that was put into the queue during the
            # window between cancel-and-recreate, causing 30-second
            # gaps between event batches at the WS layer (while the SSE
            # path that uses ``wait_for`` directly streamed in real time).
            evt = None
            try:
                evt = await asyncio.wait_for(
                    outbox.get(),
                    timeout=_KEEPALIVE_SECONDS,
                )
            except asyncio.TimeoutError:
                # No event for KEEPALIVE_SECONDS — emit keepalive
                # ping so the dashboard's lastEventAt watchdog
                # doesn't fire.
                if not run_done.is_set():
                    await _send_async({"type": "ping"})
                continue

            if disconnect_event.is_set():
                break

            if evt is None:
                # End-of-run sentinel from _run()
                break

            await _send_async(evt)

            if run_done.is_set():
                # Drain remaining events.
                while not outbox.empty():
                    extra = outbox.get_nowait()
                    if extra is None:
                        continue
                    await _send_async(extra)
                break

    except WebSocketDisconnect:
        try:
            if agent_ref[0] is not None:
                agent_ref[0].interrupt()
        except Exception:
            pass
    finally:
        for t in (run_task, disconnect_task):
            if not t.done():
                t.cancel()

        # Terminal done frame.
        final_text = ""
        if "result" in run_result_holder:
            result = run_result_holder["result"] or {}
            final_text = (
                result.get("response")
                or result.get("final_response")
                or "".join(outbox.streamed_text)
            )
            if result.get("failed"):
                await _send_async({
                    "type": "error",
                    "message": result.get("error") or "Agent run failed",
                })
            # v3.3.21 — Mirror SSE path: surface guardrail halts so the
            # dashboard can show "the agent stopped itself because the
            # same read_file was called 4 times" instead of an unexplained
            # silence. See the same code in chat_endpoint (SSE) for the
            # full rationale.
            guardrail = result.get("guardrail")
            if guardrail:
                await _send_async({
                    "type": "guardrail_halt",
                    "turn_id": turn_id,
                    "tool_name": guardrail.get("tool_name", ""),
                    "code": guardrail.get("code", ""),
                    "message": guardrail.get("message", ""),
                    "count": guardrail.get("count", 0),
                })
        elif "error" in run_result_holder:
            await _send_async({
                "type": "error",
                "message": str(run_result_holder["error"]),
            })
        await _send_async({"type": "done", "turn_id": turn_id, "content": final_text})

        # C3: capture the assistant's final message + session_end (WS).
        if chat_cap is not None:
            try:
                tokens_in = 0
                tokens_out = 0
                result_for_tokens = run_result_holder.get("result") or {}
                if isinstance(result_for_tokens, dict):
                    tokens_in = int(result_for_tokens.get("tokens_in") or 0)
                    tokens_out = int(result_for_tokens.get("tokens_out") or 0)
                chat_cap.assistant_message(
                    text=final_text,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                )
                chat_cap.session_end(
                    status="err" if run_result_holder.get("error") or run_result_holder.get("result", {}).get("failed") else "ok",
                )
            except Exception as exc:  # noqa: BLE001
                logger.debug("ChatCapture final capture failed: %s", exc)

        # v3.3.22 — Unregister the gate. Idempotent.
        _unregister_gate(turn_id)

        # ── Auto-skill reflection hook (mirror of the SSE path) ────
        # Emit a `skill_drafted` event if the reflection produced a
        # draft. Failures must never break the response.
        try:
            from cvc.agent.auto_skill import maybe_create_draft
            draft_result = maybe_create_draft(
                session_id=session_id,
                turn_id=turn_id,
                user_message=user_message,
                outbox_events=outbox.tool_events,
                final_response=final_text,
                workspace_path=workspace_path,
            )
            if draft_result and draft_result.get("drafted"):
                logger.info(
                    "auto-skill: drafted %s (confidence=%.2f) from turn %s",
                    draft_result.get("name"),
                    draft_result.get("confidence", 0.0),
                    turn_id,
                )
                await _send_async({
                    "type": "skill_drafted",
                    "turn_id": turn_id,
                    "name": draft_result.get("name"),
                    "path": draft_result.get("path"),
                    "confidence": draft_result.get("confidence", 0.0),
                })
        except Exception as e:  # pragma: no cover — best-effort
            logger.debug("auto-skill reflection failed: %s", e)

        # ── Per-turn soul auto-encoder (H2 wiring — mirror of SSE) ──
        # hotfix/soul-wiring-2026-06-30 — this is the path the
        # dashboard uses (POST /api/chat and /api/ws/chat). Before
        # this patch, the soul only learned during channel-adapter
        # message ingestion, so dashboard chats never updated
        # user_model.json and the Soul page rendered permanently
        # empty. The hook writes to <workspace>/.cvc/user_model.json
        # exactly the way the Soul page reads it. Best-effort.
        #
        # v3.5.0 → v3.5.1 — TIME PORTAL: changed from "skip in portal mode" to
        # "always write, but label portal-mode turns with [portal:{date}]".
        # Same pattern as the HTTP path — see comment there for rationale.
        try:
            from cvc.operations.per_turn_soul import fire_and_forget_update
            user_msg_for_soul = user_message
            assistant_text_for_soul = final_text
            if portal_session_id:
                try:
                    from cvc.gateway.soul import _load_portal_sessions
                    _psess = _load_portal_sessions().get(portal_session_id) or {}
                    _pdate = (
                        _psess.get("date")
                        or _psess.get("iso_date")
                        or "unknown"
                    )
                    _pscope = _psess.get("scope", "snapshot")
                    _plabel = f"[portal:{_pdate}][{_pscope}] "
                    user_msg_for_soul = _plabel + (user_message or "")
                    assistant_text_for_soul = _plabel + (final_text or "")
                except Exception:  # noqa: BLE001
                    pass
            fire_and_forget_update(
                user_message=user_msg_for_soul,
                assistant_text=assistant_text_for_soul,
                workspace_path=workspace_path,
            )
        except Exception as e:  # pragma: no cover — best-effort
            logger.debug("per-turn soul hook (ws) failed: %s", e)


# -----------------------------------------------------------------------------
# HTTP approval routes — v3.3.22
# -----------------------------------------------------------------------------
#
# These mirror the legacy gateway's ``/api/chat/confirm`` and
# ``/api/chat/approval-mode`` endpoints so HTTP-only callers (curl scripts,
# the legacy agent_chat path, external integrations) can resolve approvals
# without going through WebSockets. The dashboard's WS confirm path is
# preferred — these routes exist for fallback + parity.
#
# Both routes consult the legacy module state directly (single source of
# truth shared with the dashboard's ApprovalModeSwitcher pill).

@router.post("/chat/confirm")
async def confirm_tool_endpoint(request: Request):
    """Resolve a pending tool approval via HTTP.

    Body: ``{"decision": "allow_once" | "allow_always" | "trust_all" | "deny" | "deny_suggest", "turn_id": "..." (optional)}``
    Returns: ``{"ok": true, "decision": "..."}``

    Routes the decision to BOTH:
      1. The legacy ``_set_tool_confirm`` machinery (for legacy ``agent_chat`` turns).
      2. The per-turn ``_ApprovalGate`` in this chat router's registry (for
         new ``/api/chat`` and ``/api/ws/chat`` turns). If ``turn_id`` is
         provided, that gate is preferred; otherwise the most recently
         registered gate wins.
    """
    try:
        body = await request.json()
    except Exception:
        return {"ok": False, "error": "invalid json body"}
    raw = str(body.get("decision", "deny"))
    if raw == "allow":
        raw = "allow_once"
    if raw not in _VALID_DECISIONS:
        raw = "deny"
    turn_id = body.get("turn_id")
    # 1. Resolve the new chat router's per-turn gate first (this is the
    #    dashboard's actual pending gate for the current request).
    try:
        gate = _resolve_active_gate(turn_id=turn_id)
        if gate is not None and gate.is_pending:
            gate.resolve(raw)
            logger.info("HTTP /api/chat/confirm → gate resolved decision=%s turn_id=%s", raw, turn_id)
    except Exception as e:
        logger.debug("gate resolve failed: %s", e)
    # 2. Fan out to legacy in-flight turns.
    try:
        import cvc.gateway_legacy as _legacy
        _legacy._set_tool_confirm(evt=_legacy._tool_confirm_event, result=raw)
        if _legacy._tool_confirm_event is not None:
            _legacy._tool_confirm_event.set()
        for _ts in list(_legacy._active_turns.values()):
            try:
                _ts.client_queue.put_nowait({"type": "confirm", "result": raw})
            except Exception:
                pass
    except Exception:
        pass
    logger.info("HTTP /api/chat/confirm → decision=%s", raw)
    return {"ok": True, "decision": raw}


@router.get("/chat/approval-mode")
async def get_approval_mode_endpoint():
    """Return the current approval mode + safe-tool count.

    Body: ``{"mode": "default" | "bypass" | "autopilot", "safe_tool_count": N}``
    """
    mode, safe_tools = _resolve_approval_mode()
    return {"mode": mode, "safe_tool_count": len(safe_tools)}


@router.post("/chat/approval-mode")
async def set_approval_mode_endpoint(request: Request):
    """Set the approval mode. Forwards to the legacy module state."""
    try:
        body = await request.json()
    except Exception:
        return {"error": "invalid json body"}
    mode = str(body.get("mode", "default")).lower()
    if mode not in ("default", "bypass", "autopilot"):
        return {"error": f"invalid mode: {mode}"}
    try:
        import cvc.gateway_legacy as _legacy
        _legacy._approval_mode = mode  # type: ignore[attr-defined]
        # If switching to bypass/autopilot while a tool is waiting,
        # auto-allow it (matches legacy gateway_legacy.py:8523).
        if mode in ("bypass", "autopilot") and _legacy._tool_confirm_event is not None:
            _legacy._set_tool_confirm(evt=_legacy._tool_confirm_event, result="allow_once")
            try:
                _legacy._tool_confirm_event.set()
            except Exception:
                pass
            for _ts in list(_legacy._active_turns.values()):
                try:
                    _ts.client_queue.put_nowait({"type": "confirm", "result": "allow_once"})
                except Exception:
                    pass
    except Exception as e:
        return {"error": str(e)}
    logger.info("HTTP /api/chat/approval-mode → mode=%s", mode)
    return {"mode": mode}


@router.get("/chat/diagnostics")
async def chat_diagnostics_endpoint():
    """Return the v3.3.26 instrumentation counters.

    Body: ``{
        "deltas_total": int,          # total text deltas since process start
        "delta_chars_total": int,     # cumulative chars in all deltas
        "tools_total": int,           # total tool_start events since process start
        "turns_total": int,           # total turns since process start
    }``

    These are the per-process counters incremented inside
    ``_on_delta`` / ``_on_tool_start``. They are the only way to tell
    the difference between
      (a) the agent never produced deltas (counter stays at 0)
      (b) the agent produced deltas but the dashboard renderer
          skipped them (counter is high but the user sees a flash)
      (c) everything is fine (counter is high AND the user sees
          text appear gradually)
    without having to attach a debugger to the running daemon.
    """
    return {
        "deltas_total": _DELTA_COUNT[0],
        "delta_chars_total": _DELTA_TOTAL_CHARS[0],
        "tools_total": _TOOL_COUNT[0],
        "turns_total": _TURN_COUNT[0],
    }
