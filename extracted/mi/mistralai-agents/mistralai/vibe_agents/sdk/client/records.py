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
        case UnknownOutcome(outcome):
            ...  # an outcome a newer host added
        case Running():
            ...
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar

import typing_extensions
from pydantic import BaseModel, JsonValue, ValidationError

from mistralai.vibe.harness.app_server.session.models import AllowApproval, DenyApproval
from mistralai.vibe_agents.sdk.authoring import tool as tool_authoring
from mistralai.vibe_agents.sdk.authoring.errors import ObservationLost, SdkError
from mistralai.vibe_agents.sdk.authoring.tool_result import ToolResult
from mistralai.vibe_agents.sdk.client.approval_requests import ApprovalRequest
from mistralai.vibe_agents.sdk.client.unknown_values import UnknownValue
from mistralai.vibe_agents.sdk.transport.client_tools import ClientToolCall
from mistralai.vibe_agents.sdk.transport.results import ToolCall

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.client.handles import Turn

__all__ = [
    "AlreadySettled",
    "Answered",
    "Blocked",
    "Busy",
    "CancelledTermination",
    "Completed",
    "CompletedTermination",
    "Failed",
    "FailedTermination",
    "Interrupted",
    "InvalidOutput",
    "NotFound",
    "ObservationLost",
    "OpenApproval",
    "OpenCallback",
    "OpenClientToolCall",
    "OpenSignIn",
    "ProtocolError",
    "Running",
    "SessionInfo",
    "SignInRequest",
    "Termination",
    "TurnConflict",
    "TurnState",
    "UnknownOpenCallback",
    "UnknownOutcome",
    "UnknownTermination",
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
    ``OpenSignIn``, an ``OpenClientToolCall`` or an ``UnknownOpenCallback``.

    ``id`` is the one ``turn.answer`` takes, for an approval, a client tool call and a sign-in, on
    any turn of its session or of a session above it in the tree. ``session_id`` and ``turn_id``
    name the session and turn that opened it: a subagent's callback has the subagent's ids, its own
    turn included. A callback whose host names no turn raises ``RuntimeError`` when it is read:
    the Harness hosts name one on every callback. ``kind`` is ``"approval"`` for an approval,
    ``"sign_in"`` for a sign-in and ``"client_tool"`` for a client tool call; a host has other
    kinds for its own use, which can change. ``title`` is an approval's title, ``None`` for the other kinds.
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


@dataclass(frozen=True, slots=True, kw_only=True)
class SignInRequest:
    """One source that a sign-in asks the user to connect.

    ``source`` is ``"connector"`` for a Mistral connector; ``"mcp"`` is for an MCP server, which no
    host asks a sign-in for yet. ``id`` is the source's id, the one ``SignInAnswer`` takes: a
    connector's is the name the Agent gives it, as in ``agents.connector("linear")``. ``name`` is
    the name to show the user: the display name when the host knows it, else the id.
    ``mode`` is ``"connect"`` for a first sign-in and ``"reconnect"`` when the source was connected
    and its access has to be renewed. A newer host may send a ``source`` or a ``mode`` this SDK
    does not know: it is an :class:`UnknownValue`.
    """

    source: Literal["connector", "mcp"] | UnknownValue
    id: str
    name: str
    mode: Literal["connect", "reconnect"] | UnknownValue = "connect"


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class OpenSignIn(OpenCallback):
    """A sign-in the turn waits on: the agent asks the user to connect one or more sources, such
    as connectors, before it uses their tools.

    ``requests`` lists the sources, one ``SignInRequest`` each. Answer it with
    ``turn.answer(callback.id, agents.SignInAnswer(connected=..., denied=...))``, naming each
    source by its ``id``, or with an ``on_sign_in=`` handler, which gets this record. ``kind`` is
    ``"sign_in"``. ``on_client_tool`` never gets a sign-in.
    """

    __match_args__ = ("requests",)

    requests: tuple[SignInRequest, ...] = field(hash=False)


# A client tool's parameters and return type. ``<stub>.called(callback)`` narrows an open call to its
# stub's; without it, any function and any result.
_P = typing_extensions.ParamSpec("_P", default=...)
_R = typing_extensions.TypeVar("_R", default=Any)


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class OpenClientToolCall(OpenCallback, Generic[_P, _R]):
    """A client tool call the turn waits on. ``call`` is the call to answer: the same
    ``ClientToolCall`` an ``on_client_tool`` handler gets for it.

    Check which tool it calls with ``<stub>.called(callback)``, then answer it with
    ``turn.answer(callback.id, await callback.run(fn))``.
    """

    __match_args__ = ("call",)

    call: ClientToolCall = field(hash=False)
    # The stub of the call's tool, from the tools of the Agent, its guardrails and hooks, and its
    # subagents; None without one.
    _tool: tool_authoring.ClientTool[_P, _R] | None = field(default=None, repr=False, compare=False, hash=False)

    async def run(
        self, fn: Callable[_P, _R | ToolResult[Any] | Awaitable[_R | ToolResult[Any]]], /
    ) -> _R | ToolResult[Any]:
        """Call ``fn`` with the call's arguments, validated by the tool's stub, and return its result:
        what ``turn.answer(callback.id, ...)`` takes for this call.

        ``fn`` takes the stub's parameters, without a context, and returns the stub's return type
        or an ``agents.ToolResult``, synchronously or not. A synchronous ``fn`` runs in a tool
        thread. An exception ``fn`` raises propagates: ``tool_errors`` does not apply.

        When the model's arguments do not match the stub, ``fn`` is not called: the result is an
        error ``agents.ToolResult`` saying why, so that answering it lets the model correct the call.

        Raises:
            SdkError: the tools of the Agent, its guardrails and hooks, and its subagents have no stub
                for this tool, as on a handle from ``Agent.load_from()``, or two different stubs share
                its ID. Read ``call.arguments`` instead.
        """
        tool = self._tool
        if tool is None:
            raise SdkError(
                f"No stub for the client tool {self.call.name}: run() needs it in the tools= of the Agent, of "
                "its guardrails and hooks or of its subagents, and no other stub with the same ID. Read the "
                "arguments from callback.call.arguments instead"
            )
        try:
            parsed: BaseModel = tool._declaration.input_model.model_validate(self.call.arguments)
        except ValidationError as error:
            return ToolResult.error(f"{type(error).__name__}: {error}")
        result: _R | ToolResult[Any] = await tool_authoring.call_with_arguments(tool, fn, parsed)
        return result


# TODO: a new callback kind breaks an older client that cannot answer it. Gate each new kind
# behind a flag the client sets at session creation, so an older client never gets a kind it
# cannot handle (user, 3 Nov). Linear: https://linear.app/mistral-ai/issue/AGE-2316/session-v1-an-older-client-never-gets-a-callback-kind-it-cannot-answer
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
    """The turn completed, possibly early: see ``stop_reason``.

    ``output`` is the turn's output, validated against the requested type, or
    :class:`InvalidOutput` when it did not validate. With ``output_type``, it is ``None``
    when the turn ended early: ``stop_reason`` is ``"iteration_limit"`` (the turn reached its
    iteration limit), ``"skipped"`` (a hook skipped it), ``"rejected"`` (a hook rejected the
    reply) or ``"output_limit"`` (the model's last reply stopped at the output token limit after
    the harness asked it again for a shorter reply, up to 6 times), so there is no answer to parse.
    Without ``output_type``, it is the turn's text, also when the turn ended early (a
    skipped turn's text is the hook's reason, a cut-off turn's text is the cut-off reply), or
    ``""`` when there is none.
    ``stop_reason`` is ``None`` when the turn ended normally. ``tool_calls`` lists the turn's own
    tool calls in the order the model made them; a subagent's calls are not included.
    """

    __match_args__ = ("output",)

    output: _T_co | InvalidOutput | None
    stop_reason: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Interrupted(_TurnRecord):
    """The turn stopped before it completed.

    ``cause`` says why, as the host reports it:

    - ``"interrupted"``: a client interrupted the turn;
    - ``"cancelled"``: a client cancelled or closed the turn's session;
    - ``"lifetime_limit"`` or ``"idle_limit"``: the session reached one of its limits.

    When the host names no cause, as an older one may, the SDK reads ``"cancelled"`` if the turn
    ended with its cancelled session, else ``"interrupted"``. A newer host may report a cause not
    listed here.
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


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownOutcome(_TurnRecord):
    """The turn ended with an outcome this SDK does not know, such as ``"budget_exceeded"``.

    ``outcome`` is that outcome, and ``raw`` the turn's termination as the host sent it. A newer host
    can add outcomes: leave a ``case`` for this one, so your code still runs.
    """

    __match_args__ = ("outcome", "raw")

    outcome: str
    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)


type TurnState[T] = Running | Blocked | Completed[T] | Interrupted | Failed | UnknownOutcome
"""A turn's state as of ``cursor``: one of the six records ``Running``, ``Blocked``, ``Completed``,
``Interrupted``, ``Failed`` and ``UnknownOutcome``."""


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

    ``answer`` is the approval answer that counted. It is another client's when that client
    answered first: compare it with yours to tell. It is ``None`` when the host did not say, as an
    older host does not, and for a client tool call: no host says which result counted.
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
    """An answer named a callback that the session never opened, and that none of its subagents
    has open. Nothing changed.

    Once a subagent's callback is no longer open, its root says ``NotFound``: the subagent's own
    session says ``AlreadySettled``.
    """

    session_id: str
    callback_id: str


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CompletedTermination:
    """The session completed.

    ``stop_reason`` is ``"iteration_limit"`` when it reached its iteration limit, ``"skipped"`` when
    a hook skipped its work, ``"rejected"`` when a ``post_llm_call`` hook rejected the reply,
    ``"output_limit"`` when the model's last reply stopped at the output token limit, and
    ``None`` when it ended normally. A deployed session's record always has ``None``: the control
    plane does not keep the reason with the session. Its turn's result has it. A stop reason a
    newer host added is an :class:`UnknownValue`.
    """

    __match_args__ = ("stop_reason",)

    stop_reason: Literal["iteration_limit", "skipped", "rejected", "output_limit"] | UnknownValue | None = None


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CancelledTermination:
    """The session was cancelled.

    ``cause`` is ``"lifetime_limit"`` or ``"idle_limit"`` when it reached one of its limits, and
    ``None`` when a client cancelled it. A newer host may report another cause.
    """

    __match_args__ = ("cause",)

    cause: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class FailedTermination:
    """The session failed. ``error`` is the error the host reported."""

    __match_args__ = ("error",)

    error: ProtocolError


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownTermination:
    """The session ended with an outcome this SDK does not know, such as ``"budget_exceeded"``.

    ``outcome`` is that outcome, and ``raw`` the termination as the host sent it. A newer host can
    add outcomes: leave a ``case`` for this one, so your code still runs.
    """

    __match_args__ = ("outcome", "raw")

    outcome: str
    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)


type Termination = CompletedTermination | CancelledTermination | FailedTermination | UnknownTermination
"""How a session ended: one class for each outcome, and ``UnknownTermination`` for an outcome this
SDK does not know."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionInfo:
    """One session found in a listing.

    ``status`` is ``"running"`` while a turn is active, ``"waiting"`` when no turn is, and
    ``"terminated"`` once the session has ended, and an :class:`UnknownValue` for a status a newer
    host added; ``termination`` says how it ended, and is ``None`` until then. ``parent_id`` is the
    parent session of a
    subagent, or ``None`` for a root session; ``root_id`` is the root session of its tree, its own
    ``id`` for a root. ``title`` is the session's title, or ``None`` when it has none yet. The
    times are in UTC; ``archived_at`` is ``None`` for a session that is not archived. A listing
    gives unarchived sessions only, so ``archived_at`` is ``None`` in every listed record.
    """

    id: str
    parent_id: str | None
    root_id: str
    title: str | None
    status: Literal["running", "waiting", "terminated"] | UnknownValue
    created_at: datetime
    updated_at: datetime
    archived_at: datetime | None
    termination: Termination | None
