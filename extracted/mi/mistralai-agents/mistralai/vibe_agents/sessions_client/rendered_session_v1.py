"""Client-side reconstruction of a Session v1 session from its ``/events`` stream.

Unlike the legacy task protocol (see :mod:`~mistralai.vibe_agents.sessions_client.rendered_session`,
a JSON-patch stream against an opaque entry list), Session v1 delivers whole
history entries: ``history_entry_added`` carries the entry, ``history_entry_completed``
carries its final form, and ``history_entry_patched`` refines one entry in place
while it is still generating. Turn, session and callback lifecycle arrive as their
own events rather than being encoded as state rows.

Frames are parsed with ``ClientEvent``, whose validator downgrades payload types
this SDK does not know to ``UnknownEventPayload`` instead of raising, so a server
that starts emitting new event types never breaks an older client. Each frame is
parsed once; a frame that does not parse is logged and skipped.
"""

import copy
from bisect import insort_right
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

import structlog
from pydantic import ValidationError

from mistralai.vibe.harness.app_server.session.models import (
    ApprovalCallback,
    CheckpointHistoryEntry,
    ClientEvent,
    HistoryEntry,
    HistoryEntryAdapter,
    NoticeHistoryEntry,
    ProtocolError,
    Session,
    SessionCallback,
    TextContentBlock,
    TurnState,
    UnknownEventPayload,
    UnknownHistoryEntry,
)
from mistralai.vibe_agents.sessions_client.rendered_session import Callback

logger = structlog.get_logger(__name__)

# Callback kinds whose open callback leaves the session waiting on a client answer.
# The Nuage-native channel sends ask_user_question and connector prompts as client_tool.
V1_BLOCKING_CALLBACK_KINDS = frozenset({"approval", "user_input", "client_tool"})

# History entries the harness also emits outside a turn, so their arrival says
# nothing about the agent taking back control. An entry of a type this SDK does not
# know may be one of them, so it does not count either.
_SIDECAR_ENTRIES = (CheckpointHistoryEntry, NoticeHistoryEntry, UnknownHistoryEntry)


def _callback_prompt(callback: SessionCallback) -> str:
    if isinstance(callback, ApprovalCallback):
        return callback.title
    message = getattr(callback, "message", None)
    if not isinstance(message, list):
        return ""
    return "".join(block.text for block in message if isinstance(block, TextContentBlock))


def _callback_uuid(raw_id: str) -> UUID | None:
    try:
        return UUID(raw_id)
    except ValueError:
        return None


def callback_from_v1_callback(callback: SessionCallback) -> Callback | None:
    """Adapt a canonical session callback to the client-facing :class:`Callback`.

    Returns ``None`` when the id is not a UUID. ``CallbackId`` is typed as a bare
    string in the protocol, but vibe_agents issues UUIDs and its callback-result
    route only accepts them, so a non-UUID id is not answerable by this client.
    """
    callback_id = _callback_uuid(callback.id)
    if callback_id is None:
        return None
    return Callback(
        id=callback_id,
        name=callback.kind,
        prompt=_callback_prompt(callback),
        input=callback.model_dump(mode="json"),
    )


# Frames of the legacy task protocol. The served stream of a Session v1 session still carries
# them for older readers; this client reads the v1 events beside them and skips these quietly.
_LEGACY_FRAME_TYPES = frozenset({"history_update", "callback_call", "task_result"})


def parse_session_v1_event(event: dict[str, Any]) -> ClientEvent | None:
    """Parse one ``/events`` frame payload; ``None`` when it is not a valid v1 event."""
    frame_type = event.get("type")
    if frame_type in _LEGACY_FRAME_TYPES:
        logger.debug("Skipping legacy task-protocol frame", frame_type=frame_type)
        return None
    try:
        return ClientEvent.model_validate(event)
    except ValidationError as error:
        payload = event.get("payload")
        logger.warning(
            "Skipping invalid Session v1 frame",
            payload_type=payload.get("type") if isinstance(payload, dict) else None,
            error=str(error),
        )
        return None


@dataclass(slots=True)
class RenderedSessionV1:
    """Accumulates canonical Session v1 events into a readable session view."""

    entries: list[HistoryEntry] = field(default_factory=list)
    session: Session | None = None
    latest_turn: TurnState | None = None
    active_callbacks: dict[str, SessionCallback] = field(default_factory=dict)
    # Every callback the stream has reported resolved. Kept apart from clearing
    # ``active_callbacks`` because a caller waiting for its own answer to be taken needs
    # to tell "resolved" from "never opened here", which an absence cannot say.
    resolved_callback_ids: set[str] = field(default_factory=set)
    notices: list[str] = field(default_factory=list)
    errors: list[ProtocolError] = field(default_factory=list)
    unknown_event_count: int = 0
    invalid_frame_count: int = 0
    # The frame `apply_public_session_event` last folded, and what it parsed to, so the
    # driver asking `callback_from_event` about that same frame does not parse it twice.
    _last_frame: tuple[dict[str, Any], ClientEvent | None] | None = field(
        default=None, init=False, repr=False, compare=False
    )
    # Latched by the events that hand control back, cleared by any sign of new
    # activity. A stale value is what makes a renderer unusable for a second
    # turn, so every branch of the fold sets it explicitly rather than reading
    # it back off ``session`` or ``latest_turn``, which both lag the stream.
    _handed_back: bool = False

    @property
    def is_terminated(self) -> bool:
        return self.session is not None and self.session.status == "terminated"

    @property
    def is_blocked_on_callback(self) -> bool:
        """Whether an open callback blocks the session, answerable by this client or not.

        Being blocked and being able to answer are different questions. A Host publishes
        the id its own answer route accepts, and one that publishes something this client
        cannot use leaves a callback visible and unanswerable. The session is blocked all
        the same, and a reader that conflated the two would report the agent as still
        working while it waits on a user who is never asked.
        """
        return any(callback.kind in V1_BLOCKING_CALLBACK_KINDS for callback in self.active_callbacks.values())

    @property
    def blocking_callback(self) -> Callback | None:
        """The first open callback this client can both see and answer, if any.

        ``None`` does not mean the session is unblocked; see
        :attr:`is_blocked_on_callback`.
        """
        for callback in self.active_callbacks.values():
            if callback.kind not in V1_BLOCKING_CALLBACK_KINDS:
                continue
            answerable = callback_from_v1_callback(callback)
            if answerable is not None:
                return answerable
        return None

    @property
    def waiting_for_input(self) -> bool:
        """Whether the agent has handed control back and is waiting on the user.

        An open blocking callback is live state, so it is read directly. The two
        other signals, a waiting session status and a terminated turn, are
        latched on ``_handed_back``, because they describe a transition rather
        than a condition and nothing in the stream restates them.

        A blocking callback wins over the latch: the session blocks on the user
        while its turn is still running.
        """
        if self.is_terminated:
            return False
        if self.is_blocked_on_callback:
            return True
        return self._handed_back

    def resolve_callback(self, callback_id: UUID) -> None:
        """Forget a callback the client has answered.

        Only ``callback_resolved`` clears ``active_callbacks`` otherwise, and the
        driver re-reads ``waiting_for_input`` right after answering, so without
        this the answered callback would still read as blocking and end the wait.
        """
        for raw_id in [raw for raw in self.active_callbacks if _callback_uuid(raw) == callback_id]:
            del self.active_callbacks[raw_id]

    def holds_entry(self, entry_id: str) -> bool:
        """Whether the stream delivered this history entry, so a patch to it can apply."""
        return any(entry.id == entry_id for entry in self.entries)

    def callback_from_event(self, event: dict[str, Any]) -> Callback | None:
        """Return the actionable callback a ``callback_opened`` event carries, if any."""
        if self._last_frame is not None and self._last_frame[0] is event:
            parsed = self._last_frame[1]
        else:
            parsed = parse_session_v1_event(event)
        if parsed is None or parsed.payload.type != "callback_opened":
            return None
        return callback_from_v1_callback(parsed.payload.callback)

    def apply_public_session_event(self, event: dict[str, Any]) -> None:
        """Fold one public session event (the inner ``event`` of an /events frame)."""
        parsed = parse_session_v1_event(event)
        self._last_frame = (event, parsed)
        if parsed is None:
            self.invalid_frame_count += 1
            return
        self.apply_parsed_event(parsed)

    def apply_parsed_event(self, parsed: ClientEvent) -> None:
        """Fold an already-parsed frame.

        Callers that need the parsed event for their own reasons use this so one frame is
        validated once, rather than here and again at the call site.
        """

        payload = parsed.payload
        if isinstance(payload, UnknownEventPayload):
            self.unknown_event_count += 1
            logger.debug("Skipping unknown Session v1 event payload", payload_type=payload.original_type)
            return

        match payload.type:
            case "history_entry_added":
                # The first frame of a new turn, ahead of turn_started and of
                # session_updated("running"). Clearing here is what lets a
                # renderer be reused to drive the turn after a wait. Checkpoints
                # and notices are excluded: the harness emits them between turns
                # too, so they would clear the latch on a session still waiting.
                if not isinstance(payload.entry, _SIDECAR_ENTRIES):
                    self._handed_back = False
                self._upsert_entry(payload.entry)
            case "history_entry_completed":
                self._upsert_entry(payload.entry)
            case "history_entry_patched":
                if not self._patch_entry(payload.entry_id, payload.patches):
                    self.invalid_frame_count += 1
            case "turn_started":
                self.latest_turn = payload.turn
                self._handed_back = False
            case "turn_updated":
                self.latest_turn = payload.turn
            case "turn_terminated":
                self.latest_turn = payload.turn
                self._handed_back = True
            case "session_updated":
                self.session = payload.session
                self._handed_back = payload.session.status == "waiting"
            case "session_terminated":
                self.session = payload.session
            case "callback_opened":
                self.active_callbacks[payload.callback.id] = payload.callback
            case "callback_resolved":
                self.active_callbacks.pop(payload.callback_id, None)
                self.resolved_callback_ids.add(payload.callback_id)
            case "notice":
                self.notices.append(payload.message)
            case "error":
                self.errors.append(payload.error)

    def _upsert_entry(self, entry: HistoryEntry) -> None:
        for position, existing in enumerate(self.entries):
            if existing.id == entry.id:
                self.entries[position] = entry
                return
        # Entries are keyed by a projector-allocated dense index, so ordering by it
        # keeps the list readable even if frames arrive out of order after a resume.
        insort_right(self.entries, entry, key=lambda candidate: candidate.index)

    def _patch_entry(self, entry_id: str, patches: Sequence[Any]) -> bool:
        for position, existing in enumerate(self.entries):
            if existing.id != entry_id:
                continue
            document = existing.model_dump(mode="json")
            for patch in patches:
                if not _apply_patch(document, patch.model_dump(mode="json")):
                    return False
            try:
                self.entries[position] = HistoryEntryAdapter.validate_python(document)
            except ValidationError:
                return False
            return True
        return False


def _pointer_tokens(path: str) -> list[str] | None:
    if not path.startswith("/"):
        return None
    return [part.replace("~1", "/").replace("~0", "~") for part in path.removeprefix("/").split("/")]


def _resolve_parent(document: Any, tokens: list[str]) -> tuple[Any, str] | None:
    current = document
    for token in tokens[:-1]:
        if isinstance(current, dict):
            if token not in current:
                return None
            current = current[token]
        elif isinstance(current, list):
            index = _list_index(token, len(current))
            if index is None:
                return None
            current = current[index]
        else:
            return None
    return current, tokens[-1]


def _list_index(token: str, length: int, *, allow_end: bool = False) -> int | None:
    if token == "-" and allow_end:  # noqa: S105 — JSON-pointer token, not a secret
        return length
    try:
        index = int(token)
    except ValueError:
        return None
    if index < 0 or index > length or (index == length and not allow_end):
        return None
    return index


def _apply_patch(document: dict[str, Any], patch: dict[str, Any]) -> bool:
    tokens = _pointer_tokens(patch.get("path", ""))
    if not tokens:
        return False
    resolved = _resolve_parent(document, tokens)
    if resolved is None:
        return False
    parent, token = resolved
    op = patch.get("op")

    if op == "remove":
        return _remove(parent, token)
    if op == "append":
        value = patch.get("value")
        return _append(parent, token, value) if isinstance(value, str) else False
    if op in ("add", "replace"):
        return _set(parent, token, copy.deepcopy(patch.get("value")), allow_insert=op == "add")
    # move/copy/test are in the protocol union but the producer does not emit them;
    # treating them as invalid keeps a silent no-op from looking like a clean apply.
    return False


def _set(parent: Any, token: str, value: Any, *, allow_insert: bool) -> bool:
    if isinstance(parent, dict):
        if not allow_insert and token not in parent:
            return False
        parent[token] = value
        return True
    if isinstance(parent, list):
        index = _list_index(token, len(parent), allow_end=allow_insert)
        if index is None:
            return False
        if allow_insert:
            parent.insert(index, value)
        else:
            parent[index] = value
        return True
    return False


def _remove(parent: Any, token: str) -> bool:
    if isinstance(parent, dict):
        if token not in parent:
            return False
        del parent[token]
        return True
    if isinstance(parent, list):
        index = _list_index(token, len(parent))
        if index is None:
            return False
        parent.pop(index)
        return True
    return False


def _append(parent: Any, token: str, value: str) -> bool:
    if isinstance(parent, dict):
        if not isinstance(parent.get(token), str):
            return False
        parent[token] += value
        return True
    if isinstance(parent, list):
        index = _list_index(token, len(parent))
        if index is None or not isinstance(parent[index], str):
            return False
        parent[index] += value
        return True
    return False


__all__ = [
    "V1_BLOCKING_CALLBACK_KINDS",
    "RenderedSessionV1",
    "callback_from_v1_callback",
    "parse_session_v1_event",
]
