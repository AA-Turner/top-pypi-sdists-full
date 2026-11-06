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
            ...  # an outcome added after your SDK version
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
    """The fields every turn state has."""

    session_id: str
    """The ID of the turn's session."""
    turn_id: str
    """The ID of the turn."""
    cursor: str
    """The ID of the position in the session's log that the record was read at.

    For a ``Running`` or ``Blocked`` that a wait with ``on_event`` returns, it is the position the
    handler's events reached, when that differs.
    """
    text: str | None
    """The turn's latest assistant text at that position, or ``None`` before the first one."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Running(_TurnRecord):
    """The turn is working. Nothing waits on you."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OpenCallback:
    """A callback that the turn, or one of its subagents, waits on: an ``OpenApproval``, an
    ``OpenSignIn``, an ``OpenClientToolCall`` or an ``UnknownOpenCallback``.

    ``turn.answer`` takes its ``id`` on any turn of its session or of a session above it in the tree.
    A subagent's callback has the subagent's IDs, its own turn included.
    """

    id: str
    """The callback's ID, the one ``turn.answer`` takes."""
    session_id: str
    """The ID of the session that opened the callback: a subagent's, for a subagent's callback."""
    turn_id: str
    """The ID of the turn that opened the callback."""
    kind: str
    """``"approval"``, ``"sign_in"`` or ``"client_tool"``; other kinds are for Mistral's own use."""
    title: str | None
    """An approval's title, ``None`` for the other kinds."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class OpenApproval(OpenCallback):
    """An approval the turn waits on."""

    __match_args__ = ("request",)

    request: ApprovalRequest = field(hash=False)
    """The tool call that the approval is for: the same ``ApprovalRequest`` an ``on_approval`` handler gets."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SignInRequest:
    """One source that a sign-in asks the user to connect."""

    source: Literal["connector", "mcp"] | UnknownValue
    """``"connector"`` for a Mistral connector, ``"mcp"`` for an MCP server, or an :class:`UnknownValue` for a
    source added after your SDK version."""
    id: str
    """The source's ID, the one ``SignInAnswer`` takes: a connector's is the name the agent gives it, as in
    ``agents.connector("linear")``."""
    name: str
    """The name to show the user: its display name when Mistral has one, else the ID."""
    mode: Literal["connect", "reconnect"] | UnknownValue = "connect"
    """``"connect"`` for a first sign-in, ``"reconnect"`` when the source was connected and its access has to be
    renewed, or an :class:`UnknownValue` for a mode added after your SDK version."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class OpenSignIn(OpenCallback):
    """A sign-in the turn waits on: the agent asks the user to connect one or more sources, such
    as connectors, before it uses their tools.

    Answer it with ``turn.answer(callback.id, agents.SignInAnswer(connected=..., denied=...))``,
    naming each source by its ``id``, or with an ``on_sign_in=`` handler, which gets this record.
    ``kind`` is ``"sign_in"``. ``on_client_tool`` never gets a sign-in.
    """

    __match_args__ = ("requests",)

    requests: tuple[SignInRequest, ...] = field(hash=False)
    """The sources to connect, one ``SignInRequest`` each."""


# A client tool's parameters and return type. ``<stub>.called(callback)`` narrows an open call to its
# stub's; without it, any function and any result.
_P = typing_extensions.ParamSpec("_P", default=...)
_R = typing_extensions.TypeVar("_R", default=Any)


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class OpenClientToolCall(OpenCallback, Generic[_P, _R]):
    """A client tool call the turn waits on.

    Check which tool it calls with ``<stub>.called(callback)``, then answer it with
    ``turn.answer(callback.id, await callback.run(fn))``.
    """

    __match_args__ = ("call",)

    call: ClientToolCall = field(hash=False)
    """The call to answer: the same ``ClientToolCall`` an ``on_client_tool`` handler gets."""
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

        Args:
            fn: The function that runs the tool on this side, with the stub's parameters.

        Raises:
            SdkError: No stub for this tool in the agent's tools, guardrails, hooks or subagents (as on
                a handle from ``Agent.load_from()``), or two stubs share its ID. Read ``call.arguments``
                instead.
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
    """A callback of a kind with no type of its own in your SDK version.

    A later SDK version can give a kind a type of its own. Match on ``kind``, and leave open the kinds
    that you do not know.
    """

    __match_args__ = ("kind", "raw")

    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)
    """The callback's data, unparsed."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Blocked(_TurnRecord):
    """The turn waits for an answer to one or more callbacks."""

    __match_args__ = ("callbacks",)

    callbacks: tuple[OpenCallback, ...]
    """The callbacks the turn waits on."""


@dataclass(frozen=True, slots=True, kw_only=True)
class InvalidOutput:
    """The turn completed, but its output did not validate against the requested type."""

    raw: JsonValue
    """The turn's text."""
    error: str
    """Why it did not validate."""


# Declared covariant: mypy infers a frozen dataclass's parameter as invariant, and a
# Completed[Model] must be accepted where any record is, as Completed[object].
_T_co = TypeVar("_T_co", covariant=True)


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Completed(_TurnRecord, Generic[_T_co]):
    """The turn completed, possibly early: see ``stop_reason``.

    With ``output_type``, ``output`` is ``None`` when the turn ended early, so there is no answer to
    parse. Without ``output_type``, it is the turn's text, also when the turn ended early (a skipped
    turn's text is the hook's reason, a cut-off turn's text is the cut-off reply), or ``""`` when there
    is none.
    """

    __match_args__ = ("output",)

    output: _T_co | InvalidOutput | None
    """The turn's text; with ``output_type``, that text parsed, :class:`InvalidOutput` when it does not
    validate, or ``None`` when the turn ended early."""
    stop_reason: str | None = None
    """``"iteration_limit"`` (the turn reached its iteration limit), ``"skipped"`` (a hook skipped it),
    ``"rejected"`` (a hook rejected the reply), ``"output_limit"`` (the model's last reply stopped at the output
    token limit, after the agent asked it for a shorter reply up to 6 times), ``None`` when the turn ended
    normally, or a stop reason added after your SDK version."""
    tool_calls: tuple[ToolCall, ...] = ()
    """The turn's own tool calls, in the order the session history records them; a subagent's calls are not included."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Interrupted(_TurnRecord):
    """The turn stopped before it completed.

    When no cause is given, the SDK reads ``"cancelled"`` if the turn ended with its cancelled session, else
    ``"interrupted"``.
    ``text`` is what the turn said before it stopped.
    """

    __match_args__ = ("cause",)

    cause: str
    """Why the turn stopped: ``"interrupted"`` (a client interrupted the turn), ``"cancelled"`` (a client
    cancelled or closed the turn's session), ``"lifetime_limit"`` or ``"idle_limit"`` (the session reached one
    of its limits), or a cause added after your SDK version."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ProtocolError:
    """An error from where the session runs, such as the one a turn failed with.

    The ``code`` of a failed turn's error says what failed, so you can match on it:

    - ``"completion_rejected"``: the model provider refused the request with an HTTP 4xx status other than 401,
      403, 408, 409 and 429, for example an unknown model or an invalid parameter: fix the request.
    - ``"completion_unauthorized"``: the model provider refused the credentials (HTTP 401 or 403). Not retryable.
    - ``"completion_rate_limited"``: more requests than your rate limit allows (HTTP 429 with reason
      ``rate_limited``). Retryable.
    - ``"completion_unavailable"``: the model provider could not serve the request: no model capacity (HTTP 409,
      or any other 429), an outage or a server error. Retryable for a transient cause, such as HTTP 502, 503 or
      504.
    - ``"completion_timed_out"``: the provider answered HTTP 408, the model stopped producing output, or the
      call ran past its time limit. Retryable, except for a call past its time limit.
    - ``"completion_context_too_large"``: the request is larger than the model's context window. Not
      retryable, except when the provider refuses it again right after a context compaction, or refuses even
      the smallest compaction request (``details.reason`` is ``"after_compaction"`` or
      ``"minimal_summary_request"``).
    - ``"completion_billing_denied"``: billing refused the request, for example because the budget is spent.
      Not retryable.
    - ``"completion_failed"``: the model call failed without an HTTP status, for example a lost connection or
      a stream that ended early. Retryable.
    - ``"completion_failed_permanently"``: the model call failed without an HTTP status and a retry will not
      help, for example a reply that reports no token usage: an OpenAI-compatible server must support
      ``stream_options.include_usage``. Not retryable.
    - ``"remote_session_failed"``: a served or deployed session failed or reached its time limit. The session
      has ended: start a new one.
    - ``"capability_execution_failed"``: a hook other than ``pre_tool_call`` or ``post_tool_call`` raised an
      exception, or its saved state was too large. The message ends with the exception's text. Not retryable.
    - ``"tool_raised"``: a tool raised an exception other than ``agents.ToolError`` on an agent with
      ``tool_errors="raise"``. The message names the tool and the exception's type. Not retryable.
    - ``"tool_output_schema_mismatch"``: a tool's result did not match its ``output_schema=`` on an agent with
      ``tool_errors="raise"``. Not retryable.
    - ``"invalid_compaction_summary"``: a context compaction failed: the model's summary was empty, had
      malformed ``<summary>`` delimiters, called tools, or reached the output token limit. Not retryable.
    - ``"compaction_request_too_large"``: a context compaction could not start, because the context it must
      send does not fit under the compaction threshold. Not retryable.
    - ``"compaction_replacement_too_large"``: the summary and the context the turn needs do not fit under the
      compaction threshold. Not retryable.
    - ``"turn_failed"``: a served agent's error that has no code of its own.
    """

    message: str
    """What went wrong."""
    code: str | None = None
    """The error's code, such as ``"completion_rate_limited"``, or ``None`` when it has none."""
    retryable: bool = False
    """``True`` when sending the same request again may succeed, for example after a model stream timeout."""
    details: dict[str, JsonValue] | None = None
    """The structured data that came with the error, such as
    ``{"reason": "invalid_request_error", "status_code": 422}`` from the model provider, or ``None`` when
    none came (data that is not a JSON object is left out)."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Failed(_TurnRecord):
    """The turn ended with an error, for example a refusal from the model provider."""

    __match_args__ = ("error",)

    error: ProtocolError
    """Why the turn failed, a ``ProtocolError``."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownOutcome(_TurnRecord):
    """The turn ended with an outcome added after your SDK version, such as ``"future_outcome"``.

    Leave a ``case`` for this record, so your code still runs when outcomes are added.
    """

    __match_args__ = ("outcome", "raw")

    outcome: str
    """The outcome, such as ``"future_outcome"``."""
    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)
    """The turn's termination, unparsed."""


type TurnState[T] = Running | Blocked | Completed[T] | Interrupted | Failed | UnknownOutcome
"""A turn's state as of ``cursor``: one of the six records ``Running``, ``Blocked``, ``Completed``,
``Interrupted``, ``Failed`` and ``UnknownOutcome``."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Busy:
    """A new turn was not started, because another turn of the session is active.

    This is not a turn state: no turn was started.
    """

    session_id: str
    """The ID of the session."""
    active_turn_id: str
    """The ID of the turn that is active."""
    turn: Turn = field(compare=False)
    """The active turn's handle, to steer, interrupt or wait for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TurnConflict:
    """A request named a turn that is no longer the session's active turn. Nothing was applied: the session
    refused the request."""

    session_id: str
    """The ID of the session."""
    expected_turn_id: str
    """The ID of the turn that the request named."""
    active_turn_id: str | None
    """The ID of the turn that is active now, or ``None`` when no turn is."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Answered:
    """The callback was open when read, and it was answered."""

    session_id: str
    """The ID of the session."""
    callback_id: str
    """The ID of the callback."""
    answer: AllowApproval | DenyApproval | None = None
    """The approval answer that counted. It is another client's when that client answered first, so compare it
    with yours to tell. It is ``None`` for a client tool call or a sign-in, or when the answer that counted
    could not be read in time or is of a kind added after your SDK version; read the turn to see the outcome."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlreadySettled:
    """An answer named a callback that is no longer open: it was answered, or it closed. Nothing changed.

    Another client may have answered first, the callback's turn ended, or the session ended.
    """

    session_id: str
    """The ID of the session."""
    callback_id: str
    """The ID of the callback."""


@dataclass(frozen=True, slots=True, kw_only=True)
class NotFound:
    """An answer named a callback that the session never opened, and that none of its subagents
    has open. Nothing changed.

    Once a subagent's callback is no longer open, its root says ``NotFound``. The subagent's own
    session says ``AlreadySettled``.
    """

    session_id: str
    """The ID of the session."""
    callback_id: str
    """The ID of the callback."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CompletedTermination:
    """The session completed."""

    __match_args__ = ("stop_reason",)

    stop_reason: Literal["iteration_limit", "skipped", "rejected", "output_limit"] | UnknownValue | None = None
    """``"iteration_limit"`` when it reached its iteration limit, ``"skipped"`` when a hook skipped its work,
    ``"rejected"`` when a ``post_llm_call`` hook rejected the reply, ``"output_limit"`` when the model's last
    reply stopped at the output token limit, ``None`` when it ended normally, and an :class:`UnknownValue` for a
    stop reason added after your SDK version. Always ``None`` in a deployed session's record: read the reason in the
    turn's ``Completed.stop_reason``."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CancelledTermination:
    """The session was cancelled."""

    __match_args__ = ("cause",)

    cause: str | None = None
    """``"lifetime_limit"`` or ``"idle_limit"`` when it reached one of its limits, ``None`` when a client
    cancelled it, or a cause added after your SDK version."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class FailedTermination:
    """The session failed."""

    __match_args__ = ("error",)

    error: ProtocolError
    """The error the session ended with, a ``ProtocolError``."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownTermination:
    """The session ended with an outcome added after your SDK version, such as ``"future_outcome"``.

    Leave a ``case`` for this record, so your code still runs when outcomes are added.
    """

    __match_args__ = ("outcome", "raw")

    outcome: str
    """The outcome, such as ``"future_outcome"``."""
    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)
    """The termination, unparsed."""


type Termination = CompletedTermination | CancelledTermination | FailedTermination | UnknownTermination
"""How a session ended: one class for each outcome, and ``UnknownTermination`` for an outcome added
after your SDK version."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionInfo:
    """One session found in a listing. The times are in UTC."""

    id: str
    """The session's ID."""
    parent_id: str | None
    """The parent session of a subagent, or ``None`` for a root session."""
    root_id: str
    """The root session of its tree, its own ``id`` for a root."""
    title: str | None
    """The session's title, or ``None`` when it has none yet."""
    status: Literal["running", "waiting", "terminated"] | UnknownValue
    """``"running"`` while a turn is active, ``"waiting"`` when no turn is, ``"terminated"`` once the session has
    ended, or an :class:`UnknownValue` for a status added after your SDK version, such as ``"paused"``."""
    created_at: datetime
    """When the session was created."""
    updated_at: datetime
    """When the session last changed."""
    archived_at: datetime | None
    """When the session was archived. A listing gives unarchived sessions only, so it is ``None`` in every listed
    record."""
    termination: Termination | None
    """How the session ended, or ``None`` until it has."""
