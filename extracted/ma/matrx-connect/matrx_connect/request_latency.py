"""Always-on request → first provider call latency (independent of CHAT_TIME_CHECK)."""

from __future__ import annotations

import re
import time
import uuid
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import UTC, datetime

_AI_ROUTE_PREFIXES = (
    "/agents",
    "/agent/",
    "/conversations",
    "/conversation/",
    "/chat",
    "/manual",
    "/prompts",
    "/prompt/",
    "/ai/",
    "/mandates",
)

CLIENT_SENT_AT_HEADER = "x-matrx-client-sent-at"
CLIENT_PREP_MS_HEADER = "x-matrx-client-prep-ms"


@dataclass(frozen=True)
class ClientLatencyStamp:
    """What the client said about its half of the request, plus when we saw it.

    ``server_arrived_at_ms`` is OUR wall clock at the earliest hook; ``client_sent_at_ms``
    is the CLIENT's wall clock at submission, so ``network_ms`` carries clock skew —
    it is an estimate, never a measurement (negative values are real and kept).
    """

    server_arrived_at_ms: int
    client_sent_at_ms: int | None
    client_prep_ms: int | None
    route: str

    @property
    def network_ms(self) -> int | None:
        if self.client_sent_at_ms is None:
            return None
        return self.server_arrived_at_ms - self.client_sent_at_ms

    @property
    def server_arrived_at(self) -> datetime:
        return datetime.fromtimestamp(self.server_arrived_at_ms / 1000, tz=UTC)

    @property
    def client_sent_at(self) -> datetime | None:
        if self.client_sent_at_ms is None:
            return None
        return datetime.fromtimestamp(self.client_sent_at_ms / 1000, tz=UTC)


_client_stamp: ContextVar[ClientLatencyStamp | None] = ContextVar(
    "request_latency_client_stamp", default=None
)


def _int_header(headers: object, name: str) -> int | None:
    raw = headers.get(name) if headers is not None else None  # type: ignore[attr-defined]
    if raw is None:
        return None
    try:
        return int(float(raw))
    except (TypeError, ValueError):
        return None


def get_client_latency_stamp() -> ClientLatencyStamp | None:
    return _client_stamp.get()


_VERSION_SEGMENT = re.compile(r"^/v\d+(?=/)")


def unversioned_path(path: str) -> str:
    """``path`` with a leading ``/api`` mount and ``/vN`` version segment removed.

    A prefix check against the bare route names must see through any version
    segment, or a versioned request silently goes unmeasured (2026-10-03: every
    Agent Battle turn on the since-removed ``/v2/ai/...`` recorded no
    time-to-first-token).
    """
    if path.startswith("/api/"):
        path = path[len("/api") :]
    return _VERSION_SEGMENT.sub("", path, count=1)


def is_ai_route(path: str) -> bool:
    """True for every AI route, versioned or not (see ``unversioned_path``)."""
    bare = unversioned_path(path)
    return any(bare.startswith(prefix) for prefix in _AI_ROUTE_PREFIXES)


@dataclass
class RequestLatencyClock:
    """THE THREE LEGS of one AI HTTP request, on ONE server clock (``time.perf_counter``).

    * LEG 1 (ours, before): arrival -> ``provider_call_at`` (``server_prep_ms``);
    * LEG 2 (provider, informational): ``provider_call_at`` -> ``first_response_at`` — the
      provider's FIRST relayable output (reasoning started, the first reasoning or text delta,
      a tool/citation event, or a non-streaming reply arriving; a bare stream-open is NOT
      counted) — ``provider_wait_ms``;
    * LEG 3 (ours, after): ``first_response_at`` -> ``first_emit_at``, the first frame written
      to the client's stream after the provider responded — ``server_relay_ms``.

    Mutable and shared by reference: every task spawned from the request (the streaming
    task, a journal writer) sees the same clock, so a stamp taken anywhere lands once.
    ``latency_id`` keys the request's ledger row AND rides the marked wire frame, so the
    browser's own report joins the row whichever lands first.
    """

    arrived_perf: float
    arrived_epoch_ms: int
    latency_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    provider_call_at: float | None = None
    first_response_at: float | None = None
    first_response_kind: str | None = None
    #: The provider's transport opened (e.g. Anthropic ``message_start``) — informational only.
    #: It is NOT the first response: nothing relayable exists yet, so counting it moved the
    #: provider's own time-to-first-content into OUR relay leg (2026-10-10: relay read 230-790ms).
    stream_open_at: float | None = None
    first_emit_claimed: bool = False
    first_emit_at: float | None = None

    def _epoch(self, perf: float | None) -> datetime | None:
        if perf is None:
            return None
        ms = self.arrived_epoch_ms + (perf - self.arrived_perf) * 1000
        return datetime.fromtimestamp(ms / 1000, tz=UTC)

    @staticmethod
    def _ms(a: float | None, b: float | None) -> int | None:
        if a is None or b is None or b < a:
            return None
        return int(round((b - a) * 1000))

    @property
    def server_prep_ms(self) -> int | None:
        return self._ms(self.arrived_perf, self.provider_call_at)

    @property
    def provider_wait_ms(self) -> int | None:
        return self._ms(self.provider_call_at, self.first_response_at)

    @property
    def server_relay_ms(self) -> int | None:
        return self._ms(self.first_response_at, self.first_emit_at)

    def stamps(self) -> dict[str, object]:
        """The ledger columns this clock owns."""
        return {
            "provider_call_started_at": self._epoch(self.provider_call_at),
            "provider_first_response_at": self._epoch(self.first_response_at),
            "provider_first_response_kind": self.first_response_kind,
            "server_first_emit_at": self._epoch(self.first_emit_at),
            "server_prep_ms": self.server_prep_ms,
            "provider_wait_ms": self.provider_wait_ms,
            "server_relay_ms": self.server_relay_ms,
        }


_clock: ContextVar[RequestLatencyClock | None] = ContextVar("request_latency_clock", default=None)

#: The root field the StreamEmitter adds to the ONE frame written first after the provider
#: responded. Its value is the request's ``latency_id``; the browser stamps its receipt.
LATENCY_MARK_FIELD = "latency_mark"


def get_request_latency_clock() -> RequestLatencyClock | None:
    return _clock.get()


def arm_request_latency(*, path: str, headers: object = None) -> None:
    if not is_ai_route(path):
        return
    now_perf = time.perf_counter()
    now_ms = int(time.time() * 1000)
    _clock.set(RequestLatencyClock(arrived_perf=now_perf, arrived_epoch_ms=now_ms))
    _client_stamp.set(
        ClientLatencyStamp(
            server_arrived_at_ms=now_ms,
            client_sent_at_ms=_int_header(headers, CLIENT_SENT_AT_HEADER),
            client_prep_ms=_int_header(headers, CLIENT_PREP_MS_HEADER),
            route=unversioned_path(path),
        )
    )


def reaches_wire(emitter: object | None) -> bool:
    """Does a model call running under ``emitter`` stream to the person's response?

    THE CLOCK BELONGS TO THE TURN THE PERSON IS WAITING ON (2026-10-17). Side calls run
    inside the same request context — the new-chat title labeler, every held code-call
    mandate — under an emitter that never reaches the wire (``ConsoleEmitter``,
    ``SilentEmitter``: ``reaches_wire = False``). They used to stamp this request's
    clock: the labeler's cheap model answered before the chat model's first token, so
    LEG 2 ended on the labeler's reply and LEG 3 ran until the ``conversation_labeled``
    frame — production read a 400-700 ms "relay" on every new chat that was the
    labeler's own parse-and-save, while the real first-token relay was 30-60 ms. An
    unknown or missing emitter still counts (no worse than before)."""
    return emitter is None or getattr(emitter, "reaches_wire", True) is not False


def mark_first_provider_call(emitter: object | None = None) -> None:
    clock = _clock.get()
    if clock is None or clock.provider_call_at is not None or not reaches_wire(emitter):
        return
    clock.provider_call_at = time.perf_counter()


def mark_provider_stream_open() -> None:
    """The provider's stream opened. Recorded, never counted as its first response."""
    clock = _clock.get()
    if clock is None or clock.provider_call_at is None or clock.stream_open_at is not None:
        return
    clock.stream_open_at = time.perf_counter()


def mark_provider_first_response(kind: str, emitter: object | None = None) -> None:
    """The provider produced its first RELAYABLE output — reasoning started, a reasoning or
    text delta, a tool/citation event, or a non-streaming reply. A bare transport event
    (stream open) is ``mark_provider_stream_open``. Only the first, after the call started,
    and only from a call whose output reaches the wire (``reaches_wire``)."""
    clock = _clock.get()
    if clock is None or clock.provider_call_at is None or clock.first_response_at is not None:
        return
    if not reaches_wire(emitter):
        return
    clock.first_response_at = time.perf_counter()
    clock.first_response_kind = kind


def claim_first_emit() -> RequestLatencyClock | None:
    """Called by the stream emitter for each outbound frame: returns the clock exactly once —
    for the first frame after the provider responded — so that frame is marked and its
    write time stamped (``note_first_emit``)."""
    clock = _clock.get()
    if clock is None or clock.first_response_at is None or clock.first_emit_claimed:
        return None
    clock.first_emit_claimed = True
    return clock


def note_first_emit(clock: RequestLatencyClock) -> None:
    if clock.first_emit_at is None:
        clock.first_emit_at = time.perf_counter()


def get_time_to_first_provider_s() -> float | None:
    clock = _clock.get()
    if clock is None or clock.provider_call_at is None:
        return None
    return round(clock.provider_call_at - clock.arrived_perf, 3)


def clear_request_latency() -> None:
    _clock.set(None)
    _client_stamp.set(None)
