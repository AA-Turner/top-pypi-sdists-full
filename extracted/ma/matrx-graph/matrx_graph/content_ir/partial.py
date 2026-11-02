"""Streaming partial kinds — the live-rendering contract, engine half.

THE CONTRACT (Arman, 2026-08-20 — plan of record:
``common-docs/systems/architecture/content-ir/FEATURE.md`` §7.6; wire
contract of record: ``common-docs/systems/architecture/content-ir/FEATURE.md``):

    "upon recognition of a potential block, the system starts outputting a kind
    that has a key that clearly defines that it's not done streaming it yet and
    that it's only sort of like a pre-recognition, but then Python needs to
    actually close the JSON so that it's a valid JSON that it's sending. And
    then the front end recognizes that, sees that it's a partial JSON and knows
    that it may end up being something different, but it renders it as each
    chunk of the stream comes in. And then if it ends up that the object is
    accurate, the final closing removes the partial and whatever else and sends
    the final through. Whereas if it turns out that we were wrong in the
    detection and it's not that kind, then the system needs sort of an escape
    hatch."

THREE EVENTS, ONE CHANNEL, ONE KEY
----------------------------------
Everything rides ``metadata`` on the events the platform ALREADY streams
(``render_block`` for chat and server-orchestrated agent runs, the node event
frame for workflows) at the reserved key ``__ir_partial``. No new event type,
no second transport, one streaming law for chat and workflows.

``state`` is a CLOSED union and is the machine-checkable marker — never
inferred, never a heuristic, never "no ``__ir`` means partial":

* ``partial``    — repeatable. A provisional kind instance whose ``root.value``
                   is VALID, CLOSED JSON built from everything received so far.
                   ``root.kindState`` is ``speculative`` (pre-recognition: the
                   kind is a detection guess) and ``root.status`` is
                   ``streaming``. It MAY still become something else.
* ``superseded`` — TERMINAL. The block completed AS the provisional kind. The
                   verified ``__ir`` envelope on the SAME event is the truth;
                   the client drops the partial and renders the final.
* ``retracted``  — TERMINAL, the escape hatch. Detection was wrong: the region
                   is not that kind (``became_kind`` names what it actually is,
                   or ``None`` when it resolved to no kind at all).
                   ``reason`` says why. Never a silent swap.

**Every partial ends in exactly one terminal event.** A producer that emits a
``partial`` for a block MUST emit ``superseded`` or ``retracted`` for it — the
loud-failure posture, because a partial that never terminates is a stuck
skeleton in the UI and the user can never tell a live render from a dead one.
``PartialKindTracker`` below exists so a producer cannot forget.

WHY A SEPARATE KEY AND NOT ``__ir``
-----------------------------------
Law 1 of both envelope producers is COMPLETE-ONLY: a premature ``__ir`` is
seeded into the frontend's fingerprint-keyed envelope cache
(``sanitizeInboundEnvelopeMetadata`` → ``seedEnvelope``) and poisons every
later read of that region. That law is not weakened here — it is honored
literally. A partial NEVER touches ``__ir``, so
``classifyInboundEnvelopeMetadata`` sees "absent" and passes through untouched;
the partial channel is opt-in and can poison nothing. It is also why a partial
is never mistaken for a verified pass: an ``__ir`` envelope means "validated
against the registered schema", and a partial is by definition unvalidated.

WHY THE VALUE IS CLOSED JSON AND NOT A RAW TRUNCATED STRING
-----------------------------------------------------------
Arman's requirement, and it is the whole difference between progressive
rendering and a spinner: the client must be able to ``JSON.parse`` every
partial and render the fields that have arrived. ``close_partial_json`` below
truncates at the last position where the document can be closed cleanly and
appends the closers — so a half-written object is a smaller VALID object, never
a parse error the client has to guess at.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any, Literal

from matrx_graph.content_ir.envelope import IR_ENGINE, IR_VERSION, KIND_KEY
from matrx_graph.content_ir.fingerprint import fingerprint_text

__all__ = [
    "IR_PARTIAL_KEY",
    "PARTIAL_STATES",
    "PartialState",
    "close_partial_json",
    "partial_kind_event",
    "superseded_event",
    "retracted_event",
    "read_partial_event",
    "PartialKindTracker",
]

#: The reserved metadata key carrying every event of this contract. Distinct
#: from ``__ir`` by design — see the module docstring.
IR_PARTIAL_KEY = "__ir_partial"

PartialState = Literal["partial", "superseded", "retracted"]

#: The closed union, exported so consumers validate rather than string-match.
PARTIAL_STATES: frozenset[str] = frozenset({"partial", "superseded", "retracted"})

#: Notice codes carried on ``root.residue.notices`` of a ``partial`` event.
NOTICE_TRUNCATED = "partial_truncated"
NOTICE_UNVALIDATED = "partial_unvalidated"


# ---------------------------------------------------------------------------
# The JSON closer — "Python needs to actually close the JSON"
# ---------------------------------------------------------------------------


class _Frame:
    __slots__ = ("kind", "state", "has_members")

    def __init__(self, kind: str) -> None:
        self.kind = kind  # "obj" | "arr"
        # obj: key | colon | value | comma      arr: value | comma
        self.state = "key" if kind == "obj" else "value"
        self.has_members = False


def close_partial_json(text: str, *, include_open_string: bool = True) -> str | None:
    """Close a truncated JSON document into a VALID, smaller one.

    Returns the closed JSON text, or ``None`` when the input cannot be made
    valid (not JSON at all, or nothing usable has arrived yet). ``None`` is the
    loud posture: no partial is emitted rather than an unparseable one.

    The rule is truncate-then-close, never invent: the scanner records the last
    position at which the document could be closed cleanly — after a complete
    value, or inside a still-empty container — and everything after that
    position (a half-written key, a dangling ``:``, a trailing ``,``, a
    fragment of a number) is DROPPED. Nothing is guessed and no placeholder
    value is fabricated, so the result is always a strict subset of what the
    producer actually sent.

    ``include_open_string`` (the default) makes ONE exception, and it is the
    exception that makes progressive rendering worth having: a string VALUE
    still being typed is emitted as the text received so far, closed. A user
    watching a long answer stream sees it fill in character by character
    instead of watching the whole field blink into existence at the end. The
    tail may still grow, which is exactly what the ``partial`` state and the
    ``partial_truncated`` notice tell the client. An unterminated KEY is never
    included — a key with no value cannot be rendered and would only invent a
    field name that may not survive.

    A number at the end of the buffer is always dropped: ``1`` may still become
    ``12``, and a wrong number renders as confidently as a right one. The three
    JSON keywords cannot extend, so a complete ``true`` / ``false`` / ``null``
    at the buffer edge is kept.

    A document that is already complete and valid comes back unchanged.
    """
    if not text:
        return None

    stack: list[_Frame] = []
    # (index_after, depth, suffix) of the last position where closing is legal.
    # ``suffix`` closes an included open string before the container closers.
    safe_at: int | None = None
    safe_depth: int = 0
    safe_suffix: str = ""
    root_done = False

    i = 0
    n = len(text)
    while i < n:
        ch = text[i]

        if ch in " \t\r\n":
            i += 1
            continue

        if ch == '"':
            # Scan the whole string literal; an unterminated one is dropped by
            # falling out of the loop without moving ``safe_at``.
            j = i + 1
            closed = False
            while j < n:
                cj = text[j]
                if cj == "\\":
                    j += 2
                    continue
                if cj == '"':
                    closed = True
                    break
                j += 1
            if not closed:
                if not include_open_string:
                    break
                at_value_position = (stack and stack[-1].state == "value") or (
                    not stack and not root_done
                )
                if not at_value_position:
                    break  # an unterminated KEY is never rendered
                cut = _open_string_cut(text, i + 1)
                if cut is None:
                    break
                safe_at, safe_depth, safe_suffix = cut, len(stack), '"'
                break
            i = j + 1
            if stack:
                frame = stack[-1]
                if frame.kind == "obj":
                    if frame.state == "key":
                        frame.state = "colon"
                        # A key alone is NOT a safe point — the object would
                        # close to a dangling key. safe_at stays put.
                        continue
                    if frame.state == "value":
                        frame.state = "comma"
                        frame.has_members = True
                        safe_at, safe_depth, safe_suffix = i, len(stack), ""
                        continue
                    return None  # string where a delimiter belongs
                if frame.state != "value":
                    return None
                frame.state = "comma"
                frame.has_members = True
                safe_at, safe_depth, safe_suffix = i, len(stack), ""
                continue
            # Root-level string.
            root_done = True
            safe_at, safe_depth, safe_suffix = i, 0, ""
            continue

        if ch in "{[":
            if stack:
                frame = stack[-1]
                if frame.state != "value":
                    return None
            elif root_done:
                return None
            stack.append(_Frame("obj" if ch == "{" else "arr"))
            i += 1
            # A freshly opened container can be closed immediately as empty.
            safe_at, safe_depth, safe_suffix = i, len(stack), ""
            continue

        if ch in "}]":
            if not stack:
                return None
            frame = stack.pop()
            if frame.kind != ("obj" if ch == "}" else "arr"):
                return None
            i += 1
            if stack:
                parent = stack[-1]
                parent.state = "comma"
                parent.has_members = True
            else:
                root_done = True
            safe_at, safe_depth, safe_suffix = i, len(stack), ""
            continue

        if ch == ":":
            if not stack or stack[-1].kind != "obj" or stack[-1].state != "colon":
                return None
            stack[-1].state = "value"
            i += 1
            continue

        if ch == ",":
            if not stack or stack[-1].state != "comma":
                return None
            stack[-1].state = "key" if stack[-1].kind == "obj" else "value"
            i += 1
            continue

        # A primitive: number, true, false, null. It is complete only once a
        # delimiter follows — a trailing ``1`` may still become ``12``.
        j = i
        while j < n and text[j] not in ",]}  \t\r\n":
            j += 1
        literal = text[i:j]
        if j >= n:
            # At the buffer edge. A number may still grow (``1`` → ``12``), so
            # it is dropped; the three keywords cannot extend, so they are kept.
            if literal not in ("true", "false", "null"):
                break

        if not _is_complete_primitive(literal):
            return None
        i = j
        if stack:
            frame = stack[-1]
            if frame.state != "value":
                return None
            frame.state = "comma"
            frame.has_members = True
            safe_at, safe_depth, safe_suffix = i, len(stack), ""
        else:
            if root_done:
                return None
            root_done = True
            safe_at, safe_depth, safe_suffix = i, 0, ""
        continue

    if safe_at is None:
        return None

    closed = (
        text[:safe_at]
        + safe_suffix
        + "".join("}" if frame.kind == "obj" else "]" for frame in reversed(stack[:safe_depth]))
    )
    try:
        json.loads(closed)
    except ValueError:
        return None
    return closed


def _open_string_cut(text: str, start: int) -> int | None:
    """Last index at which an unterminated string literal can be cut cleanly.

    ``start`` is the index just after the opening quote. The cut never lands
    mid-escape (a trailing ``\\``) or mid-``\\uXXXX``, because closing there
    would produce text that is not valid JSON at all. Returns ``None`` when
    nothing of the string has arrived yet — an empty partial string is real
    data ("" so far), so that case returns ``start``, not ``None``; ``None`` is
    reserved for a start position past the end of the buffer.
    """
    if start > len(text):
        return None
    cut = start
    i = start
    n = len(text)
    while i < n:
        if text[i] == "\\":
            if i + 1 >= n:
                break  # lone trailing backslash — cut before it
            if text[i + 1] == "u":
                if i + 6 > n:
                    break  # truncated \uXXXX — cut before it
                i += 6
                cut = i
                continue
            i += 2
            cut = i
            continue
        i += 1
        cut = i
    return cut


def _is_complete_primitive(literal: str) -> bool:
    if literal in ("true", "false", "null"):
        return True
    try:
        json.loads(literal)
    except ValueError:
        return False
    return True


def parse_partial_json(text: str) -> Any | None:
    """``close_partial_json`` + parse. ``None`` when nothing usable arrived."""
    closed = close_partial_json(text)
    if closed is None:
        return None
    try:
        return json.loads(closed)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# The three events
# ---------------------------------------------------------------------------


def _notices(truncated: bool) -> list[dict[str, str]]:
    notices = [
        {
            "code": NOTICE_UNVALIDATED,
            "message": (
                "Provisional kind instance — NOT validated against the kind's "
                "registered schema. Required fields may be missing and the kind "
                "itself may still be retracted."
            ),
        }
    ]
    if truncated:
        notices.append(
            {
                "code": NOTICE_TRUNCATED,
                "message": "Source JSON was truncated mid-document and closed for transport.",
            }
        )
    return notices


def partial_kind_event(
    *,
    kind: str,
    value: dict[str, Any],
    seq: int,
    source_text: str,
    discriminator: dict[str, Any],
    truncated: bool = False,
) -> dict[str, Any]:
    """A provisional kind instance for a region that is still streaming.

    ``value`` must already be a plain, JSON-serializable dict (the caller
    produced it from ``parse_partial_json`` or from a streaming parser's
    growing snapshot). It is stamped with the wire discriminator so the payload
    is self-describing exactly like a finished one — a partial is a kind
    instance, not a different species of thing.

    ``seq`` is monotonic PER BLOCK and is the ordering / staleness key: a
    consumer that receives events out of order (or re-renders late) keeps the
    highest ``seq`` and ignores the rest.
    """
    # Round-2 W1: the ANNOUNCED kind wins — a streamed value that itself
    # carries __kind (a model echoing an example, or naming a different kind
    # than detection guessed) must not override the envelope's identity, or
    # one region gets two designated renderers.
    payload = {**value, KIND_KEY: kind}
    return {
        "v": IR_VERSION,
        "engine": IR_ENGINE,
        "state": "partial",
        "seq": seq,
        "fingerprint": fingerprint_text(source_text),
        "root": {
            "role": "structured",
            "kind": kind,
            # Pre-recognition: the kind is a DETECTION GUESS, and the frontend's
            # own IR vocabulary already has the word for that.
            "kindState": "speculative",
            "discriminator": discriminator,
            "path": [],
            "status": "streaming",
            "value": payload,
            "residue": {
                "extra": None,
                "optionalMissing": None,
                "notices": _notices(truncated),
            },
        },
    }


def superseded_event(*, kind: str, seq: int) -> dict[str, Any]:
    """TERMINAL: the region completed AS ``kind``; the final is authoritative.

    Rides the same event as the verified ``__ir`` envelope, so a consumer
    replaces the partial with the final in one frame and never flickers through
    an empty state. When the completed block produced NO ``__ir`` (unregistered
    kind, schema drift, loud-skip) the client still knows the partial is over
    and falls back to its own parse — which is why this event carries the
    terminal signal rather than leaving it implied by the arrival of ``__ir``.
    """
    return {
        "v": IR_VERSION,
        "engine": IR_ENGINE,
        "state": "superseded",
        "seq": seq,
        "kind": kind,
    }


def retracted_event(
    *,
    kind: str,
    seq: int,
    reason: str,
    became_kind: str | None = None,
    became_block_type: str | None = None,
) -> dict[str, Any]:
    """TERMINAL escape hatch: detection was wrong about ``kind``.

    ``became_kind`` names what the region actually is (``None`` when it
    resolved to no registered kind at all, e.g. it turned out to be prose);
    ``became_block_type`` carries the detector's final block type so a client
    can route without a second guess. A consumer can therefore always tell
    "this became something else" from "this completed" — the two never share a
    shape and neither is inferred from the absence of the other.
    """
    return {
        "v": IR_VERSION,
        "engine": IR_ENGINE,
        "state": "retracted",
        "seq": seq,
        "kind": kind,
        "reason": reason,
        "becameKind": became_kind,
        "becameBlockType": became_block_type,
    }


def _is_seq(value: Any) -> bool:
    """A wire ``seq``: a finite number that is not a bool.

    ``isinstance(True, int)`` is True in Python, so the naive check accepted
    ``seq: true`` — an event the TS twin rejects outright. Floats are accepted
    for the same reason the TS reader accepts them (``typeof === "number"``):
    the two readers must agree on the SAME event, and a reader that is stricter
    than its twin is a divergence in the other direction.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value == value and value not in (float("inf"), float("-inf"))
    return False


def _read_discriminator(value: Any) -> dict[str, Any] | None:
    """Twin of TS ``readDiscriminator`` — the three legal shapes, nothing else."""
    if not isinstance(value, dict):
        return None
    fmt = value.get("format")
    if fmt == "json" and value.get("key") == KIND_KEY:
        return value
    if fmt == "xml" and isinstance(value.get("tag"), str):
        return value
    if fmt == "fence" and isinstance(value.get("language"), str):
        return value
    return None


def _is_path(value: Any) -> bool:
    """Twin of TS ``readPath`` — a list of string / int segments."""
    if not isinstance(value, list):
        return False
    return all(
        isinstance(segment, str) or (isinstance(segment, int) and not isinstance(segment, bool))
        for segment in value
    )


_RESIDUE_INVALID = object()


def _read_residue(value: Any) -> Any:
    """Twin of TS ``readResidue``. ``_RESIDUE_INVALID`` = reject the event."""
    if value is None:
        return None
    if not isinstance(value, dict):
        return _RESIDUE_INVALID
    extra = value.get("extra")
    if extra is not None and not isinstance(extra, dict):
        return _RESIDUE_INVALID
    optional_missing = value.get("optionalMissing")
    if optional_missing is not None and (
        not isinstance(optional_missing, list)
        or not all(isinstance(item, str) for item in optional_missing)
    ):
        return _RESIDUE_INVALID
    notices = value.get("notices")
    if notices is not None and (
        not isinstance(notices, list)
        or not all(
            isinstance(notice, dict)
            and isinstance(notice.get("code"), str)
            and isinstance(notice.get("message"), str)
            and (
                notice.get("at") is None
                or (isinstance(notice.get("at"), int | float) and not isinstance(notice.get("at"), bool))
            )
            for notice in notices
        )
    ):
        return _RESIDUE_INVALID
    return value


def read_partial_event(
    metadata: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Read + validate a partial-channel event off a metadata dict.

    Returns the event only when it is well-formed and its ``state`` is in the
    closed union. Anything else reads as absent — a malformed partial degrades
    to "no live rendering", never to a wrong render.

    🚨 **This is the TWIN of TS ``readPartialKindEvent``**
    (``@ai-matrx/content-ir`` ``wire/partial-kind.ts``) and the two must accept
    exactly the same events. Until 2026-08-31 this half validated only ``v``
    and ``state``: a structurally corrupt event (no ``engine``, no ``root``, a
    ``retracted`` with no ``reason``, ``seq: true``) passed the Python reader
    and was rejected by the TS one, so Workflow Studio and the parity harness
    trusted events no browser would ever render. Every check below has a named
    counterpart there; change one side and you change both.
    """
    if not isinstance(metadata, dict):
        return None
    event = metadata.get(IR_PARTIAL_KEY)
    if not isinstance(event, dict):
        return None
    if event.get("v") != IR_VERSION:
        return None
    if not isinstance(event.get("engine"), str):
        return None
    if not _is_seq(event.get("seq")):
        return None
    state = event.get("state")
    if state not in PARTIAL_STATES:
        return None

    if state == "partial":
        root = event.get("root")
        if not isinstance(root, dict):
            return None
        if root.get("role") != "structured":
            return None
        if root.get("status") != "streaming":
            return None
        if root.get("kindState") != "speculative":
            return None
        kind = root.get("kind")
        if not isinstance(kind, str) or not kind:
            return None
        if not isinstance(root.get("value"), dict):
            return None
        if _read_discriminator(root.get("discriminator")) is None:
            return None
        if not _is_path(root.get("path")):
            return None
        if _read_residue(root.get("residue")) is _RESIDUE_INVALID:
            return None
        return event

    kind = event.get("kind")
    if not isinstance(kind, str) or not kind:
        return None
    if state == "superseded":
        return event

    reason = event.get("reason")
    if not isinstance(reason, str) or not reason:
        return None
    # Present-and-typed, not merely absent: the TS reader sees ``undefined``
    # for a missing key and rejects it, and a producer that stops sending them
    # must fail LOUDLY on both sides rather than on one.
    for field in ("becameKind", "becameBlockType"):
        if field not in event:
            return None
        value = event[field]
        if value is not None and not isinstance(value, str):
            return None
    return event


# ---------------------------------------------------------------------------
# The tracker — a producer cannot leave a stuck skeleton behind
# ---------------------------------------------------------------------------


class PartialKindTracker:
    """Per-stream ledger of open partials, so every one gets a terminal event.

    A producer calls ``opened`` each time it emits a ``partial`` and ``closed``
    when it emits a terminal. ``drain`` yields a ``retracted`` event for every
    block still open — which is what a producer emits at finalize time for a
    region that was announced and then never resolved (a stream that died, a
    block the final split re-interpreted away). The user sees the skeleton
    disappear with a stated reason instead of watching it forever.
    """

    def __init__(self) -> None:
        self._open: dict[str, str] = {}  # block_id -> provisional kind
        self._seq: dict[str, int] = {}
        self._last_value: dict[str, str] = {}  # block_id -> last emitted value
        self._high_water: dict[str, int] = {}  # block_id -> longest source seen

    def regressed(self, block_id: str, source_len: int) -> bool:
        """Whether this block's source text went BACKWARDS since the last partial.

        LAW 6, enforced rather than assumed: "a partial may be INCOMPLETE; it
        may never be WRONG". A value that appears may still grow; it may never
        shrink, because a client renders each partial as the truth-so-far and a
        shrink shows the user a card, a question or a section VANISHING.

        Measured 2026-08-23 on a real unfenced ``flashcard_set`` stream: the
        splitter re-reads the buffer on every token and momentarily handed one
        block a PREFIX of the content it had already been given
        (cards 2 → 1 → 2). The producer cannot fix the splitter's transient
        from inside the partial channel, and it does not need to — a partial
        built from less source than one already sent carries no new truth, so
        withholding it costs nothing and closes the only way the law could
        break.

        High-water is per block and is cleared with the block (``closed``), so
        a re-typed region starts its own accounting.
        """
        high = self._high_water.get(block_id)
        if high is not None and source_len < high:
            return True
        self._high_water[block_id] = source_len
        return False

    def advanced(self, block_id: str, value: dict[str, Any]) -> bool:
        """Whether ``value`` differs from the last partial sent for this block.

        A block re-splits on every token, so without this the SAME provisional
        value is re-sent dozens of times per region — each carrying the whole
        payload. The event itself still ships (the raw content is streaming);
        only a redundant partial payload is withheld. A consumer therefore sees
        a new ``seq`` exactly when something actually changed.
        """
        serialized = json.dumps(value, sort_keys=True, default=str)
        if self._last_value.get(block_id) == serialized:
            return False
        self._last_value[block_id] = serialized
        return True

    def next_seq(self, block_id: str) -> int:
        seq = self._seq.get(block_id, 0) + 1
        self._seq[block_id] = seq
        return seq

    def opened(self, block_id: str, kind: str) -> None:
        self._open[block_id] = kind

    def is_open(self, block_id: str) -> bool:
        return block_id in self._open

    def open_kind(self, block_id: str) -> str | None:
        return self._open.get(block_id)

    def closed(self, block_id: str) -> None:
        self._open.pop(block_id, None)
        self._last_value.pop(block_id, None)
        self._high_water.pop(block_id, None)

    def drain(
        self,
        reason: str,
        *,
        resolve: Callable[[str], tuple[str | None, str | None]] | None = None,
    ) -> list[tuple[str, dict[str, Any]]]:
        """``(block_id, retracted_event)`` for every partial still open.

        ``resolve`` is asked, per block id, what the region actually BECAME:
        ``(became_kind, became_block_type)``. §3.3 of the wire contract shows
        both fields populated, and the caller is the only one who can know them
        — it is holding the block. Until 2026-08-31 the drain passed neither,
        so every drained retraction serialized ``becameKind: null`` /
        ``becameBlockType: null`` and a consumer's "re-route on what it became"
        branch was structurally unreachable. A resolver that raises is not
        allowed to cost the block its terminal: law 1 outranks the extra
        detail, so the retraction still ships, without it.
        """
        out: list[tuple[str, dict[str, Any]]] = []
        for block_id, kind in list(self._open.items()):
            became_kind: str | None = None
            became_block_type: str | None = None
            if resolve is not None:
                try:
                    became_kind, became_block_type = resolve(block_id)
                except Exception:  # noqa: BLE001 — a terminal is never optional
                    became_kind, became_block_type = None, None
            out.append(
                (
                    block_id,
                    retracted_event(
                        kind=kind,
                        seq=self.next_seq(block_id),
                        reason=reason,
                        became_kind=became_kind,
                        became_block_type=became_block_type,
                    ),
                )
            )
            self.closed(block_id)
        return out
