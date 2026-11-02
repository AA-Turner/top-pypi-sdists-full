"""Records: what the host reported about a turn or a session, as immutable values.

A record holds no connection and sends no request (``Busy.turn`` is a handle: it sends one only
when it is used). It is what the host reported at one position of the session's log, and it keeps
that position in ``cursor``. A record does not
change after it is created, so it can be out of date: read the turn again for a newer one.

Records are shallowly immutable: their fields cannot be reassigned, but a field that holds the
host's JSON (``UnknownOpenCallback.raw``, ``OpenClientToolCall.call.arguments``,
``InvalidOutput.raw``, ``ToolCall.arguments``, ``ProtocolError.details``, and ``Completed.output``
when it is a dict or a list) is the object as received, not a frozen copy. Do not change it: copy
it first.

Every read or wait of a turn returns one :data:`TurnState`. Match on its type::

    match state:
        case Completed(output):
            ...
        case Blocked(callbacks):
            ...
        case Interrupted(cause):
            ...
        case Failed(error):
            ...
        case Running():
            ...
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Generic, Literal, TypeVar

from pydantic import JsonValue

from mistralai.vibe.harness.app_server.session.models import AllowApproval, DenyApproval
from mistralai.vibe_agents.sdk.authoring.errors import ObservationLost
from mistralai.vibe_agents.sdk.client.approval_requests import ApprovalRequest
from mistralai.vibe_agents.sdk.transport.client_tools import ClientToolCall
from mistralai.vibe_agents.sdk.transport.results import ToolCall

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.client.handles import Turn

__all__ = [
    "AlreadySettled",
    "Answered",
    "Blocked",
    "Busy",
    "Completed",
    "Failed",
    "Interrupted",
    "InvalidOutput",
    "NotFound",
    "ObservationLost",
    "OpenApproval",
    "OpenCallback",
    "OpenClientToolCall",
    "ProtocolError",
    "Running",
    "SessionInfo",
    "Termination",
    "TurnConflict",
    "TurnState",
    "UnknownOpenCallback",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class _TurnRecord:
    """The fields every turn state has.

    ``cursor`` is the id of the position in the session's log that the record was read at. For a
    ``Running`` or ``Blocked`` that a wait with ``on_event`` returns, it is the position the
    handler's events reached, when that differs.
    ``text`` is the turn's latest assistant text at that position, or ``None`` before the first one.
    """

    session_id: str
    turn_id: str
    cursor: str
    text: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class Running(_TurnRecord):
    """The turn is working. Nothing waits on you."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OpenCallback:
    """A callback that the turn, or one of its subagents, waits on: an ``OpenApproval``, an
    ``OpenClientToolCall`` or an ``UnknownOpenCallback``.

    ``id`` is the one ``turn.answer`` takes for an approval; a client tool call is answered with
    the raw client's ``answer_callback``. ``session_id`` and ``turn_id`` name the session and
    turn that opened it: a subagent's callback has the subagent's ids, its own turn included. When
    the host does not send the turn, the SDK reads the session that opened the callback for its
    running turn. ``kind`` is ``"approval"`` for an approval and ``"client_tool"`` for a client tool
    call; a host has other kinds for its own use, which can change. ``title`` is an approval's
    title, ``None`` for the other kinds.
    """

    id: str
    session_id: str
    turn_id: str
    kind: str
    title: str | None


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class OpenApproval(OpenCallback):
    """An approval the turn waits on. ``request`` is the tool call it is for: the same
    ``ApprovalRequest`` an ``on_approval`` handler gets for it."""

    __match_args__ = ("request",)

    request: ApprovalRequest = field(hash=False)


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class OpenClientToolCall(OpenCallback):
    """A client tool call the turn waits on. ``call`` is the call to answer: the same
    ``ClientToolCall`` an ``on_client_tool`` handler gets for it."""

    __match_args__ = ("call",)

    call: ClientToolCall = field(hash=False)


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownOpenCallback(OpenCallback):
    """A callback of a kind with no type of its own here. ``raw`` is the callback as the host
    sent it.

    A newer SDK can give a kind a type of its own. Match on ``kind``, and leave open the kinds
    that you do not know.
    """

    __match_args__ = ("kind", "raw")

    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Blocked(_TurnRecord):
    """The turn waits for an answer to one or more callbacks, as the host lists them."""

    __match_args__ = ("callbacks",)

    callbacks: tuple[OpenCallback, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class InvalidOutput:
    """The turn completed, but its output did not validate against the requested type.

    ``raw`` is the turn's text. ``error`` says why it did not validate.
    """

    raw: JsonValue
    error: str


# Declared covariant: mypy infers a frozen dataclass's parameter as invariant, and a
# Completed[Model] must be accepted where any record is, as Completed[object].
_T_co = TypeVar("_T_co", covariant=True)


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Completed(_TurnRecord, Generic[_T_co]):
    """The turn ended normally.

    ``output`` is the turn's output, validated against the requested type, or
    :class:`InvalidOutput` when it did not validate. ``tool_calls`` lists the turn's own tool
    calls in the order the model made them; a subagent's calls are not included.
    """

    __match_args__ = ("output",)

    output: _T_co | InvalidOutput
    stop_reason: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Interrupted(_TurnRecord):
    """The turn stopped before it completed.

    ``cause`` says why, as the host reports it:

    - ``"interrupted"``: a client interrupted the turn;
    - ``"cancelled"``: a client cancelled or closed the turn's session;
    - ``"lifetime_limit"`` or ``"idle_limit"``: the session reached one of its limits.

    When the host names no limit, a turn whose end the host did not report has the cause
    ``"cancelled"`` when its session was cancelled; any other stopped turn has ``"interrupted"``,
    so a turn the host ended while cancelling its session usually reads ``"interrupted"``. A newer
    host may report a cause not listed here.
    ``text`` is what the turn said before it stopped.
    """

    __match_args__ = ("cause",)

    cause: str


@dataclass(frozen=True, slots=True, kw_only=True)
class ProtocolError:
    """An error reported by the host.

    ``code`` is ``None`` when the host gave no code. ``retryable`` is ``True`` when sending the same
    request again may succeed, for example after a model stream timeout. ``details`` is the
    structured data the host reported with the error, such as
    ``{"reason": "invalid_request_error", "status_code": 422}`` from the model provider, or
    ``None`` when it reported none (data that is not a JSON object is left out).
    """

    message: str
    code: str | None = None
    retryable: bool = False
    details: dict[str, JsonValue] | None = None


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Failed(_TurnRecord):
    """The turn ended with an error, for example a refusal from the model provider."""

    __match_args__ = ("error",)

    error: ProtocolError


type TurnState[T] = Running | Blocked | Completed[T] | Interrupted | Failed
"""A turn's state as of ``cursor``: one of the five records above."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Busy:
    """A new turn was not started, because another turn of the session is active.

    ``active_turn_id`` is that turn, and ``turn`` is its handle, to steer, interrupt or wait for.
    This is not a turn state: no turn was started.
    """

    session_id: str
    active_turn_id: str
    turn: Turn = field(compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class TurnConflict:
    """A request named a turn that is no longer the session's active turn. Nothing was sent.

    ``active_turn_id`` is the turn that is active now, or ``None`` when no turn is.
    """

    session_id: str
    expected_turn_id: str
    active_turn_id: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class Answered:
    """The callback was open when read, and it was answered.

    ``answer`` is the answer that counted. It is another client's when that client answered
    first: compare it with yours to tell. It is ``None`` when the host did not say, as an older
    host does not.
    """

    session_id: str
    callback_id: str
    answer: AllowApproval | DenyApproval | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class AlreadySettled:
    """An answer named a callback that is no longer open: it was answered, or it closed. Nothing changed.

    Another client may have answered first, the callback's turn ended, or the session ended.
    """

    session_id: str
    callback_id: str


@dataclass(frozen=True, slots=True, kw_only=True)
class NotFound:
    """An answer named a callback that the session never opened. Nothing changed.

    A subagent's callback is opened by the subagent's session: answer it there.
    """

    session_id: str
    callback_id: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Termination:
    """How a session ended.

    ``outcome`` is ``"completed"``, ``"cancelled"`` or ``"failed"``. The other fields are set for
    one outcome only, and are ``None`` otherwise:

    - ``stop_reason``, when it completed: ``"iteration_limit"`` when it reached its iteration
      limit, ``"skipped"`` when a hook skipped its work, ``None`` when it ended normally. A
      deployed session's record always has ``None``: the control plane does not keep the reason
      with the session. Its turn's result has it;
    - ``cause``, when it was cancelled: ``"lifetime_limit"`` or ``"idle_limit"`` when it reached one
      of its limits, ``None`` when a client cancelled it. A newer host may report another cause;
    - ``error``, when it failed: the error the host reported.
    """

    outcome: Literal["completed", "cancelled", "failed"]
    stop_reason: Literal["iteration_limit", "skipped"] | None = None
    cause: str | None = None
    error: ProtocolError | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionInfo:
    """One session found in a listing.

    ``status`` is ``"running"`` while a turn is active, ``"waiting"`` when no turn is, and
    ``"terminated"`` once the session has ended; ``termination`` says how it ended, and is ``None``
    until then. ``parent_id`` is the parent session of a
    subagent, or ``None`` for a root session; ``root_id`` is the root session of its tree, its own
    ``id`` for a root. ``title`` is the session's title, or ``None`` when it has none yet. The
    times are in UTC; ``archived_at`` is ``None`` for a session that is not archived. A listing
    gives unarchived sessions only, so ``archived_at`` is ``None`` in every listed record.
    """

    id: str
    parent_id: str | None
    root_id: str
    title: str | None
    status: Literal["running", "waiting", "terminated"]
    created_at: datetime
    updated_at: datetime
    archived_at: datetime | None
    termination: Termination | None
