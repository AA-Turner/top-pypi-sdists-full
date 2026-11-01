"""How many bytes the hosted MCP hands a coding agent per tool call, counted where the bytes
leave us (hosted only; bytes, not characters; reference tokens are not billed tokens; counts and
uuid refs, never content). Why, and the thread/opt-in traps: DESIGN.md."""


from __future__ import annotations

import atexit
import contextvars
import logging
import os
import queue
import threading
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Literal

from ...foundation.request_identity.request_identity import CLIENT_KIND_HEADER, CLIENT_VERSION_HEADER
from ...shared.reads.search_contract import EntityType
from ..generated.views import View
from ...analytics import core as core
from ...analytics.events import EVENT_MCP_TOOL_SERVED
from ...sdk.agent_session import (
    AGENT_HEADER,
    AGENT_SESSION_HEADER,
    AGENTS,
    HIDE_SESSION_WORK_HEADER,
    valid_session_id,
)
from ...sdk.delivery.transport.headers import queued_session_scope
from ...foundation.token_budget.token_budget import MAX_TOKENS, MIN_TOKENS

_logger = logging.getLogger("probe.mcp.accounting")  # the old module's name (agent:17)  restructure-guard-ok: a logger name, not an import

#: PostHog event name (the catalog's). `mcp.` prefixed to sit beside the other surface-scoped events.
EVENT_TOOL_SERVED = EVENT_MCP_TOOL_SERVED

#: Explicit opt-in, set only in deploy/mcp/k8s.yaml; absent = silent.
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

#: Only agents whose transcripts reach Research OS may be named (an unresolvable session id is a
#: dead link). DERIVED from `sdk.agent_session.AGENTS` so a fourth captured agent is not silently
#: dropped; the backend's twin is `app.runs.agent_session.CAPTURED_AGENTS` (the MCP cannot import it).
_CAPTURED_AGENTS = frozenset(spec.label for spec in AGENTS if spec.captured)

#: Bounded so a wedged sender cannot grow. Overflow drops silently: losing a count is fine, delaying a tool call is not.
_QUEUE_MAX = 1000

#: Per-request holder: a MUTABLE dict, never rebound by the worker thread (DESIGN.md). None outside a hosted request.
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
            # Queue full is EXACTLY when a flush matters: make room, or the sentinel drops and we wait 2s for a drain never told to finish.
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


@contextmanager
def caller_session_scope() -> Iterator[None]:
    """Send the backend calls in this block as the CALLER's coding-agent session.

    Hosted, the SDK transport would name this server process's own session (it
    reads its own environment), never the caller's, so the API could not say
    which session searched. This binds the caller's validated pair
    (`calling_agent_session`) as the outbound `X-Probe-Agent` /
    `X-Probe-Agent-Session`, or binds NO session when the caller sent none:
    the pod never lends its own. A no-op outside a hosted request (stdio runs
    inside the caller's own session and already sends it).
    """
    if _request.get() is None:
        yield
        return
    caller = calling_agent_session()
    with queued_session_scope(f"{caller[0]}:{caller[1]}" if caller else None):
        yield


def session_work_to_hide() -> str | None:
    """The session whose OWN work this request's reads leave out, or None.

    Only when the caller opted in (`X-Probe-Hide-Session-Work: 1`) AND the
    AMBIENT `X-Probe-Agent-Session` names a session. Always the ambient one,
    never a tool argument: the header is set by the process that runs the model
    (the daemon's reader), and a model that could pass another id -- through
    search's `exclude_session`, say -- could switch which session's
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


#: Every `kind:` a read ref may carry (`contract.EntityType`).
_REF_KINDS = frozenset(kind.value for kind in EntityType)

#: At most this many read ids on one event; `entity` takes up to 20 refs.
_MAX_READ_IDS = 20


def _id_ref(ref: object) -> str | None:
    """`ref` when it names a record BY ID -- `<kind>:<uuid>`, or
    `session:<agent>/<uuid>` for a captured agent -- with the uuid lowercased;
    None for a slug, a name or anything malformed. A slug or a name is the
    caller's own text (`run:prophetic-manatee-987`, `artifact:<name>`), and
    this module records ids, never text."""
    if not isinstance(ref, str):
        return None
    kind, sep, rest = ref.partition(":")
    if not sep or kind not in _REF_KINDS:
        return None
    agent, slash, raw = rest.rpartition("/")
    if slash and (kind != EntityType.SESSION or agent not in _CAPTURED_AGENTS):
        return None
    try:
        value = str(uuid.UUID(raw))
    except ValueError:
        return None
    if raw.lower() != value:  # braces, urn: and bare hex are not how ids are written
        return None
    return f"{kind}:{agent}/{value}" if slash else f"{kind}:{value}"


def note_refs(refs: object) -> None:
    """Record which records a read tool was asked for, so a search
    (`search_performed.result_doc_ids`) joins to the reads that follow it.

    Ids only (`_id_ref`): a ref given by slug or name is counted in
    `read_ref_count` and never recorded. A no-op for a tool with no `refs`
    argument and under stdio, where no holder is bound.
    """
    if not isinstance(refs, (list, tuple)):
        return
    holder = _request.get()
    if holder is None:
        return
    ids = [found for ref in refs if (found := _id_ref(ref))]
    holder["read_ids"] = list(dict.fromkeys(ids))[:_MAX_READ_IDS]
    holder["read_ref_count"] = len(refs)


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
        if "read_ref_count" in holder:
            properties["read_ids"] = holder.get("read_ids") or []
            properties["read_ref_count"] = holder["read_ref_count"]
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
