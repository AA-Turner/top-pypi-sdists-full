"""How many bytes the hosted MCP hands back to a coding agent, per tool call.

WHY HERE AND NOWHERE ELSE
-------------------------
The question is "how much of a customer's agent context is Probe?", and the only
honest place to answer it is the last point the bytes are ours. The backend API
cannot: `service._fit` / `_fit_sections` trim the payload to the caller's
`token_budget` INSIDE this process, so the API's response is pre-trim and always an
over-estimate. The agent cannot be asked either. So: count what leaves this server.

HOSTED ONLY, on purpose. A stdio MCP runs on the user's machine as a child of their
agent; we do not instrument it. `with_auth_and_health` is the hosted wrapper, so
wiring the counter there is what makes that boundary structural rather than a
convention someone later forgets.

BYTES, NOT CHARACTERS, and the name says so. ASGI hands us encoded bytes; for
non-ASCII payloads (names, notes, prose -- ordinary research content) a character is
1-4 of them. `response_bytes` is what we can count without decoding every body, and
naming it honestly is what stops someone downstream dividing it as if it were
characters.

REFERENCE TOKENS ARE NOT BILLED TOKENS. The final MCP boundary may provide its exact
frozen o200k_base count and UTF-8 text bytes, effective budget and continuation flag.
Those are prepared content measurements, separate from ASGI bytes actually sent;
neither proves what a client's model received or billed. Never derive tokens by
dividing response_bytes. Older callers that provide no final measurement retain
their existing event shape.

WHY ARGUMENT DIMENSIONS ARE CLOSED AND CONTENT IS EXCLUDED
--------------------------------------------------------
Entity views have different cost shapes: a compact card, a row page, and a complete
document walk answer different questions. All final responses now share the same
hard limit, but combining their measurements still hides useful distinctions.

`view` is validated against the closed enum `contract.View`; the effective budget
is a validated integer limit. Staleness is either `source_changed` or absent. No
free-form argument or error belongs here: `search_knowledge(query=...)` is literally
the user's text, and this file's whole contract is counts, never content.

WHAT IS DELIBERATELY NOT COUNTED
--------------------------------
Only TOOL RESPONSES. `initialize` and `tools/list` traffic is excluded, which falls
out of only emitting when a tool actually ran. That exclusion is a decision, not an
oversight: MCP_INSTRUCTIONS (1,005 chars) plus `tools/list` (31,738) are ~32KB,
roughly 8.4k tokens per session that loads them -- deferred since 2026-09-06:
`.mcp.json` no longer sets `alwaysLoad`, so the client lazy-loads the tool
schemas on demand and sessions that never reach for Probe pay ~nothing. When
they ARE loaded they arrive whole, so every budget argument in this tree still
holds. Whether that exceeds
tool-response traffic is exactly what this event will let us find out. It is tracked
separately in TODOS.md: a constant per release does not need per-request
instrumentation.

THE TOOL NAME CROSSES A THREAD
------------------------------
`server._tool`'s inner `_invoke` runs each tool body through `anyio.to_thread.run_sync`,
and that worker gets a COPY of the calling context. Rebinding a ContextVar inside that copy is invisible out
here, so the ContextVar holds a MUTABLE dict and the worker mutates it in place. This
is the one non-obvious thing in the file; get it wrong and every event lands with
`tool: None` while every test still passes.

SELF-HOSTERS EMIT NOTHING
-------------------------
`probe-research-mcp-http` is a published console script, so "hosted" is not a place --
it is a deployment anyone can run. Without a gate, a self-hoster would ship their OWN
users' ids, tools and session ids to the vendor's PostHog using the embedded capture
key, which is exactly what `tests/selfhost/test_egress.py` exists to prevent.

The gate is an EXPLICIT OPT-IN (`PROBE_MCP_ANALYTICS=1`), set only in our own
Deployment, plus the usual `PROBE_TELEMETRY` killswitch.

It is deliberately NOT the `hosted_base_url(resolve().base_url)` check the client
surfaces use, and the reason is worth keeping: this pod talks to the API over
`http://research-os.research.svc.cluster.local:8080` (deploy/mcp/k8s.yaml) to avoid a
load-balancer hairpin. That is neither https nor a prbe.ai host, so the client gate
answers "self-hosted" for our own production fleet and silences the feature entirely --
with every unit test still green, because no unit test sets that variable.
tests/test_mcp_accounting.py reads the real manifest to keep that from recurring.

DELIVERY NEVER TOUCHES THE REQUEST
----------------------------------
`_telemetry_core.post_batch` is blocking urllib. Emission hands off to a bounded queue
drained by one daemon thread, so a slow or dead PostHog costs a tool call nothing. A
full queue drops. Nothing in this module raises: the whole file is wrapped in the same
contract as `capture()` -- observability must never become observable.

(The CLI's `_Sender` does the same job, but it lives in `cli/`, which `deploy-mcp.yml`
deliberately excludes from the hosted MCP's rebuild filter. Importing it would either
fail `tests/test_deploy_scope.py` or -- lazily -- pass it while leaving this service
running stale code. Hence a small sender of our own, inside the closure.)
"""

from __future__ import annotations

import atexit
import contextvars
import logging
import os
import queue
import threading
from datetime import datetime, timezone
from typing import Any, Literal

from ..client_headers import CLIENT_KIND_HEADER, CLIENT_VERSION_HEADER
from .contract import View
from ..sdk import _telemetry_core as core
from ..sdk.agent_session import (
    AGENT_HEADER,
    AGENT_SESSION_HEADER,
    AGENTS,
    HIDE_SESSION_WORK_HEADER,
    valid_session_id,
)
from .budget import MAX_TOKENS, MIN_TOKENS

_logger = logging.getLogger(__name__)

#: PostHog event name. `mcp.` prefixed to sit beside the other surface-scoped events.
EVENT_TOOL_SERVED = "mcp.tool_served"

#: Explicit opt-in. Set in deploy/mcp/k8s.yaml and nowhere else; absent means silent.
ANALYTICS_ENV = "PROBE_MCP_ANALYTICS"

# A fixed reference metric, not a claim about the caller's model or billing.
REFERENCE_ENCODING = "o200k_base_frozen_v1"
_DELIVERY_PROPERTIES = frozenset(
    {
        "reference_tokens",
        "reference_encoding",
        "response_text_bytes",
        "token_budget",
        "has_continuation",
        "stale_reason",
    }
)

#: Only agents whose transcripts actually reach Research OS may be named: a session id
#: we can never resolve to a transcript is a dead link, and recording it invites someone
#: to chase it. DERIVED from `sdk.agent_session.AGENTS` rather than restated, so a fourth
#: captured agent cannot be silently dropped here. (The backend expresses the same set as
#: `app.runs.agent_session.CAPTURED_AGENTS`, a module the MCP cannot import.)
_CAPTURED_AGENTS = frozenset(spec.label for spec in AGENTS if spec.captured)

#: Bounded so a wedged sender cannot grow without limit. Overflow drops, silently and
#: deliberately: losing a count is acceptable, delaying a tool call is not.
_QUEUE_MAX = 1000

#: The per-request holder. A MUTABLE dict, never rebound by the worker thread -- see
#: the module docstring. None outside a hosted request (stdio, lifespan, tests).
_request: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar(
    "probe_mcp_accounting_request", default=None
)


class _Sender:
    """One queue, one daemon thread, silence everywhere."""

    def __init__(self) -> None:
        self.q: queue.Queue = queue.Queue(maxsize=_QUEUE_MAX)
        self.transport = core.post_batch  # test seam
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._stop = object()

    def start(self) -> None:
        with self._lock:
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(
                    target=self._run, daemon=True, name="probe-mcp-accounting"
                )
                self._thread.start()

    def put(self, entry: dict) -> None:
        try:
            self.q.put_nowait(entry)
        except Exception:
            pass  # full queue: drop, never block the request

    def request_flush(self, timeout: float = 2.0) -> None:
        """Enqueue the stop sentinel and join, bounded. Drops what misses the bound:
        the daemon thread dies with the process, which is the accepted-loss path."""
        try:
            self.q.put_nowait(self._stop)
        except Exception:
            # Queue full -- which is EXACTLY when a flush matters. Make room rather
            # than dropping the sentinel and then waiting 2s for a drain that was
            # never told to finish.
            try:
                self.q.get_nowait()
                self.q.put_nowait(self._stop)
            except Exception:
                pass
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout)

    def _run(self) -> None:
        while True:
            item = self.q.get()
            saw_stop = item is self._stop
            batch = [] if saw_stop else [item]
            while True:
                try:
                    nxt = self.q.get_nowait()
                except queue.Empty:
                    break
                if nxt is self._stop:
                    saw_stop = True
                else:
                    batch.append(nxt)
            if batch:
                try:
                    self.transport(batch)
                except Exception:  # PostHog down costs a tool call nothing
                    pass
            if saw_stop:
                return


_sender: _Sender | None = None
_sender_lock = threading.Lock()
_flush_registered = False


def _flush_at_exit() -> None:
    """Bounded final drain. A pod rolling out mid-batch would otherwise drop whatever
    was queued, which reads downstream as a usage dip rather than a deploy."""
    sender = _sender
    if sender is not None:
        try:
            sender.request_flush()
        except BaseException:  # noqa: BLE001 - never let exit reporting raise at exit
            pass


def _ensure_sender() -> _Sender:
    global _sender, _flush_registered
    with _sender_lock:
        if _sender is None:
            _sender = _Sender()
        _sender.start()
        if not _flush_registered:
            atexit.register(_flush_at_exit)
            _flush_registered = True
        return _sender


def _telemetry_permitted() -> bool:
    """Whether this deployment may emit at all. Fails CLOSED.

    Two gates, both fail-closed:
      * `PROBE_MCP_ANALYTICS=1` -- an explicit opt-in only our own Deployment sets.
        Anything else (unset, empty, "0") means no. A self-hoster who configures
        nothing therefore emits nothing, which is the safe default for a promise
        about egress.
      * `core.telemetry_disabled()` -- the PROBE_TELEMETRY killswitch, so the same
        spelling that silences every other surface silences this one.
    Any error answering the question is answered as "no".
    """
    try:
        if (os.environ.get(ANALYTICS_ENV) or "").strip() != "1":
            return False
        return not core.telemetry_disabled()
    except Exception:
        return False


def agent_from_headers(headers: dict[bytes, bytes]) -> tuple[str | None, str | None]:
    """``(agent, session_id)`` from raw ASGI headers; either half may be None.

    Untrusted input from the caller's plugin, so it is validated the same way the
    backend validates it (`app.runs.agent_session.agent_session_from_request`): a
    non-captured agent or a session id failing the charset/length bound yields None
    rather than a value nobody can resolve. Absent beats wrong.
    """
    try:
        raw_agent = headers.get(AGENT_HEADER.lower().encode(), b"").decode("ascii")
        raw_session = headers.get(AGENT_SESSION_HEADER.lower().encode(), b"").decode("ascii")
    except UnicodeDecodeError:
        return (None, None)
    agent = raw_agent if raw_agent in _CAPTURED_AGENTS else None
    session = raw_session if agent and valid_session_id(raw_session) else None
    return (agent, session)


def hide_session_work_from_headers(headers: dict[bytes, bytes]) -> bool:
    """Whether the caller sent `X-Probe-Hide-Session-Work: 1`.

    Exactly "1", nothing looser: an opt-in that narrows what a read returns
    must not switch on from a typo or a value some proxy invented. It asks for
    nothing by itself -- `session_work_to_hide` pairs it with the caller's
    session, and without one there is nothing to hide.
    """
    return headers.get(HIDE_SESSION_WORK_HEADER.lower().encode(), b"").strip() == b"1"


def begin_request(
    agent: str | None,
    session_id: str | None,
    client_headers: dict,
    *,
    hide_session_work: bool = False,
) -> dict:
    """Open a holder for one hosted request and bind it.

    `client_headers` is the already-VALIDATED pair from `client_version_headers` --
    `{}` when the caller reported nothing or reported it malformed. We read the
    caller's kind/version out of it rather than our own, for the same reason
    `client_headers_scope` exists: hosted, our own version is the server's, not
    theirs.
    """
    validated = client_headers or {}
    holder: dict[str, Any] = {
        "agent": agent,
        "agent_session_id": session_id,
        # Request state, not telemetry: `emit` never reads it.
        "hide_session_work": bool(hide_session_work),
        "client_kind": validated.get(CLIENT_KIND_HEADER),
        "client_version": validated.get(CLIENT_VERSION_HEADER),
        "tool": None,
        "view": None,
        "response_bytes": 0,
    }
    return {"holder": holder, "token": _request.set(holder)}


def end_request(state: dict) -> None:
    try:
        _request.reset(state["token"])
    except Exception:
        pass


def calling_agent_session() -> tuple[str, str] | None:
    """The ``(agent, session_id)`` of the caller, from the request headers.

    The AMBIENT half of self-exclusion. `agent_from_headers` already validated
    both halves at the ASGI boundary, so this is a read of a decided fact, not a
    second parse.

    None whenever either half is missing -- a non-captured agent, a session id
    that failed the charset/length bound, a stdio server with no per-request
    headers, or (today) any Codex caller: Codex connects its MCP servers before
    a thread id exists, so `X-Probe-Agent-Session` is simply absent there. That
    is exactly why the tool takes an explicit override as well.
    """
    holder = _request.get()
    if holder is None:
        return None
    agent = holder.get("agent")
    session_id = holder.get("agent_session_id")
    if not agent or not session_id:
        return None
    return (agent, session_id)


def session_work_to_hide() -> str | None:
    """The session whose OWN work this request's reads leave out, or None.

    Only when the caller opted in (`X-Probe-Hide-Session-Work: 1`) AND the
    AMBIENT `X-Probe-Agent-Session` names a session. Always the ambient one,
    never a tool argument: the header is set by the process that runs the model
    (the daemon's reader), and a model that could pass another id -- through
    search_knowledge's `exclude_session`, say -- could switch which session's
    work is hidden, un-hiding its own. `exclude_session` still drives the
    transcript self-exclusion, which is a different filter. None outside a
    hosted request (stdio, tests), so nothing changes there.
    """
    holder = _request.get()
    if holder is None or not holder.get("hide_session_work"):
        return None
    ambient = calling_agent_session()
    return ambient[1] if ambient else None


def note_view(value: object) -> None:
    """Record which `get_entity` view is being served, when it is a known one.

    Validated against `contract.View`, not merely bounded: an unrecognised value is
    dropped rather than recorded. That keeps the property a closed dimension even
    though the argument arrives from the caller -- the service rejects an invalid view
    anyway, so there is nothing lost by not naming it here.
    """
    if not isinstance(value, str):
        return
    try:
        View(value)
    except ValueError:
        return
    holder = _request.get()
    if holder is not None:
        holder["view"] = value


def note_tool(name: str) -> None:
    """Record which tool is being served. Called from the worker thread.

    Mutates the dict in place. Assigning to the ContextVar here would be lost: the
    worker runs on a COPY of the context.
    """
    holder = _request.get()
    if holder is not None:
        holder["tool"] = name


def note_delivery(
    *,
    reference_tokens: int,
    response_text_bytes: int,
    token_budget: int,
    has_continuation: bool,
    stale_reason: Literal["source_changed"] | None = None,
) -> None:
    """Attach final prepared-content measurements to the existing hosted event.

    No payload, cursor, source identifier or free-form error is accepted. Counts
    are not clamped to the budget: a future boundary regression must remain visible.
    The final measurement replaces any earlier one; it is never summed. Stdio has
    no holder and remains silent. This function never creates a sender or raises.
    """
    try:
        holder = _request.get()
        if holder is None:
            return
        if (
            type(reference_tokens) is not int
            or reference_tokens < 0
            or type(response_text_bytes) is not int
            or response_text_bytes < 0
            or type(token_budget) is not int
            or not MIN_TOKENS <= token_budget <= MAX_TOKENS
            or type(has_continuation) is not bool
        ):
            holder.pop("delivery", None)
            return
        delivery = {
            "reference_tokens": reference_tokens,
            "reference_encoding": REFERENCE_ENCODING,
            "response_text_bytes": response_text_bytes,
            "token_budget": token_budget,
            "has_continuation": has_continuation,
        }
        if type(stale_reason) is str and stale_reason == "source_changed":
            delivery["stale_reason"] = stale_reason
        holder["delivery"] = delivery
    except Exception:
        pass


def counting_send(state: dict, send: Any) -> Any:
    """Wrap an ASGI ``send`` so response body bytes are accumulated into the holder."""
    holder = state["holder"]

    async def _send(message: dict) -> None:
        # Count AFTER the send returns. Counting first would bill a client for bytes
        # it never received when the connection drops mid-response, and the emit in
        # the wrapper's `finally` would then ship that inflated number.
        await send(message)
        if message.get("type") == "http.response.body":
            body = message.get("body")
            # bytes-like ONLY. A str body (a different ASGI server, a test double)
            # has a len() too, and counting its CHARACTERS into a field named
            # response_bytes would be wrong in exactly the silent way this whole
            # module is trying to avoid. Skip it instead.
            if isinstance(body, (bytes, bytearray, memoryview)):
                holder["response_bytes"] += len(body)

    return _send


def emit(state: dict, identity: dict | None) -> None:
    """Queue one `mcp.tool_served` event. Never raises.

    A no-op unless a tool actually ran: `initialize` and `tools/list` share this path
    and are deliberately out of scope (see the module docstring).
    """
    try:
        holder = state["holder"]
        tool = holder.get("tool")
        if not tool:
            return
        if not _telemetry_permitted():
            return
        ident = identity or {
            "distinct_id": "unknown",
            "customer_id": None,
            "workspace_id": None,
            "authenticated": False,
        }
        # Email is deliberately NOT forwarded. `build_batch` would write it onto the
        # PostHog person via `$set`, and the distinct_id already merges with the
        # dashboard's identify -- so carrying it would add an identifiable field for
        # no analytical gain, on the exact surface where account deletion is already
        # a known gap.
        ident = {k: v for k, v in ident.items() if k != "email"}
        properties: dict[str, Any] = {"tool": tool, "response_bytes": holder["response_bytes"]}
        delivery = holder.get("delivery")
        if isinstance(delivery, dict):
            properties.update(
                {key: delivery[key] for key in _DELIVERY_PROPERTIES if key in delivery}
            )
        if holder.get("view"):
            properties["view"] = holder["view"]
        if holder.get("agent"):
            properties["agent"] = holder["agent"]
        if holder.get("agent_session_id"):
            properties["agent_session_id"] = holder["agent_session_id"]
        # The CALLER's client, not ours. "mcp" when they reported nothing, which is
        # still true of them and keeps the surface breakdown complete.
        # Stamp at EMIT. Delivery is a queue drained by one thread doing blocking
        # POSTs, so without this the time axis is ingestion time -- and a PostHog
        # slowdown would silently skew the whole series.
        entries = core.build_batch(
            [
                {
                    "event": EVENT_TOOL_SERVED,
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                    "properties": properties,
                }
            ],
            ident,
            client_kind=holder.get("client_kind") or "mcp",
            lib="probe-mcp",
            client_version=holder.get("client_version"),
            # EXPLICIT, including None. Letting build_batch detect would read the
            # POD's environment and stamp our own label onto every caller who sent
            # no agent header -- the same mislabelling this release fixes clientside.
            agent=holder.get("agent"),
        )
        _ensure_sender().put(entries[0])
    except Exception as exc:  # observability must never become observable
        _logger.debug("mcp accounting emit failed: %s", exc)
