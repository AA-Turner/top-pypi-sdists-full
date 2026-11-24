"""THE FINAL OUTBOUND SNAPSHOT and the STATIC SEAL CHECK (report only).

Plan: ``common-docs/systems/agents/agent-harness/projects/prompt-blocks-static-seal/PLAN.md`` §5.6 (P0). Arman's words:
``VISION.md`` beside it. The static seal line is an OBSERVER: it compares the bytes that actually
left for the provider with the previous send of the same conversation, and when anything above the
line changed it REPORTS. It never fixes, blocks, restores or reorders anything.

Where it runs (the last moment before the provider):

* httpx SDKs (Anthropic, OpenAI, Groq, Cerebras, Together, generic OpenAI-compatible): the request
  event hook every provider client is built with (``outbound_capture._outbound_request_hook``),
  after the SDK serialized the body. Fidelity ``bytes``.
* Google ``genai``: the patched last pre-transport step (``request_capture.install_genai_capture``),
  on the exact bytes genai's transport sends (``json.dumps(http_request.data)``). Fidelity ``bytes``.
* xAI chat (gRPC): the request proto the stub sends (``chat._make_request``'s source, the chat's
  ``_proto``), each message serialized deterministically. Fidelity ``proto``.

What it records (``FinalOutboundSnapshot``): provider, model, conversation id, request id, loop
round, fidelity, the sha256 of the whole body, and SEGMENT fingerprints — sha256 of the canonical
bytes of ``tools``, ``system`` and each wire message above the seal (whole messages before the
seal message, then the seal message's content blocks before the boundary). Hashes and lengths only
(plus 2 KB chunk digests that locate a divergence, in process memory only): no body is ever kept.

Canonical bytes leave out what may change without touching the cached text: cache-control markers
and their TTL (``cache_control``), ``prompt_cache_key``, and stream flags (both are request fields
outside the segments).

Where the line sits (default, ruled 2026-11-12): immediately BEFORE the first per-turn platform
block (the host turn, ``typed_text_last.HOST_TURN_KEY``) of the newest person turn. When she typed
text that is after her authored template text; when nothing was typed the block opens the final
template message, so that whole message is below the line. With no per-turn block the line is
before the newest person turn. Each translator stamps the line in ITS OWN wire list
(``SealLocator``): translators merge same-role turns, insert notes and move the system text, so the
position is ``(wire message index, content-block index)``.

The line POSITION belongs to the conversation and is fixed at its ASSEMBLY send (a conversation with
no completed turn): stored as the index in the translator's rendered list, every later send — any
provider, any model — maps it to its own wire list. A conversation with no stored position that
already finished a turn (it predates the record) seals tools and system only: under-seal, never
over-seal. Baselines are keyed by (conversation, provider, model, agent): a model or provider switch
is a new baseline, never a break. Both persist across turns in
``chat.conversation.cache_state[SEAL_STATE_KEY]`` (``db/persistence._refresh_cache_state``). SIDE
runs — a system process inside the conversation it serves (the labeler), a system run, an unsaved or
confidential (``store=False``) run — never touch the conversation's position or baseline: each keeps
its own in-memory baseline for its own loop.

The check: a differing segment, while the previous send is younger than the knob
``agents.prompt_cache.seal_window_minutes`` (the provider cache is gone after it, so an older send
is not compared — silently), is ONE warning per segment per conversation per window: a WARNING log
line (``app_log`` in the host) and a compact entry in ``cache_state`` (segment, both request ids,
divergence offset). P0 files no ``system_error`` (server mode keeps today's known breakers).

The check reads ONLY this snapshot — never ``system_prompt_frozen``, ``_enforce_frozen_prompt`` or
any "unchanged" flag.

NEVER BREAKS A SEND: every entry point is wrapped; its own failure is said once per kind per process
(red console line + ERROR log) and the send proceeds. Cost: only agent-loop sends are fingerprinted;
on the event loop the hook only takes a reference to the body and queues it. The fingerprint (parse,
hash, segment, the residual check's subtraction) runs in ONE WORKER PROCESS (``seal_worker.py``):
worker THREADS stalled the event loop 160-240 ms under load (2026-11-13: full garbage collections
from ``json.loads`` and interpreter-lock contention). One dispatcher thread feeds it plain data and
compares the short hashes it returns. Above ``seal_parse_max_kb`` hashed whole, never parsed; a genai
dict above ``seal_genai_max_kb`` is skipped. The stamp is cleared with the send it belongs to.
"""

from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from collections import OrderedDict
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

#: ``chat.conversation.cache_state`` key: ``{"position": {...}, "<provider>|<model>|<agent>": record}``.
SEAL_STATE_KEY = "static_seal"

#: Wire shapes — one segment parser each.
SHAPE_ANTHROPIC = "anthropic_messages"
SHAPE_RESPONSES = "openai_responses"
SHAPE_CHAT = "chat_completions"
SHAPE_GOOGLE = "google_generate_content"
SHAPE_XAI = "xai_proto"

#: Divergence is located to a chunk of this many canonical bytes (chunk digests live in process
#: memory only; ``cache_state`` keeps one digest and the length per segment).
CHUNK_BYTES = 2048
_DIGEST_CHARS = 16
_CHUNK_DIGEST_CHARS = 8
#: Bounds on what is kept per conversation (memory and cache_state).
_MAX_CONVERSATIONS = 512
_MAX_KEYS_PER_CONVERSATION = 4
_MAX_BREAKS_KEPT = 10
#: Chunk digests kept per segment, from BOTH ends (chunk grid from the segment's start): the first
#: ``_HEAD_CHUNKS`` and the last ``_TAIL_CHUNKS``. Bounds the memory one huge segment holds in
#: ``_LATEST`` while a head edit and a tail edit (an append) are still located to within a chunk; a
#: middle edit is located "between" the known-equal ends. ``cache_state`` keeps fewer of each.
_HEAD_CHUNKS = 64
_TAIL_CHUNKS = 64
_PERSISTED_HEAD_CHUNKS = 8
_PERSISTED_TAIL_CHUNKS = 8

FEATURE = "agents.prompt_cache"
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_window_minutes".
SEAL_WINDOW_MINUTES_MIRROR = 60
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_parse_max_kb".
SEAL_PARSE_MAX_KB_MIRROR = 1024
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_pending_max".
SEAL_PENDING_MAX_MIRROR = 32
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_pending_max_mb".
SEAL_PENDING_MAX_MB_MIRROR = 64
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_check_on" (0 = off, 1 = on).
#: Off until the fingerprint work leaves this process: an independent load probe (2026-11-13)
#: measured event-loop stalls of 160-240 ms from garbage collection and interpreter-lock
#: contention while worker threads parsed large bodies. A real request is never slowed for a saving.
SEAL_CHECK_ON_MIRROR = 0
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_genai_max_kb": a genai body
#: (a dict; sending it to the worker process walks every node) above this is skipped, said once.
SEAL_GENAI_MAX_KB_MIRROR = 64
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_worker_restart_minutes": after
#: the worker process dies, at most one restart per this many minutes (jobs are dropped meanwhile).
SEAL_WORKER_RESTART_MINUTES_MIRROR = 10
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "seal_worker_timeout_seconds": a job
#: the worker has not answered by then kills the worker (it counts as dead).
SEAL_WORKER_TIMEOUT_SECONDS_MIRROR = 30
#: The reserved entry of ``cache_state[SEAL_STATE_KEY]`` holding the conversation's line position.
POSITION_KEY = "position"
#: Key prefix of a side run's records (a system process, an unsaved run): process memory only.
_SIDE_PREFIX = "side:"


def seal_window_seconds() -> float:
    from matrx_ai.knobs import package_knob_number

    minutes = package_knob_number(FEATURE, "seal_window_minutes", SEAL_WINDOW_MINUTES_MIRROR, low=1, high=1440)
    return float(minutes) * 60.0


def seal_parse_max_bytes() -> int:
    from matrx_ai.knobs import package_knob_number

    kb = package_knob_number(FEATURE, "seal_parse_max_kb", SEAL_PARSE_MAX_KB_MIRROR, low=64, high=65536)
    return int(kb) * 1024


def seal_check_on() -> bool:
    """Whether background fingerprinting runs at all. Any doubt (a knob read that fails) is off."""
    try:
        from matrx_ai.knobs import package_knob_number

        return int(package_knob_number(FEATURE, "seal_check_on", SEAL_CHECK_ON_MIRROR, low=0, high=1)) == 1
    except Exception:  # noqa: BLE001 — the observer never breaks a send; off is the safe answer
        return False


def seal_genai_max_bytes() -> int:
    from matrx_ai.knobs import package_knob_number

    kb = package_knob_number(FEATURE, "seal_genai_max_kb", SEAL_GENAI_MAX_KB_MIRROR, low=1, high=65536)
    return int(kb) * 1024


def seal_worker_restart_seconds() -> float:
    from matrx_ai.knobs import package_knob_number

    minutes = package_knob_number(
        FEATURE, "seal_worker_restart_minutes", SEAL_WORKER_RESTART_MINUTES_MIRROR, low=1, high=1440
    )
    return float(minutes) * 60.0


def seal_worker_timeout_seconds() -> float:
    from matrx_ai.knobs import package_knob_number

    return float(
        package_knob_number(FEATURE, "seal_worker_timeout_seconds", SEAL_WORKER_TIMEOUT_SECONDS_MIRROR, low=1, high=600)
    )


def seal_pending_max() -> int:
    """Most background fingerprints in flight; past it a job is dropped (said once), never queued."""
    from matrx_ai.knobs import package_knob_number

    return int(package_knob_number(FEATURE, "seal_pending_max", SEAL_PENDING_MAX_MIRROR, low=1, high=1024))


def seal_pending_max_bytes() -> int:
    """Most body bytes held by background fingerprints in flight; past it a job is dropped (said
    once), never queued — the count cap alone let 32 large bodies sit in memory."""
    from matrx_ai.knobs import package_knob_number

    mb = package_knob_number(FEATURE, "seal_pending_max_mb", SEAL_PENDING_MAX_MB_MIRROR, low=1, high=4096)
    return int(mb) * 1024 * 1024


# ---------------------------------------------------------------------------
# Who is sending: the run's identity, and side runs
# ---------------------------------------------------------------------------


def _app_context() -> Any:
    try:
        from matrx_connect.context.app_context import try_get_app_context

        return try_get_app_context()
    except Exception:  # noqa: BLE001
        return None


def is_side_run(ctx: Any) -> bool:
    """A send that is not a turn of the person's conversation run: a system process inside the
    conversation it serves (the labeler), a system run, or an unsaved (``store=False``) run. Side
    runs never touch the conversation's baseline or its line position."""
    if ctx is None:
        return False
    if getattr(ctx, "system_run", False) or getattr(ctx, "store", True) is False:
        return True
    metadata = getattr(ctx, "metadata", None)
    if isinstance(metadata, dict):
        from matrx_ai.agents.conversation_type import SYSTEM_PROCESS_KEY

        if metadata.get(SYSTEM_PROCESS_KEY):
            return True
    return False


def _in_agent_loop() -> bool:
    try:
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        return try_get_execution_state() is not None
    except Exception:  # noqa: BLE001
        return False


def _loop_identity() -> str:
    try:
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        return str(id(try_get_execution_state()))
    except Exception:  # noqa: BLE001
        return "?"


# ---------------------------------------------------------------------------
# The seal stamp — each translator marks the line in its own wire list
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SealStamp:
    """Where the static seal line sits in ONE send's wire message list.

    ``message_index``: wire messages before it are wholly above the line. ``block_index``: when not
    None, that many leading content blocks of message ``message_index`` are above it too.
    ``position``: the same line in the translator's rendered (provider-neutral) list — the index of
    its first message below the line, the form stored per conversation. ``under_sealed``: no stored
    position and not an assembly send (a chat that predates the record): only tools and system are
    sealed. ``side``: the send of a side run (``is_side_run``).
    """

    shape: str
    message_index: int
    block_index: int | None = None
    position: int | None = None
    under_sealed: bool = False
    side: bool = False
    #: ``(message index, blocks)`` the previous send of this baseline sealed INSIDE a message. When
    #: this send seals that message whole (its turn row was merged since: B8), the same leading
    #: blocks are fingerprinted under the previous label too, so an unchanged head is never a break.
    previous_head: tuple[int, int] | None = None


_stamp_var: ContextVar[SealStamp | None] = ContextVar("matrx_ai_static_seal_stamp", default=None)


def stamp_seal(stamp: SealStamp | None) -> None:
    _stamp_var.set(stamp)


def current_seal_stamp() -> SealStamp | None:
    return _stamp_var.get()


def default_seal_position(messages: list[Any]) -> int | None:
    """Index (in the list a translator renders) of the first message BELOW the default line.

    The first per-turn platform block (host turn) of the newest person turn; without one, the
    newest person turn itself; ``None`` when neither exists (a send with no person turn)."""
    from matrx_ai.config.typed_text_last import HOST_TURN_KEY, turn_person_index

    for index, message in enumerate(messages):
        metadata = getattr(message, "metadata", None)
        if isinstance(metadata, dict) and metadata.get(HOST_TURN_KEY):
            return index
    return turn_person_index(messages)


#: Conversations whose row (and so ``cache_state``) could not be read this process: never "new".
_ROW_UNKNOWN: OrderedDict[str, None] = OrderedDict()


def note_conversation_row_read(conversation_id: str | None, *, known: bool) -> None:
    """The resolver's word on whether the conversation's ``cache_state`` was read (a missing row
    counts as read: a new conversation). Never raises."""
    try:
        if not conversation_id:
            return
        with _LOCK:
            if known:
                _ROW_UNKNOWN.pop(str(conversation_id), None)
            else:
                _ROW_UNKNOWN[str(conversation_id)] = None
                while len(_ROW_UNKNOWN) > _MAX_CONVERSATIONS:
                    _ROW_UNKNOWN.popitem(last=False)
    except Exception:  # noqa: BLE001
        pass


def _row_unknown(conversation_id: str) -> bool:
    with _LOCK:
        return str(conversation_id) in _ROW_UNKNOWN


def _only_authored_before(messages: list[Any], position: int) -> bool:
    """Every message above the line is the agent's authored template (``cache_template`` stamp) or
    the authored head of the newest person turn. A fork or import seeded with copied history has
    earlier person turns there: not an assembly send."""
    from matrx_ai.config.cache_marks import TEMPLATE_METADATA_KEY

    for message in messages[:position]:
        metadata = getattr(message, "metadata", None)
        if not (isinstance(metadata, dict) and metadata.get(TEMPLATE_METADATA_KEY)):
            return False
    return True


def _had_a_completed_turn(conversation_id: str) -> bool:
    """Whether the conversation finished a turn before this one: its persisted ``cache_state``
    (read at resolve) records a response. A brand-new conversation has none — its first send is
    the assembly send. (Template messages may hold model turns, so roles cannot tell.)"""
    from matrx_ai.config.cache_state_reader import persisted_cache_state

    return bool(persisted_cache_state(conversation_id).get("last_response_at"))


def _content_len(wire_message: Any) -> int | None:
    if isinstance(wire_message, dict):
        for key in ("content", "parts"):
            value = wire_message.get(key)
            if isinstance(value, list):
                return len(value)
        return None
    content = getattr(wire_message, "content", None)
    try:
        return len(content) if content is not None and not isinstance(content, str | bytes) else None
    except TypeError:
        return None


def _target_for(messages: list[Any]) -> tuple[int | None, bool, bool]:
    """(the rendered-list index of the first message below the line, under-sealed, side run).

    The line POSITION belongs to the conversation, fixed at its assembly send: a later send — any
    provider, any model — reuses the stored position. With none stored: the assembly send (a
    conversation with no completed turn) uses the default position; a later send (a chat that
    predates the record), a conversation whose row could not be read, or one seeded with copied
    history (a fork, an import: earlier person turns above the line) seals tools and system only,
    and stores no position — under-seal, never over-seal."""
    ctx = _app_context()
    side = is_side_run(ctx)
    default = default_seal_position(messages)
    if side:
        return default, False, True
    conversation_id = getattr(ctx, "conversation_id", None) if ctx is not None else None
    stored = conversation_position(conversation_id) if conversation_id else None
    if stored is not None:
        return int(stored.get("index") or 0), bool(stored.get("under_sealed")), False
    if (
        default is None
        or (conversation_id and _row_unknown(str(conversation_id)))
        or (conversation_id and _had_a_completed_turn(str(conversation_id)))
        or not _only_authored_before(messages, default)
    ):
        return 0, True, False
    return default, False, False


class SealLocator:
    """Stamps the line in a translator's own wire list, whatever it merges or splits.

    Call ``before(position, wire)`` at the top of every iteration over ``messages`` (the list the
    translator renders, in order) and ``finish(wire)`` after the loop. The locator watches what the
    target message did to the wire list — appended new message(s), or merged into the last one —
    and stamps ``(message index, block index)`` accordingly. Never raises.
    """

    __slots__ = ("_last_len", "_n_before", "_resolved", "shape", "side", "target", "under_sealed")

    def __init__(self, shape: str, messages: list[Any]) -> None:
        self.shape = shape
        self._resolved = False
        self._n_before: int | None = None
        self._last_len: int | None = None
        self.under_sealed = False
        self.side = False
        stamp_seal(None)
        try:
            self.target, self.under_sealed, self.side = _target_for(list(messages))
        except Exception as exc:  # noqa: BLE001 — a locator never breaks a translation
            self.target = None
            _say_failure("seal locator", exc)

    def _stamp(self, message_index: int, block_index: int | None) -> None:
        stamp_seal(
            SealStamp(
                self.shape,
                message_index,
                block_index,
                position=self.target,
                under_sealed=self.under_sealed,
                side=self.side,
            )
        )

    def before(self, position: int, wire: list[Any]) -> None:
        try:
            if self._resolved or self.target is None:
                return
            if position == self.target:
                self._n_before = len(wire)
                self._last_len = _content_len(wire[-1]) if wire else None
            elif self._n_before is not None:
                self._resolve(wire)
        except Exception:  # noqa: BLE001
            self._resolved = True

    def finish(self, wire: list[Any]) -> None:
        try:
            if self._resolved or self.target is None:
                return
            if self._n_before is None:
                # The target lies past the rendered list (a shorter history): the line is at its end.
                self._resolved = True
                self._stamp(len(wire), None)
                return
            self._resolve(wire)
        except Exception:  # noqa: BLE001
            self._resolved = True

    def _resolve(self, wire: list[Any]) -> None:
        n = int(self._n_before or 0)
        self._resolved = True
        if len(wire) > n or n == 0:
            self._stamp(n, None)
            return
        now_len = _content_len(wire[n - 1])
        if self._last_len is not None and now_len is not None and now_len > self._last_len:
            self._stamp(n - 1, self._last_len)  # merged into the last message
        elif self._last_len is None and now_len is None:
            self._stamp(n - 1, None)  # merged into a string: the whole message is below
        else:
            self._stamp(n, None)


# ---------------------------------------------------------------------------
# Canonical bytes and segment parsers (one per wire shape)
# ---------------------------------------------------------------------------

#: Keys never fingerprinted wherever they appear inside a segment.
_EXCLUDED_KEYS = frozenset({"cache_control", "prompt_cache_key", "stream", "stream_options"})


def _canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _canonical(v) for k, v in value.items() if k not in _EXCLUDED_KEYS}
    if isinstance(value, list):
        return [_canonical(v) for v in value]
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), default=str).encode(
        "utf-8", "replace"
    )


@dataclass(frozen=True, slots=True)
class Segment:
    label: str
    sha: str
    length: int
    #: Digests of the first chunks (indices 0..len-1 of the ``CHUNK_BYTES`` grid).
    chunks: tuple[str, ...]
    #: Digests of the last chunks of the same grid (the final ``len(tail)`` indices).
    tail: tuple[str, ...] = ()

    def chunk_map(self) -> dict[int, str]:
        """Grid index -> digest for every chunk this segment kept."""
        out = dict(enumerate(self.chunks))
        total = -(-self.length // CHUNK_BYTES)
        start = total - len(self.tail)
        for offset, digest in enumerate(self.tail):
            if start + offset >= len(self.chunks):
                out[start + offset] = digest
        return out

    def as_list(self, *, with_chunks: bool = True) -> list[Any]:
        """The stored form ``[label, sha, length, head digests, tail digests]``. Process memory keeps
        up to ``_HEAD_CHUNKS`` + ``_TAIL_CHUNKS``; ``cache_state`` (it reaches the browser every
        turn) keeps ``_PERSISTED_HEAD_CHUNKS`` + ``_PERSISTED_TAIL_CHUNKS``."""
        if with_chunks:
            return [self.label, self.sha, self.length, list(self.chunks), list(self.tail)]
        head = list(self.chunks[:_PERSISTED_HEAD_CHUNKS])
        total = -(-self.length // CHUNK_BYTES)
        kept = self.chunk_map()
        first_tail = max(len(head), total - _PERSISTED_TAIL_CHUNKS)
        tail = [kept.get(i) for i in range(first_tail, total)]
        if any(d is None for d in tail):
            tail = []
        return [self.label, self.sha, self.length, head, tail]

    @classmethod
    def from_list(cls, raw: Any) -> Segment | None:
        if not (isinstance(raw, list | tuple) and len(raw) in (3, 4, 5)):
            return None
        label, sha, length = raw[0], raw[1], raw[2]
        chunks = raw[3] if len(raw) >= 4 else ()
        tail = raw[4] if len(raw) == 5 else ()
        if not (
            isinstance(label, str)
            and isinstance(sha, str)
            and isinstance(chunks, list | tuple)
            and isinstance(tail, list | tuple)
        ):
            return None
        return cls(label, sha, int(length or 0), tuple(str(c) for c in chunks), tuple(str(c) for c in tail))


def _chunk_digest(raw: bytes, index: int) -> str:
    return hashlib.sha256(raw[index * CHUNK_BYTES : (index + 1) * CHUNK_BYTES]).hexdigest()[:_CHUNK_DIGEST_CHARS]


def segment_of(label: str, raw: bytes) -> Segment:
    total = -(-len(raw) // CHUNK_BYTES)
    head_n = min(total, _HEAD_CHUNKS)
    tail_start = max(head_n, total - _TAIL_CHUNKS)
    return Segment(
        label,
        hashlib.sha256(raw).hexdigest()[:_DIGEST_CHARS * 2],
        len(raw),
        tuple(_chunk_digest(raw, i) for i in range(head_n)),
        tuple(_chunk_digest(raw, i) for i in range(tail_start, total)),
    )


def _message_segments(
    messages: list[Any], seal: SealStamp, *, content_key: str, to_bytes: Any = canonical_bytes
) -> list[Segment]:
    out: list[Segment] = []
    upto = min(max(seal.message_index, 0), len(messages))
    for index in range(upto):
        out.append(segment_of(f"message {index}", to_bytes(messages[index])))
    heads = []
    if seal.block_index and seal.message_index < len(messages):
        heads.append((seal.message_index, seal.block_index))
    if seal.previous_head is not None:
        index, blocks = seal.previous_head
        if 0 <= index < upto and blocks and (index, blocks) not in heads:
            heads.append((index, blocks))
    for index, blocks in heads:
        message = messages[index]
        content = message.get(content_key) if isinstance(message, dict) else None
        if isinstance(content, list):
            head = {k: v for k, v in message.items() if k != content_key}
            head[content_key] = content[:blocks]
            out.append(segment_of(f"message {index} blocks 0..{blocks - 1}", to_bytes(head)))
    return out


def segments_anthropic(body: dict[str, Any], seal: SealStamp) -> list[Segment]:
    out: list[Segment] = []
    if "tools" in body:
        out.append(segment_of("tools", canonical_bytes(body.get("tools"))))
    if "system" in body:
        out.append(segment_of("system", canonical_bytes(body.get("system"))))
    out.extend(_message_segments(list(body.get("messages") or []), seal, content_key="content"))
    return out


def segments_responses(body: dict[str, Any], seal: SealStamp) -> list[Segment]:
    out: list[Segment] = []
    if "tools" in body:
        out.append(segment_of("tools", canonical_bytes(body.get("tools"))))
    if "instructions" in body:
        out.append(segment_of("system", canonical_bytes(body.get("instructions"))))
    items = body.get("input")
    if isinstance(items, str):
        items = [items]
    out.extend(_message_segments(list(items or []), seal, content_key="content"))
    return out


def segments_chat(body: dict[str, Any], seal: SealStamp) -> list[Segment]:
    out: list[Segment] = []
    if "tools" in body:
        out.append(segment_of("tools", canonical_bytes(body.get("tools"))))
    out.extend(_message_segments(list(body.get("messages") or []), seal, content_key="content"))
    return out


def segments_google(body: dict[str, Any], seal: SealStamp) -> list[Segment]:
    out: list[Segment] = []
    if "tools" in body:
        out.append(segment_of("tools", canonical_bytes(body.get("tools"))))
    for key in ("systemInstruction", "system_instruction"):
        if key in body:
            out.append(segment_of("system", canonical_bytes(body.get(key))))
            break
    out.extend(_message_segments(list(body.get("contents") or []), seal, content_key="parts"))
    return out


def _proto_bytes(message: Any) -> bytes:
    return message.SerializeToString(deterministic=True)


def _proto_size(message: Any) -> int:
    try:
        return int(message.ByteSize())
    except Exception:  # noqa: BLE001 — not a proto (a test double): size unknown, never skipped
        return 0


def segments_xai(request_proto: Any, seal: SealStamp, *, max_bytes: int | None = None) -> list[Segment]:
    """xAI ``GetCompletionsRequest``: tools, then each message (system rides as a message). A
    segment above ``max_bytes`` (``seal_parse_max_bytes``) is skipped, never serialized."""
    out: list[Segment] = []
    tools = list(getattr(request_proto, "tools", None) or [])
    if tools and not (max_bytes and sum(_proto_size(t) for t in tools) > max_bytes):
        out.append(segment_of("tools", b"".join(_proto_bytes(t) for t in tools)))
    messages = list(getattr(request_proto, "messages", None) or [])
    upto = min(max(seal.message_index, 0), len(messages))
    for index in range(upto):
        if max_bytes and _proto_size(messages[index]) > max_bytes:
            continue
        out.append(segment_of(f"message {index}", _proto_bytes(messages[index])))
    heads = []
    if seal.block_index and seal.message_index < len(messages):
        heads.append((seal.message_index, seal.block_index))
    if seal.previous_head is not None:
        index, blocks = seal.previous_head
        if 0 <= index < upto and blocks and (index, blocks) not in heads:
            heads.append((index, blocks))
    for index, blocks in heads:
        message = messages[index]
        if max_bytes and _proto_size(message) > max_bytes:
            continue
        content = list(getattr(message, "content", None) or [])[:blocks]
        raw = str(getattr(message, "role", "")).encode() + b"".join(_proto_bytes(c) for c in content)
        out.append(segment_of(f"message {index} blocks 0..{blocks - 1}", raw))
    return out


_PARSERS = {
    SHAPE_ANTHROPIC: segments_anthropic,
    SHAPE_RESPONSES: segments_responses,
    SHAPE_CHAT: segments_chat,
    SHAPE_GOOGLE: segments_google,
}


def shape_of_url(url: str) -> str | None:
    """The chat wire shape a URL is a send of, or None (files, images, batches, counts…)."""
    path = str(url).split("?", 1)[0].rstrip("/")
    if path.endswith("/messages"):
        return SHAPE_ANTHROPIC
    if path.endswith("/responses"):
        return SHAPE_RESPONSES
    if path.endswith("/chat/completions"):
        return SHAPE_CHAT
    if path.endswith(":generateContent") or path.endswith(":streamGenerateContent"):
        return SHAPE_GOOGLE
    return None


# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FinalOutboundSnapshot:
    provider: str
    model: str
    conversation_id: str | None
    request_id: str | None
    loop_round: int | None
    fidelity: str
    body_sha256: str
    body_bytes: int
    seal: SealStamp | None
    segments: tuple[Segment, ...] = ()
    parsed: bool = True
    agent_id: str | None = None
    #: The loop that sent it (a side run's baseline is its own loop's).
    loop: str = "?"
    at: float = field(default_factory=time.time)


_last_snapshot_var: ContextVar[FinalOutboundSnapshot | None] = ContextVar(
    "matrx_ai_final_outbound_snapshot", default=None
)


def last_final_outbound_snapshot() -> FinalOutboundSnapshot | None:
    """The final outbound snapshot of this task's most recent inline chat send (readers: P7)."""
    return _last_snapshot_var.get()


# ---------------------------------------------------------------------------
# Memory: per conversation, the line position and the latest record per run identity
# ---------------------------------------------------------------------------

_LOCK = threading.Lock()
#: One check at a time (sends checked inline and in worker threads).
_CHECK_LOCK = threading.Lock()
#: conversation -> {key: record}. Records here keep chunk digests; the persisted form drops them.
_LATEST: OrderedDict[str, dict[str, dict[str, Any]]] = OrderedDict()
#: conversation -> its line position ``{"index", "under_sealed", "at"}`` (fixed at assembly).
_POSITIONS: OrderedDict[str, dict[str, Any]] = OrderedDict()
#: conversation -> keys (and ``POSITION_KEY``) changed since persistence last took them.
_DIRTY: OrderedDict[str, set[str]] = OrderedDict()


def _key(provider: str, model: str, agent_id: str | None) -> str:
    return f"{provider}|{model}|{agent_id or '-'}"


def _baseline_key(provider: str, model: str, agent_id: str | None, *, side: bool, loop: str) -> str:
    key = _key(provider, model, agent_id)
    return f"{_SIDE_PREFIX}{loop}|{key}" if side else key


def _with_previous_head(stamp: SealStamp, conversation_id: str | None, key: str) -> SealStamp:
    """``stamp`` carrying the previous send's in-message seal (see ``SealStamp.previous_head``)."""
    if not conversation_id:
        return stamp
    previous = _previous(conversation_id, key) or {}
    raw = previous.get("seal")
    if isinstance(raw, list | tuple) and len(raw) == 2 and isinstance(raw[0], int) and isinstance(raw[1], int):
        return SealStamp(
            stamp.shape,
            stamp.message_index,
            stamp.block_index,
            position=stamp.position,
            under_sealed=stamp.under_sealed,
            side=stamp.side,
            previous_head=(raw[0], raw[1]),
        )
    return stamp


def _persisted_seal_state(conversation_id: str) -> dict[str, Any]:
    """The conversation's persisted ``cache_state[SEAL_STATE_KEY]`` (read once at resolve)."""
    from matrx_ai.config.cache_state_reader import persisted_cache_state

    seal_state = persisted_cache_state(conversation_id).get(SEAL_STATE_KEY)
    return seal_state if isinstance(seal_state, dict) else {}


def conversation_position(conversation_id: str | None) -> dict[str, Any] | None:
    """The conversation's line position, from this process or its persisted ``cache_state``."""
    if not conversation_id:
        return None
    with _LOCK:
        mine = _POSITIONS.get(str(conversation_id))
    if mine is not None:
        return dict(mine)
    persisted = _persisted_seal_state(str(conversation_id)).get(POSITION_KEY)
    if isinstance(persisted, dict) and isinstance(persisted.get("index"), int):
        return dict(persisted)
    return None


def _remember_position(conversation_id: str, stamp: SealStamp, at: float) -> None:
    if stamp.side or stamp.position is None or stamp.under_sealed:
        return
    with _LOCK:
        if str(conversation_id) in _POSITIONS:
            return
        _POSITIONS[str(conversation_id)] = {"index": stamp.position, "under_sealed": stamp.under_sealed, "at": at}
        while len(_POSITIONS) > _MAX_CONVERSATIONS:
            _POSITIONS.popitem(last=False)
        _DIRTY.setdefault(str(conversation_id), set()).add(POSITION_KEY)


def _previous(conversation_id: str, key: str) -> dict[str, Any] | None:
    with _LOCK:
        mine = (_LATEST.get(conversation_id) or {}).get(key)
    persisted = None if key.startswith(_SIDE_PREFIX) else _persisted_seal_state(conversation_id).get(key)
    persisted = persisted if isinstance(persisted, dict) else None
    if mine is None:
        return {**persisted, "_source": "cache_state"} if persisted else None
    if persisted and float(persisted.get("at") or 0) > float(mine.get("at") or 0):
        return {**persisted, "_source": "cache_state"}
    return {**mine, "_source": "this process"}


def _store(conversation_id: str, key: str, record: dict[str, Any]) -> None:
    with _LOCK:
        entries = _LATEST.setdefault(conversation_id, {})
        entries[key] = record
        if len(entries) > _MAX_KEYS_PER_CONVERSATION:
            oldest = sorted(entries, key=lambda k: float(entries[k].get("at") or 0))
            for gone in oldest[: len(entries) - _MAX_KEYS_PER_CONVERSATION]:
                entries.pop(gone, None)
        _LATEST.move_to_end(conversation_id)
        while len(_LATEST) > _MAX_CONVERSATIONS:
            gone_conversation, _ = _LATEST.popitem(last=False)
            _DIRTY.pop(gone_conversation, None)
        if not key.startswith(_SIDE_PREFIX):
            _DIRTY.setdefault(conversation_id, set()).add(key)
            _DIRTY.move_to_end(conversation_id)


def _persisted_form(record: dict[str, Any]) -> dict[str, Any]:
    out = dict(record)
    out["segments"] = [
        s.as_list(with_chunks=False) for s in (Segment.from_list(r) for r in record.get("segments") or []) if s
    ]
    return out


def take_seal_records(conversation_id: str | None) -> dict[str, Any] | None:
    """What changed for ``conversation_id`` since the last take, in its persisted form (no chunk
    digests, no side runs): read by ``db/persistence._refresh_cache_state`` (pattern:
    ``send_boundary.take_context_breakdown``)."""
    if not conversation_id:
        return None
    with _LOCK:
        keys = _DIRTY.pop(str(conversation_id), None)
        entries = dict(_LATEST.get(str(conversation_id)) or {})
        position = _POSITIONS.get(str(conversation_id))
    if not keys:
        return None
    out: dict[str, Any] = {k: _persisted_form(entries[k]) for k in keys if k in entries}
    if POSITION_KEY in keys and position is not None:
        out[POSITION_KEY] = dict(position)
    return out


def merged_seal_state(existing: Any, taken: dict[str, Any] | None) -> dict[str, Any] | None:
    """``cache_state[SEAL_STATE_KEY]`` after folding in ``taken``: the stored position never moves
    once written; newest record wins per key; at most ``_MAX_KEYS_PER_CONVERSATION`` record keys."""
    base = dict(existing) if isinstance(existing, dict) else {}
    if not taken:
        return base or None
    for key, record in taken.items():
        if key == POSITION_KEY:
            if not isinstance(base.get(POSITION_KEY), dict):
                base[POSITION_KEY] = record
            continue
        old = base.get(key)
        if isinstance(old, dict) and float(old.get("at") or 0) > float(record.get("at") or 0):
            continue
        base[key] = record
    records = {k: v for k, v in base.items() if k != POSITION_KEY}
    if len(records) > _MAX_KEYS_PER_CONVERSATION:
        keep = sorted(records.items(), key=lambda kv: float((kv[1] or {}).get("at") or 0), reverse=True)
        position = base.get(POSITION_KEY)
        base = dict(keep[:_MAX_KEYS_PER_CONVERSATION])
        if position is not None:
            base[POSITION_KEY] = position
    return base


def reset_for_tests() -> None:
    with _LOCK:
        _LATEST.clear()
        _POSITIONS.clear()
        _DIRTY.clear()
        _ROW_UNKNOWN.clear()
    _PENDING.clear()
    _PENDING_BYTES[0] = 0
    _FAILED.clear()
    _SKIPPED.clear()
    _WORKER_DOWN_AT[0] = None  # the worker process itself is kept: it holds no state
    stamp_seal(None)
    from matrx_ai.providers import residual_check

    residual_check.reset_for_tests()
    _last_snapshot_var.set(None)


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------


def _divergence(prev: Segment, new: Segment) -> tuple[int, int] | None:
    """``(low, high)``: the two segments are known equal before byte ``low`` and the first
    difference is at or before byte ``high`` (``low == high``: located exactly, to ``CHUNK_BYTES``).
    Compares the chunk digests both kept (head and tail of the same grid). None when neither kept
    any (an old stored baseline)."""
    a, b = prev.chunk_map(), new.chunk_map()
    if not a or not b:
        return None
    low = 0
    for index in sorted(set(a) & set(b)):
        if a[index] == b[index]:
            if index * CHUNK_BYTES == low:
                low = (index + 1) * CHUNK_BYTES
            continue
        return low, index * CHUNK_BYTES
    shorter = min(prev.length, new.length)
    if low >= shorter:
        return shorter, shorter
    # Every chunk both kept is equal: the change lies in the middle neither kept.
    later = [i * CHUNK_BYTES for i in set(a) & set(b) if i * CHUNK_BYTES > low]
    return low, (min(later) if later else max(prev.length, new.length))


def _divergence_offset(prev: Segment, new: Segment) -> int | None:
    """Where the two segments first differ, to ``CHUNK_BYTES``, when that is known exactly."""
    found = _divergence(prev, new)
    return found[0] if found is not None and found[0] == found[1] else None


def _report_break(
    *,
    snapshot: FinalOutboundSnapshot,
    baseline: str,
    segment: str,
    previous_request_id: str | None,
    divergence_offset: int | None,
    previous_length: int,
    current_length: int,
    divergence_range: list[int] | None = None,
) -> None:
    logger.warning(
        "static_seal_broken: segment %r above the static seal line changed between sends "
        "(conversation %s, agent %s, provider %s, model %s, previous request %s, this request %s, "
        "provider call %s of this turn, baseline from %s, first difference %s (to %s bytes), "
        "length %s -> %s)",
        segment,
        snapshot.conversation_id,
        snapshot.agent_id,
        snapshot.provider,
        snapshot.model,
        previous_request_id,
        snapshot.request_id,
        "?" if snapshot.loop_round is None else snapshot.loop_round,
        baseline,
        (
            f"at byte {divergence_offset}"
            if divergence_offset is not None
            else (f"between byte {divergence_range[0]} and {divergence_range[1]}" if divergence_range else "unknown")
        ),
        CHUNK_BYTES,
        previous_length,
        current_length,
        extra={"kind": "static_seal_broken", "conversation_id": snapshot.conversation_id, "segment": segment},
    )


def check_and_remember(snapshot: FinalOutboundSnapshot, *, raw_segments: list[list[Any]] | None = None) -> list[str]:
    """Compare ``snapshot`` with the previous send of its run identity in its conversation, report
    each newly broken segment once per window, and remember ``snapshot``. Returns the labels
    reported (tests read it). ``raw_segments``: the snapshot's segments in their stored list form
    (``Segment.as_list``) as the worker process returned them — compared and stored as they are,
    with no ``Segment`` built per row (the check runs on a server thread: fewer objects, less
    garbage collection)."""
    conversation_id = snapshot.conversation_id
    seal = snapshot.seal
    if not conversation_id or seal is None:
        return []
    key = _baseline_key(snapshot.provider, snapshot.model, snapshot.agent_id, side=seal.side, loop=snapshot.loop)
    # Worker threads finish out of order: the read, the compare and the store are one step, and a
    # send older than the stored one is neither compared nor stored (it never overwrites a newer one).
    # The event-loop thread never WAITS for that step (a worker may hold it over a large body): when
    # it is busy this send's check is skipped (said once). Reports are logged after the lock is
    # released, so a slow log handler never holds a send.
    if _on_event_loop_thread():
        if not _CHECK_LOCK.acquire(blocking=False):
            _say_failure("seal check busy on the event loop (a check was skipped)", BlockingIOError())
            return []
    else:
        _CHECK_LOCK.acquire()
    try:
        reported, reports = _check_locked(snapshot, conversation_id, seal, key, raw_segments)
    finally:
        _CHECK_LOCK.release()
    for report in reports:
        _report_break(snapshot=snapshot, **report)
    return reported


def _on_event_loop_thread() -> bool:
    import asyncio

    return asyncio._get_running_loop() is not None


def _check_locked(
    snapshot: FinalOutboundSnapshot,
    conversation_id: str,
    seal: SealStamp,
    key: str,
    raw_segments: list[list[Any]] | None = None,
) -> tuple[list[str], list[dict[str, Any]]]:
    previous = _previous(conversation_id, key)
    now = snapshot.at
    reports: list[dict[str, Any]] = []
    if previous is not None and float(previous.get("at") or 0) > now:
        return [], reports
    window = seal_window_seconds()
    reported: list[str] = []
    breaks: list[dict[str, Any]] = list((previous or {}).get("breaks") or [])[-_MAX_BREAKS_KEPT:]
    reported_at: dict[str, float] = {
        str(k): float(v) for k, v in dict((previous or {}).get("reported") or {}).items() if isinstance(v, int | float)
    }
    breaks_total = int((previous or {}).get("breaks_total") or 0)
    #: True only when this send was checked against a previous fingerprint inside the window (the
    #: screen never calls a segment stable that nothing was compared with).
    compared = False
    if previous is not None and snapshot.parsed and previous.get("parsed", True):
        age = now - float(previous.get("at") or 0)
        if 0 <= age <= window:
            compared = True
            # Stored segments are compared by their short hash first; only a differing one is
            # rebuilt (a Segment per stored row cost most of the check: it runs per send).
            new: dict[str, Any] = (
                {s.label: s for s in snapshot.segments} if raw_segments is None else {r[0]: r for r in raw_segments}
            )
            for raw in previous.get("segments") or []:
                if not (isinstance(raw, list | tuple) and len(raw) >= 3 and isinstance(raw[0], str)):
                    continue
                cur = new.get(raw[0])
                if cur is not None and not isinstance(cur, Segment):
                    if cur[1] == raw[1]:
                        continue
                    cur = Segment.from_list(cur)
                if cur is not None and cur.sha == raw[1]:
                    continue
                prev_seg = Segment.from_list(raw)
                if prev_seg is None:
                    continue
                label = prev_seg.label
                last = reported_at.get(label)
                if last is not None and now - last <= window:
                    continue
                if " blocks " in label and label.split(" blocks ", 1)[0] in reported:
                    continue  # the whole message is already reported: one change, one report
                found = _divergence(prev_seg, cur) if cur is not None else (0, 0)
                offset = found[0] if found is not None and found[0] == found[1] else None
                span = list(found) if found is not None and found[0] != found[1] else None
                reports.append(
                    {
                        "baseline": str(previous.get("_source") or "?"),
                        "segment": label,
                        "previous_request_id": previous.get("request_id"),
                        "divergence_offset": offset,
                        "divergence_range": span,
                        "previous_length": prev_seg.length,
                        "current_length": cur.length if cur is not None else 0,
                    }
                )
                reported_at[label] = now
                breaks_total += 1
                breaks.append(
                    {
                        "segment": label,
                        "at": now,
                        "previous_request_id": previous.get("request_id"),
                        "request_id": snapshot.request_id,
                        "loop_round": snapshot.loop_round,
                        "divergence_offset": offset,
                        **({"divergence_range": span} if span else {}),
                    }
                )
                reported.append(label)
    record = {
        "at": now,
        "request_id": snapshot.request_id,
        "loop_round": snapshot.loop_round,
        "fidelity": snapshot.fidelity,
        "body_sha256": snapshot.body_sha256,
        "parsed": snapshot.parsed,
        "seal": [seal.message_index, seal.block_index],
        "segments": [s.as_list() for s in snapshot.segments] if raw_segments is None else raw_segments,
        "reported": {k: v for k, v in reported_at.items() if now - v <= window},
        "breaks": breaks[-_MAX_BREAKS_KEPT:],
        "breaks_total": breaks_total,
        "compared": compared,
    }
    _store(conversation_id, key, record)
    _remember_position(conversation_id, seal, now)
    return reported, reports


# ---------------------------------------------------------------------------
# Entry points — the last moment before the provider. Never raise.
# ---------------------------------------------------------------------------

_FAILED: set[str] = set()
#: Background fingerprints in flight (every send made while an event loop runs): the loop-side
#: future of each job, with the body bytes it holds. Read and written on event-loop threads only.
_PENDING: dict[Any, int] = {}
#: Total body bytes held by ``_PENDING`` (one cell: read and written on the event-loop thread).
_PENDING_BYTES: list[int] = [0]


#: Set once atexit shutdown begins: a job cut off by the exit is not a failure worth reporting.
_SHUTTING_DOWN: list[bool] = [False]


def _say_failure(where: str, exc: BaseException) -> None:
    import sys

    if _SHUTTING_DOWN[0] or sys.is_finalizing():
        return
    mark = f"{where}:{type(exc).__name__}"
    if mark in _FAILED:
        return
    _FAILED.add(mark)
    try:
        from matrx_utils import vcprint

        vcprint(
            f"[final_outbound_snapshot] {where} failed (the send proceeds; said once per process): "
            f"{type(exc).__name__}: {exc}",
            color="red",
        )
    except Exception:  # noqa: BLE001
        pass
    logger.error("final outbound snapshot %s failed (the send proceeds): %r", where, exc)


_SKIPPED: set[str] = set()


def _say_skip(where: str, detail: str) -> None:
    """An EXPECTED skip (a body above a knob's size): announced once per process at WARNING, as a
    skip, never as a failure — it is the designed behaviour, files no error row and no ERROR line."""
    import sys

    if _SHUTTING_DOWN[0] or sys.is_finalizing() or where in _SKIPPED:
        return
    _SKIPPED.add(where)
    logger.warning("final outbound snapshot skipped: %s (%s; the send proceeds; said once per process)", where, detail)


@dataclass(frozen=True, slots=True)
class _Identity:
    provider: str
    model: str
    conversation_id: str | None
    request_id: str | None
    iteration: int | None
    agent_id: str | None
    loop: str


def _send_identity() -> _Identity:
    from matrx_ai.providers.outbound_capture import get_call_meta

    meta = get_call_meta()
    ctx = _app_context()
    return _Identity(
        provider=str(getattr(meta, "provider", None) or "unknown"),
        model=str(getattr(meta, "model", None) or ""),
        conversation_id=(getattr(ctx, "conversation_id", None) or None) if ctx is not None else None,
        request_id=(getattr(ctx, "request_id", None) or None) if ctx is not None else None,
        iteration=getattr(meta, "iteration", None),
        agent_id=(getattr(ctx, "agent_id", None) or None) if ctx is not None else None,
        loop=_loop_identity(),
    )


def _approx_json_size(value: Any, limit: int) -> int:
    """About how many bytes ``json.dumps(value)`` would make, walked without building them (a
    multi-MB base64 string costs ``len``, never a copy); stops counting once past ``limit``."""
    total = 0
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, str | bytes):
            total += len(item) + 2
        elif isinstance(item, dict):
            total += 2
            for key, member in item.items():
                total += len(str(key)) + 4
                stack.append(member)
        elif isinstance(item, list | tuple):
            total += 2 + len(item)
            stack.extend(item)
        else:
            total += 8
        if total > limit:
            return total
    return total


# ---------------------------------------------------------------------------
# The fingerprint — PURE functions of plain data (they run in the worker process)
# ---------------------------------------------------------------------------


def body_fingerprint(
    shape: str, body: bytes | None, body_obj: Any, stamp: SealStamp, parse_max: int
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """``(parts, parsed body)`` of one chat body. Touches no module state.

    ``body`` (httpx) is hashed whole and parsed only up to ``parse_max``. ``body_obj`` (genai: the
    dict its transport serializes) is never serialized whole: only the segments above the line are,
    and only when the body is (about) within the parse limit; it carries no whole-body hash.
    ``parts``: ``fidelity``, ``body_sha256``, ``body_bytes``, ``parsed``, ``segments`` (stored
    lists, ``Segment.as_list``), or ``{"skip": True}`` when the parsed body is not an object."""
    obj: Any = None
    if body is None:
        obj = body_obj if isinstance(body_obj, dict) else {}
        body_bytes = _approx_json_size(obj, parse_max)
        parsed = body_bytes <= parse_max
        body_sha = ""
        fidelity = "segments"
    else:
        body_bytes = len(body)
        parsed = body_bytes <= parse_max
        body_sha = hashlib.sha256(body).hexdigest()
        fidelity = "bytes"
        if parsed:
            obj = body_obj if isinstance(body_obj, dict) else (json.loads(body) if body else {})
    segments: list[list[Any]] = []
    if parsed:
        if not isinstance(obj, dict):
            return {"skip": True}, None
        segments = [s.as_list() for s in _PARSERS[shape](obj, stamp)]
    parts = {
        "fidelity": fidelity,
        "body_sha256": body_sha,
        "body_bytes": body_bytes,
        "parsed": parsed,
        "segments": segments,
    }
    return parts, (obj if parsed else None)


def xai_fingerprint(
    whole: bytes, proto_ref: tuple[str, str] | None, stamp: SealStamp, parse_max: int, request_proto: Any = None
) -> dict[str, Any]:
    """Parts of one xAI request from its serialized bytes. ``request_proto`` (inline) is read as is;
    otherwise ``proto_ref`` (module, class name) names the class the bytes are re-read into — the
    worker process imports the SDK's proto module, never the server. Above ``parse_max`` the request
    is hashed whole, never parsed; a segment above it is skipped."""
    parsed = len(whole) <= parse_max
    if parsed and request_proto is None and proto_ref is not None:
        import importlib

        module, name = proto_ref
        request_proto = getattr(importlib.import_module(module), name).FromString(whole)
    return {
        "fidelity": "proto",
        "body_sha256": hashlib.sha256(whole).hexdigest(),
        "body_bytes": len(whole),
        "parsed": parsed,
        "segments": [s.as_list() for s in segments_xai(request_proto, stamp, max_bytes=parse_max)] if parsed else [],
    }


def worker_job(job: dict[str, Any]) -> dict[str, Any]:
    """The worker process's ONE entry: a job dict of plain data in, plain data out. Never reads or
    writes module state (the parent compares and remembers)."""
    import os

    stamp: SealStamp = job["stamp"]
    if job["kind"] == "xai":
        parts = xai_fingerprint(job["whole"], job["proto_ref"], stamp, job["parse_max"])
    else:
        parts, obj = body_fingerprint(job["shape"], job.get("body"), job.get("body_obj"), stamp, job["parse_max"])
        known = job.get("known")
        if known is not None and obj is not None:
            try:
                from matrx_ai.providers.residual_check import residual_of

                parts["residual"] = residual_of(job["shape"], obj, known, patterns=job.get("patterns") or {})
            except Exception as exc:  # noqa: BLE001 — the residual never costs the fingerprint
                parts["residual_error"] = f"{type(exc).__name__}: {exc}"
    parts["pid"] = os.getpid()
    return parts


def _snapshot_of(who: _Identity, stamp: SealStamp, parts: dict[str, Any], at: float) -> FinalOutboundSnapshot:
    return FinalOutboundSnapshot(
        provider=who.provider,
        model=who.model,
        conversation_id=who.conversation_id,
        request_id=who.request_id,
        loop_round=who.iteration,
        fidelity=str(parts["fidelity"]),
        body_sha256=str(parts["body_sha256"]),
        body_bytes=int(parts["body_bytes"]),
        seal=stamp,
        # The worker built these lists (``Segment.as_list``): rebuilt without re-validating each digest.
        segments=tuple(Segment(r[0], r[1], r[2], tuple(r[3]), tuple(r[4])) for r in parts["segments"]),
        parsed=bool(parts["parsed"]),
        agent_id=who.agent_id,
        loop=who.loop,
        at=at,
    )


def _stamp_for(who: _Identity, stamp: SealStamp) -> SealStamp:
    return _with_previous_head(
        stamp,
        who.conversation_id,
        _baseline_key(who.provider, who.model, who.agent_id, side=stamp.side, loop=who.loop),
    )


# ---------------------------------------------------------------------------
# Inline (no running event loop: a sync script, a test) — the server never takes this path
# ---------------------------------------------------------------------------


def _fingerprint(
    who: _Identity, stamp: SealStamp, shape: str, body: bytes | None, body_obj: Any, at: float
) -> FinalOutboundSnapshot | None:
    """Hash and segment one body in this process, then run the check (no running loop only)."""
    stamp = _stamp_for(who, stamp)
    parts, _ = body_fingerprint(shape, body, body_obj, stamp, seal_parse_max_bytes())
    if parts.get("skip"):
        return None
    snapshot = _snapshot_of(who, stamp, parts, at)
    check_and_remember(snapshot)
    return snapshot


def _fingerprint_safely(*args: Any) -> FinalOutboundSnapshot | None:
    try:
        return _fingerprint(*args)
    except Exception as exc:  # noqa: BLE001 — the observer never breaks a send
        _say_failure("wire body", exc)
        return None


def _fingerprint_xai(
    who: _Identity, stamp: SealStamp, request_proto: Any, whole: bytes | None, proto_cls: Any, at: float
) -> FinalOutboundSnapshot | None:
    """Hash and segment one xAI request in this process (no running loop only)."""
    if whole is None:
        whole = request_proto.SerializeToString(deterministic=True)
    stamp = _stamp_for(who, stamp)
    parts = xai_fingerprint(whole, None, stamp, seal_parse_max_bytes(), request_proto=request_proto)
    snapshot = _snapshot_of(who, stamp, parts, at)
    check_and_remember(snapshot)
    return snapshot


def _fingerprint_xai_safely(*args: Any) -> FinalOutboundSnapshot | None:
    try:
        return _fingerprint_xai(*args)
    except Exception as exc:  # noqa: BLE001 — the observer never breaks a send
        _say_failure("xai proto", exc)
        return None


_PROTO_REFS: dict[Any, tuple[str, str] | None] = {}


def _proto_ref(proto_cls: Any) -> tuple[str, str] | None:
    """``(importable module, class name)`` of a generated proto class (its ``__module__`` names the
    proto package, not always an importable module: the loaded ``*_pb2`` module holding it is found
    once, off the loop, and remembered)."""
    if proto_cls in _PROTO_REFS:
        return _PROTO_REFS[proto_cls]
    import sys

    name = getattr(proto_cls, "__name__", None)
    found: tuple[str, str] | None = None
    if name:
        module = getattr(proto_cls, "__module__", None)
        if module and getattr(sys.modules.get(module), name, None) is proto_cls:
            found = (str(module), str(name))
        else:
            for mod_name, mod in list(sys.modules.items()):
                if mod_name.endswith("_pb2") and getattr(mod, name, None) is proto_cls:
                    found = (mod_name, str(name))
                    break
    _PROTO_REFS[proto_cls] = found
    return found


# ---------------------------------------------------------------------------
# Off the loop: ONE dispatcher thread feeds ONE worker process
# ---------------------------------------------------------------------------
#
# On the event loop a send only builds a ``_SealJob`` (references, no copy) and puts it on a queue.
# The dispatcher thread (a server thread, never the loop) takes one job at a time: reads the previous
# send's in-message seal, the parse limit and the residual check's known texts, sends plain data to
# the worker process, and on its answer compares the short hashes (``check_and_remember``) and reports.
# Jobs run strictly in order, so a send's previous-head lookup always sees the send before it.


@dataclass(slots=True)
class _SealJob:
    kind: str  # "body" | "xai"
    who: _Identity
    stamp: SealStamp
    shape: str
    at: float
    body: bytes | None = None
    body_obj: Any = None
    whole: bytes | None = None
    proto_cls: Any = None
    residual_source: tuple[Any, Any] | None = None


_JOBS: Any = None
_DISPATCHER: Any = None
_DISPATCHER_GUARD = threading.Lock()
#: The worker process (``seal_worker.WorkerProcess``) or None; touched by the dispatcher thread only.
_WORKER: Any = None
#: ``time.monotonic()`` when the worker last died (or failed to start); None while healthy.
_WORKER_DOWN_AT: list[float | None] = [None]
#: How many worker processes were started this process (the first start is not a restart).
_WORKER_STARTS: list[int] = [0]
#: ``time.monotonic()`` when the current/last worker process was started; None before the first start.
#: The restart throttle measures from THIS (the last restart), never from when a death was noticed.
_WORKER_STARTED_AT: list[float | None] = [None]


def _ensure_dispatcher() -> Any:
    """The job queue, with its dispatcher thread running (started once; a thread start, ~0.1 ms)."""
    global _JOBS, _DISPATCHER
    if _DISPATCHER is not None and _DISPATCHER.is_alive():
        return _JOBS
    with _DISPATCHER_GUARD:
        if _DISPATCHER is None or not _DISPATCHER.is_alive():
            import queue

            _JOBS = queue.SimpleQueue()
            _DISPATCHER = threading.Thread(target=_dispatch_forever, args=(_JOBS,), name="static-seal-dispatch", daemon=True)
            _DISPATCHER.start()
    return _JOBS


def _dispatch_forever(jobs: Any) -> None:
    while True:
        item = jobs.get()
        if item is None:
            return
        job, loop, future = item
        try:
            _run_job(job)
        except BaseException as exc:  # noqa: BLE001 — the dispatcher never dies of a job
            _say_failure("seal dispatcher", exc)
        finally:
            _resolve(loop, future)


def _resolve(loop: Any, future: Any) -> None:
    try:
        loop.call_soon_threadsafe(_finish_future, future)
    except RuntimeError:
        pass  # the loop is closed: nothing awaits it


def _finish_future(future: Any) -> None:
    if not future.done():
        future.set_result(None)


def _run_job(job: _SealJob) -> None:
    """One job, on the dispatcher thread: prepare plain data, run it in the worker, compare."""
    who = job.who
    parse_max = seal_parse_max_bytes()
    stamp = _stamp_for(who, job.stamp)
    payload: dict[str, Any] = {"kind": job.kind, "stamp": stamp, "parse_max": parse_max, "shape": job.shape}
    if job.kind == "xai":
        payload["whole"] = job.whole
        payload["proto_ref"] = _proto_ref(job.proto_cls)
    elif job.body is not None:
        payload["body"] = job.body
    else:
        limit = seal_genai_max_bytes()
        if _approx_json_size(job.body_obj, limit) > limit:
            _say_skip("genai body above seal_genai_max_kb (a fingerprint was skipped)", f"more than {limit} bytes")
            return
        payload["body_obj"] = job.body_obj
    if job.residual_source is not None:
        known = _residual_known(job.residual_source)
        if known is not None:
            payload["known"], payload["patterns"] = known
    result = _run_in_worker(payload)
    if not isinstance(result, dict):
        return
    if "error" in result:
        _say_failure("seal worker job", RuntimeError(str(result["error"])))
        return
    if result.get("skip"):
        return
    raw = result["segments"]
    check_and_remember(_snapshot_of(who, stamp, {**result, "segments": ()}, job.at), raw_segments=raw)
    if result.get("residual_error"):
        _say_failure("residual check", RuntimeError(str(result["residual_error"])))
    if result.get("residual"):
        _report_residual(who, result["residual"])


def _residual_known(source: tuple[Any, Any]) -> tuple[list[str], dict[str, Any]] | None:
    try:
        from matrx_ai.providers.residual_check import known_texts, platform_patterns

        return known_texts(source), platform_patterns()
    except Exception as exc:  # noqa: BLE001
        _say_failure("residual check", exc)
        return None


def _report_residual(who: _Identity, residual: list[Any]) -> None:
    try:
        from matrx_ai.providers.residual_check import report_residual

        report_residual(
            [tuple(item) for item in residual],
            conversation_id=who.conversation_id,
            request_id=who.request_id,
            provider=who.provider,
            model=who.model,
        )
    except Exception as exc:  # noqa: BLE001 — the observer never breaks a send
        _say_failure("residual check", exc)


def _residual_source() -> tuple[Any, Any] | None:
    """What the translator rendered for this send (taken: it belongs to this send), when the residual
    check's knob is on. A ContextVar read and a knob read: no walk of the source on the loop."""
    try:
        from matrx_ai.providers.residual_check import residual_check_enabled, take_wire_source

        source = take_wire_source()
        return source if source is not None and residual_check_enabled() else None
    except Exception as exc:  # noqa: BLE001
        _say_failure("residual check", exc)
        return None


def _run_in_worker(payload: dict[str, Any]) -> Any:
    """Run one job in the worker process; None when there is no worker (said once). Starts the worker
    when needed; after it dies, at most one restart per ``seal_worker_restart_minutes`` — never a loop."""
    global _WORKER
    from matrx_ai.providers.seal_worker import WorkerGone, WorkerProcess

    if _WORKER is None or not _WORKER.alive():
        if _WORKER is not None:
            _worker_down(WorkerGone(f"worker exited (code {_WORKER.proc.poll()})"))
        down = _WORKER_DOWN_AT[0]
        if down is not None and time.monotonic() - down < seal_worker_restart_seconds():
            _say_failure("seal worker down (fingerprints are skipped until its next restart)", WorkerGone())
            return None
        try:
            _WORKER = WorkerProcess()
            _WORKER_STARTS[0] += 1
            _WORKER_STARTED_AT[0] = time.monotonic()
            _WORKER_DOWN_AT[0] = None
        except Exception as exc:  # noqa: BLE001
            _WORKER = None
            _WORKER_DOWN_AT[0] = time.monotonic()
            _say_failure("seal worker start", exc)
            return None
    try:
        return _WORKER.call(payload, timeout=seal_worker_timeout_seconds())
    except WorkerGone as exc:
        _worker_down(exc)
        return None


def _after_fork_in_child() -> None:
    """A forked child holds the parent's worker handle, dispatcher thread object and pending jobs —
    none of them works there. It starts clean: its first job starts its own dispatcher and worker."""
    global _WORKER, _DISPATCHER, _JOBS, _LOCK, _CHECK_LOCK, _DISPATCHER_GUARD
    # Locks held by another thread at fork time stay held forever in the child: make fresh ones.
    _LOCK = threading.Lock()
    _CHECK_LOCK = threading.Lock()
    _DISPATCHER_GUARD = threading.Lock()
    _SHUTTING_DOWN[0] = False
    _WORKER = None
    _DISPATCHER = None
    _JOBS = None
    _WORKER_DOWN_AT[0] = None
    _WORKER_STARTED_AT[0] = None
    _PENDING.clear()
    _PENDING_BYTES[0] = 0


def _close_worker_at_exit() -> None:
    """Stop and reap the worker when the server exits (no zombie, no orphan)."""
    _SHUTTING_DOWN[0] = True
    worker = _WORKER
    if worker is not None:
        worker.close()


def _install_process_hooks() -> None:
    import atexit
    import os

    atexit.register(_close_worker_at_exit)
    if hasattr(os, "register_at_fork"):
        os.register_at_fork(after_in_child=_after_fork_in_child)


_install_process_hooks()


def _worker_down(exc: BaseException) -> None:
    global _WORKER
    worker, _WORKER = _WORKER, None
    # Throttle from the last restart (when the dead worker started), not from now: a worker that
    # died long ago restarts at once; a crash loop is still held to one restart per window.
    started = _WORKER_STARTED_AT[0] if worker is not None else None
    _WORKER_DOWN_AT[0] = started if started is not None else time.monotonic()
    if worker is not None:
        worker.close()
    _say_failure("seal worker", exc)


def _off_loop(job: _SealJob, *, cost: int = 0) -> bool:
    """Hand ``job`` to the dispatcher (worker process), off the send's path. False when no loop
    runs. ``cost``: the body bytes the job holds until it ends."""
    import asyncio

    if not seal_check_on():
        # Switched off: the job is skipped (True = handled), never run inline.
        return True
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return False
    _prune_pending()
    if len(_PENDING) >= seal_pending_max() or _PENDING_BYTES[0] + max(cost, 0) > seal_pending_max_bytes():
        # Backpressure: the send never waits for a fingerprint; this one is skipped, said once.
        _say_failure(
            "background queue full (a fingerprint was skipped)",
            OverflowError(f"{len(_PENDING)} jobs, {_PENDING_BYTES[0]} bytes"),
        )
        return True
    try:
        jobs = _ensure_dispatcher()
    except Exception as exc:  # noqa: BLE001 — no dispatcher: skipped, said once
        _say_failure("background dispatcher unavailable (a fingerprint was skipped)", exc)
        return True
    future = loop.create_future()
    _PENDING[future] = max(cost, 0)
    _PENDING_BYTES[0] += max(cost, 0)
    future.add_done_callback(_release_pending)
    jobs.put((job, loop, future))
    return True


def _release_pending(future: Any) -> None:
    cost = _PENDING.pop(future, None)
    if cost:
        _PENDING_BYTES[0] = max(0, _PENDING_BYTES[0] - cost)


async def wait_for_pending() -> None:
    """Await background fingerprints of this loop, compared and remembered (tests; graceful shutdown)."""
    import asyncio

    loop = asyncio.get_running_loop()
    while True:
        _prune_pending()
        mine = [f for f in list(_PENDING) if f.get_loop() is loop]
        if not mine:
            return
        await asyncio.gather(*mine, return_exceptions=True)


def _prune_pending() -> None:
    """Drop finished jobs (and jobs of a loop that is gone) so they never hold a slot."""
    for future in list(_PENDING):
        if future.done() or future.get_loop().is_closed():
            _release_pending(future)


def _genai_cost(body_obj: Any) -> int:
    """About how many bytes a genai body dict holds, from its message parts' strings only (a few
    hundred ``len`` calls; never a walk of every node): the pending cap's charge for the job, and
    the loop-side test against ``seal_genai_max_kb``."""
    total = 0
    try:
        for content in body_obj.get("contents") or ():
            for part in content.get("parts") or () if isinstance(content, dict) else ():
                if isinstance(part, dict):
                    text = part.get("text")
                    if isinstance(text, str):
                        total += len(text)
                    inline = part.get("inlineData") or part.get("inline_data")
                    if isinstance(inline, dict) and isinstance(inline.get("data"), str | bytes):
                        total += len(inline["data"])
    except Exception:  # noqa: BLE001 — an estimate only
        return total
    return total


def observe_wire_body(
    *, url: str, body: bytes | None = None, body_obj: Any = None, always_off_loop: bool = False
) -> FinalOutboundSnapshot | None:
    """Fingerprint one serialized chat send and run the seal check.

    ``body`` is the exact bytes (httpx hook: immutable); ``body_obj`` is the dict genai's transport
    serializes. Only agent-loop sends are fingerprinted. ON THE EVENT LOOP NOTHING IS PARSED, HASHED
    OR COMPARED: the hook takes a reference to the body plus the stamp and the send's identity and
    queues them for the worker process (``_off_loop``; past its job or byte cap the job is dropped,
    said once), and returns at once. A genai body above ``seal_genai_max_kb`` is skipped (said once):
    sending a big dict to another process is a walk of every node. Only a caller with no running
    loop (a sync script, a test) is fingerprinted inline, and gets the snapshot back. The stamp is
    cleared: it belongs to this send only. (``always_off_loop`` is kept for callers.)"""
    try:
        stamp = _stamp_var.get()
        if stamp is None:
            return None
        if not seal_check_on():
            return None  # switched off: nothing parsed, hashed or queued
        shape = shape_of_url(url)
        if shape is None or shape != stamp.shape:
            return None  # a non-chat call on the same client (files, images, counts): never parsed
        stamp_seal(None)
        if not _in_agent_loop():
            return None
        who = _send_identity()
        if not who.conversation_id:
            return None
        at = time.time()
        if body is not None:
            cost = len(body)
        else:
            cost = _genai_cost(body_obj) if isinstance(body_obj, dict) else 0
            if cost > seal_genai_max_bytes():
                _say_skip("genai body above seal_genai_max_kb (a fingerprint was skipped)", f"about {cost} bytes")
                return None
        # The residual check rides the worker job only; the no-loop inline path never runs it.
        job = _SealJob("body", who, stamp, shape, at, body=body, body_obj=body_obj, residual_source=_residual_source())
        if _off_loop(job, cost=cost):
            return None
        snapshot = _fingerprint_safely(who, stamp, shape, body, body_obj, at)
        if snapshot is not None:
            _last_snapshot_var.set(snapshot)
        return snapshot
    except Exception as exc:  # noqa: BLE001 — the observer never breaks a send
        _say_failure("wire body", exc)
        return None


def observe_xai_request(chat: Any) -> FinalOutboundSnapshot | None:
    """Fingerprint an xAI chat send from the request proto the stub sends (``chat._proto``).

    On the event loop the request is only serialized (a C copy: the proto is mutable, the bytes
    are not) and queued; the worker process re-reads, hashes and segments it, so the SDK's proto
    module loads there. Inline only with no running loop."""
    try:
        stamp = _stamp_var.get()
        stamp_seal(None)
        if stamp is None or stamp.shape != SHAPE_XAI or not _in_agent_loop():
            return None
        if not seal_check_on():
            return None
        request_proto = getattr(chat, "_proto", None)
        if request_proto is None:
            return None
        who = _send_identity()
        if not who.conversation_id:
            return None
        at = time.time()
        # One serialization (a C copy, ~0.3 ms for 2 MB — cheaper than ``ByteSize``) decides the path.
        whole = request_proto.SerializeToString(deterministic=True)
        job = _SealJob("xai", who, stamp, SHAPE_XAI, at, whole=whole, proto_cls=type(request_proto))
        if _off_loop(job, cost=len(whole)):
            return None
        snapshot = _fingerprint_xai_safely(who, stamp, request_proto, whole, type(request_proto), at)
        if snapshot is not None:
            _last_snapshot_var.set(snapshot)
        return snapshot
    except Exception as exc:  # noqa: BLE001
        _say_failure("xai proto", exc)
        return None


__all__ = [
    "CHUNK_BYTES",
    "FinalOutboundSnapshot",
    "POSITION_KEY",
    "SEAL_STATE_KEY",
    "SHAPE_ANTHROPIC",
    "SHAPE_CHAT",
    "SHAPE_GOOGLE",
    "SHAPE_RESPONSES",
    "SHAPE_XAI",
    "SealLocator",
    "SealStamp",
    "Segment",
    "canonical_bytes",
    "body_fingerprint",
    "check_and_remember",
    "conversation_position",
    "current_seal_stamp",
    "default_seal_position",
    "is_side_run",
    "last_final_outbound_snapshot",
    "merged_seal_state",
    "observe_wire_body",
    "observe_xai_request",
    "reset_for_tests",
    "seal_genai_max_bytes",
    "seal_pending_max_bytes",
    "seal_window_seconds",
    "segments_anthropic",
    "segments_chat",
    "segments_google",
    "segments_responses",
    "segments_xai",
    "shape_of_url",
    "stamp_seal",
    "take_seal_records",
    "wait_for_pending",
    "worker_job",
    "xai_fingerprint",
]
