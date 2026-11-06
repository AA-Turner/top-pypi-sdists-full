"""Public-facing errors for the Agents SDK Unified Harness backend.

``AgentsError`` is the base of every error the SDK raises from a session or turn call. Each class
keeps the builtin base it had, so an older ``except LookupError`` or ``except RuntimeError`` still
matches. HTTP, connection and Harness errors reach the caller as an ``AgentsError`` that is still an
instance of its httpx or Harness class: see ``as_agents_error``.
"""

import contextlib
import functools
import warnings
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable, Coroutine
from typing import TYPE_CHECKING, Any, cast

import httpx

from mistralai.vibe.harness.app_server import session as _harness_session
from mistralai.vibe.harness.app_server.session import SessionEventStreamLostError
from mistralai.vibe.harness.runtime.capabilities.plugins import mistral_connectors as _harness_connectors
from mistralai.vibe.harness.runtime.errors import ToolNameCollisionError


class AgentsError(Exception):
    """The base of the errors the SDK raises.

    ``except agents.AgentsError`` catches a failed session or turn call for local and deployed sessions, including an
    HTTP error (``APIStatusError``), a connection error (``APIConnectionError``) or an error the
    session reported, such as ``SessionBusyError``. Argument errors stay ``ValueError`` or
    ``TypeError``, and a cancelled call raises ``asyncio.CancelledError``.
    """

    def __reduce__(self) -> tuple[Any, ...]:
        # Rebuild from the arguments and attributes: each class's ``__init__`` takes other arguments,
        # and a class ``as_agents_error`` made is found by the pair of classes it joins, not by name.
        cls = type(self)
        return (_rebuild, (_WRAPPED_PAIRS.get(cls, cls), self.args, self.__dict__))


class SdkError(AgentsError, ValueError):
    """A call the SDK refuses, such as one with a wrong argument value or one on a local runtime that has
    closed."""


class InvalidCursorError(SdkError):
    """``after=`` is not a position of the session it reads.

    The cursor is not one the session gave, or it is a cursor or a record of another session. A
    record or a cursor of another session raises before any read, on ``iter_events()`` too. A cursor
    the session never gave raises when the session reads it: at the first iteration of
    ``iter_events()``, or while the turn runs for ``result()``. ``cursor`` is the cursor passed, a
    record's ``cursor`` for a record. A cursor saved by SDK 1.0 is accepted; the error shows it with
    this session's ID.

    A program that stores cursors can catch it and read again without one::

        try:
            state = await turn.result(after=stored_cursor)
        except agents.InvalidCursorError:
            state = await turn.result()
    """

    def __init__(self, message: str, *, cursor: str | None) -> None:
        super().__init__(message)
        self.cursor = cursor
        """The cursor passed, or a record's ``cursor`` for a record."""


def invalid_cursor(
    cursor: str, session_id: object, *, owner: str | None = None, host_class: type[Exception] | None = None
) -> InvalidCursorError:
    """The ``InvalidCursorError`` both hosts raise for ``cursor`` passed to ``session_id``'s read.

    ``owner`` is the other session the cursor names, if any. ``host_class`` is the class the host
    raised before, which the error stays an instance of, so an ``except`` on it still catches it.
    """
    reason = (
        f"is not an event cursor of session {session_id}"
        if owner is None
        else f"is a cursor of session {owner}, not of {session_id}"
    )
    cls = InvalidCursorError
    if host_class is not None:
        cls = cast(type[InvalidCursorError], _wrapped_class(InvalidCursorError, host_class))
    return cls(f"after={cursor!r} {reason}: pass a cursor this session gave, or after=None", cursor=cursor)


class UnsupportedAgentFeatureError(SdkError, RuntimeError):
    """Where the agent runs does not support this Agents SDK feature."""

    def __init__(self, feature: str, reason: str) -> None:
        self.feature = feature
        """The feature that is not supported."""
        self.reason = reason
        """Why it is not supported."""
        super().__init__(f"Unsupported Agents SDK feature {feature!r}: {reason}")


class LegacySessionError(UnsupportedAgentFeatureError):
    """This session was created by an older version of the platform, and this SDK cannot open it.

    Every session that ``agents.Agent`` starts can be opened. This SDK cannot read, follow or send
    to an older one: start a new session.
    """

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        """The ID of the session."""
        self.feature = "legacy task protocol"
        """Always ``"legacy task protocol"``, the value that marks a session an older version of the platform
        created."""
        self.reason = "this SDK reads Session v1 Sessions only"
        """Why this SDK cannot open the session."""
        # Not `super().__init__`: the base class builds a message for a feature of an Agent, not of a Session.
        AgentsError.__init__(
            self,
            f"Session {session_id} uses the legacy task protocol. This SDK reads Session v1 sessions only. "
            "Start a new session.",
        )


class SessionNotFoundError(AgentsError, LookupError):
    """A call named a session that does not exist, or that you cannot read.

    For a deployed agent, either no session has this ID, or the API key in use belongs to a
    workspace that cannot read it. For a local session, no session with this ID ran in this
    process, or an ``agents.local_runtime()`` block freed it and the event loop no longer remembers
    it: each loop remembers the newest 10,000. In both cases, ``scope="tree"`` of ``list_sessions``
    also raises it for a subagent as the root.
    """

    def __init__(self, session_id: str, detail: str | None = None) -> None:
        self.session_id = session_id
        """The ID the call named."""
        super().__init__(self._message(session_id, detail))

    @staticmethod
    def _message(session_id: str, detail: str | None) -> str:
        message = f"Session {session_id} was not found; check the ID and that your API key can read it"
        return f"{message} ({detail})" if detail else message


class _LocalSessionNotFoundError(SessionNotFoundError):
    """``SessionNotFoundError`` on the local host, whose sessions no API key reads: its text has no key hint.

    It shows as ``SessionNotFoundError``, and pickles back to this class.
    """

    def __init__(self, session_id: str, detail: str) -> None:
        self.detail = detail
        super().__init__(session_id, detail)

    @staticmethod
    def _message(session_id: str, detail: str | None) -> str:
        return f"Session {session_id} was not found: {detail}"

    def __reduce__(self) -> tuple[Callable[[str, str], SessionNotFoundError], tuple[str, str]]:
        return local_session_not_found, (self.session_id, self.detail)


_LocalSessionNotFoundError.__name__ = _LocalSessionNotFoundError.__qualname__ = SessionNotFoundError.__name__


def local_session_not_found(session_id: str, detail: str) -> SessionNotFoundError:
    """``SessionNotFoundError`` for the local host, whose sessions no API key reads."""
    return _LocalSessionNotFoundError(session_id, detail)


class SessionBusyError(AgentsError, _harness_session.SessionBusyError):
    """The session cannot take the message now, and nothing was applied.

    It is raised after the request was retried for a while. Retry the same request later.
    """

    retry_after: float | None = None
    """Seconds to wait before you retry, when the server said; else ``None``."""


class SessionIdempotencyConflictError(AgentsError, _harness_session.SessionIdempotencyConflictError):
    """An idempotency key was reused for a different request, or the requests cannot be compared.

    They cannot be compared when the first request is too old, or when a local call was cancelled
    after it applied the message but before it recorded the key. In both cases the key's first
    request was applied, so do not send that message again with a new key. This call applied nothing.
    Use a new key for a new request.
    """

    idempotency_key: str
    """The key that was reused."""


class SessionTerminatedError(AgentsError, _harness_session.SessionTerminatedError):
    """The session is closed or has ended, and takes no more calls."""


class UnsupportedSessionProcedureError(AgentsError, _harness_session.UnsupportedSessionProcedureError):
    """Where the session runs does not support this call, and nothing was sent."""

    method: str
    """The call that is not supported."""

    backend: str
    """An internal name for where the session runs, for logs."""

    reason: str
    """Why the call is not supported."""


class MistralConnectorNotFoundError(AgentsError, _harness_connectors.MistralConnectorNotFoundError):
    """A connector name that matches no connector the user who runs the session can see.

    No name in ``connectors=`` raises it: the session starts without that connector and sends an
    ``agents.Notice``, whose ``details["connector"]`` is the name and ``details["reason"]`` names the
    close matches. ``connector_name`` is the name, and ``close_matches`` the names of visible
    connectors close to it.
    """


class SessionInUseError(AgentsError, RuntimeError):
    """Another process has this saved local session open, so this one cannot continue it.

    Saved local sessions (``journal_factory=`` of ``agents.local_runtime()``) take a lock on
    their journal while a process has them open. Retry once the other process has left its
    ``agents.local_runtime()`` block or exited.
    """

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        """The ID of the saved session."""
        super().__init__(f"Session {session_id} is open in another process")


class SessionConfigMismatchError(AgentsError, RuntimeError):
    """The agent that continues a saved local session is not the agent that started it.

    A saved session continues only with the same model, instructions, tools and other settings
    it was saved with. Continue it with that agent, or start a new session.
    """

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        """The ID of the saved session."""
        super().__init__(f"Session {session_id} was saved with a different Agent configuration")


class TurnNotFoundError(AgentsError, LookupError):
    """A turn handle named a turn its session does not have."""

    def __init__(self, session_id: str, turn_id: str) -> None:
        self.session_id = session_id
        """The ID of the session."""
        self.turn_id = turn_id
        """The ID the handle named."""
        super().__init__(f"Session {session_id} has no turn {turn_id}")


class ClientToolAnswerError(AgentsError, RuntimeError):
    """A client tool answer ran, but sending it to the session failed.

    ``callback_id``, ``session_id`` and ``turn_id`` name the call: a subagent's call has the
    subagent's session and turn. The send error is the ``__cause__``. The turn keeps running, and the
    call fails at its callback timeout: the model gets a tool error. To follow the turn, use
    ``agent.session(session_id).turn(turn_id)``.
    """

    def __init__(self, *, callback_id: str, session_id: str, turn_id: str) -> None:
        self.callback_id = callback_id
        """The ID of the client tool call."""
        self.session_id = session_id
        """The ID of the session the call is in: a subagent's for a subagent's call."""
        self.turn_id = turn_id
        """The ID of the turn the call is in."""
        super().__init__(
            f"The answer to client tool call {callback_id} (session {session_id}, turn {turn_id}) could not be sent"
        )


class RemoteAgentDeploymentNotFoundError(AgentsError, RuntimeError):
    """The deployed agent behind this handle no longer exists, for example after a shutdown."""


class OutcomeUnknownError(AgentsError, RuntimeError):
    """The SDK could not confirm in time whether the session started or the request applied.

    ``idempotency_key`` is the key to retry with, including one the SDK generated, or the
    callback ID for a callback answer. It is ``None`` for an operation without a key, and for a
    ``start_turn`` that found another turn running on an agent deployed with an older SDK: that
    key would be refused again. Start again with ``idempotency_key=None``, and the SDK makes a new
    key.
    """

    def __init__(self, message: str, *, idempotency_key: str | None = None) -> None:
        super().__init__(message)
        self.idempotency_key = idempotency_key
        """The key to retry with, or the callback ID for a callback answer. ``None`` when the operation has no
        key, or when retrying with the key would be refused again."""


class SessionStartupTimeoutError(OutcomeUnknownError):
    """The session was created, but it was not ready before the deadline.

    The session is not cancelled. Use ``agent.session(session_id)`` (or
    ``Agent.load_from(agent_name=...).session(session_id)`` elsewhere) to attach again
    without starting another session.
    """

    def __init__(self, session_id: str, timeout_seconds: float) -> None:
        self.session_id = session_id
        """The ID of the created session, to attach again with ``agent.session(session_id)``."""
        self.timeout_seconds = timeout_seconds
        """How long the SDK waited for the session to be ready."""
        super().__init__(
            f"Session {session_id} was created, but readiness was not observed within "
            f"{timeout_seconds:g} seconds; attach again with agent.session({session_id!r}) instead of starting another"
        )


class ObservationLost(AgentsError, RuntimeError):
    """The session's events, or the open callbacks of its subagents, could not be read again after
    the connection was lost, or the events' stream ended.

    Nothing was stopped: the session keeps running. ``cursor`` is the position up to which the events were given,
    or ``None`` when none was; continue reading after it: no event is missed.
    """

    def __init__(self, session_id: str, cursor: str | None) -> None:
        super().__init__(session_id, cursor)
        self.session_id = session_id
        """The ID of the session."""
        self.cursor = cursor
        """The position up to which the events were given, or ``None`` when none was."""

    def __str__(self) -> str:
        return (
            f"Lost the events of session {self.session_id}, or its subagents' callbacks, after cursor "
            f"{self.cursor!r}; the session keeps running"
        )


class RemoteStreamLostError(ObservationLost, SessionEventStreamLostError):
    """A session client lost the event stream of a deployed agent's session and could not reconnect.

    Nothing was interrupted: the session and its active turn may still be running. Call
    ``events()`` on the same client to resume after ``after_event_id`` (also ``cursor``), or
    reattach from anywhere with ``Agent.load_from(agent_name=...).session(session_id)``.
    """

    __str__ = RuntimeError.__str__

    def __init__(self, *, session_id: str, after_event_id: str | None, reason: str) -> None:
        SessionEventStreamLostError.__init__(
            self,
            session_id=session_id,
            after_event_id=after_event_id,
            reason=reason,
            reattach_hint=(
                "call events() on this client to resume after the last received event, or reattach "
                f"with agent.session({session_id!r}) and read its turns or iter_events()"
            ),
        )
        self.cursor = after_event_id


class APIStatusError(AgentsError, httpx.HTTPStatusError):
    """Mistral answered an HTTP request with an error status."""

    response: httpx.Response
    """The HTTP response, with its status, headers and body."""

    @property
    def status_code(self) -> int:
        """The HTTP status of the response."""
        return self.response.status_code


class AuthenticationError(APIStatusError):
    """Mistral refused the API key: HTTP 401."""


class PermissionDeniedError(APIStatusError):
    """The API key may not do this: HTTP 403."""


def retry_after_seconds(response: httpx.Response) -> float | None:
    """The response's ``Retry-After`` in seconds, or None when it has none or names a date."""

    value = response.headers.get("Retry-After", "")
    if value.isascii() and value.isdigit():
        return float(value)
    return None


class RateLimitError(APIStatusError):
    """Too many requests: HTTP 429. The same request may succeed later.

    ``retry_after`` is the wait in seconds the server named, or None when it named none, for example
    for a concurrent session limit. A session start already waits out a ``Retry-After`` that ends
    within 30 seconds of the start before it raises this error.
    """

    @property
    def retry_after(self) -> float | None:
        """Seconds to wait before you retry, when the server said; else ``None``."""
        return retry_after_seconds(self.response)


class InternalServerError(APIStatusError):
    """Mistral failed: HTTP 500 or above."""


class APIConnectionError(AgentsError, httpx.TransportError):
    """An HTTP request got no answer: the connection failed, or the network dropped it.

    It is also an instance of the httpx class that failed, such as ``httpx.ConnectError``. It is
    not a builtin ``ConnectionError``.
    """


class APITimeoutError(APIConnectionError, httpx.TimeoutException):
    """An HTTP request timed out. It is not a builtin ``TimeoutError``."""


_STATUS_ERRORS: dict[int, type[APIStatusError]] = {
    401: AuthenticationError,
    403: PermissionDeniedError,
    429: RateLimitError,
}

# Errors of these packages that reach a public call are re-raised as an ``AgentsError`` of the same class:
# httpx, the Mistral client (an in-process session reads skills from the AI Registry with it) and the Harness.
_WRAPPED_PACKAGES = ("httpx", "mistralai.client", "mistralai.vibe", "mistralai.vibe_agents")


def as_agents_error(error: Exception) -> Exception:
    """Return ``error`` as an ``AgentsError`` that is still an instance of its own class.

    An ``AgentsError`` is returned as it is. An httpx status error becomes an ``APIStatusError``
    (``AuthenticationError`` for 401, and so on), an httpx timeout an ``APITimeoutError``, another
    httpx transport error an ``APIConnectionError``. The Harness's ``SessionBusyError``,
    ``SessionIdempotencyConflictError``, ``SessionTerminatedError``,
    ``UnsupportedSessionProcedureError`` and ``MistralConnectorNotFoundError`` become the classes of
    the same names here, and its ``ToolNameCollisionError``, raised when two tools of a Session's
    capabilities take one name, and its ``SessionCallbackRejectedError``, raised for a callback
    answer the Session refuses, an ``SdkError``. Any other error of httpx, the
    Mistral client or the Harness becomes an ``AgentsError`` with its own name. The copy has the same
    arguments and attributes. Other errors, such as ``ValueError`` for a bad argument, and errors the
    caller's own code raised (see ``mark_caller_error``) are returned as they are.
    """
    module = type(error).__module__
    if (
        isinstance(error, AgentsError)
        or getattr(error, _CALLER_ERROR, False)
        or not (
            # A subclass of an httpx error, such as one of a custom transport, is classified by its type.
            isinstance(error, httpx.HTTPError)
            or any(module == package or module.startswith(f"{package}.") for package in _WRAPPED_PACKAGES)
        )
    ):
        return error
    public: type[AgentsError] = AgentsError
    if isinstance(error, httpx.HTTPStatusError):
        code = error.response.status_code
        public = _STATUS_ERRORS.get(code, InternalServerError if code >= 500 else APIStatusError)
    elif isinstance(error, httpx.TimeoutException):
        public = APITimeoutError
    elif isinstance(error, httpx.TransportError):
        public = APIConnectionError
    elif isinstance(error, _harness_session.SessionBusyError):
        public = SessionBusyError
    elif isinstance(error, _harness_session.SessionTerminatedError):
        public = SessionTerminatedError
    elif isinstance(error, _harness_session.SessionIdempotencyConflictError):
        public = SessionIdempotencyConflictError
    elif isinstance(error, _harness_session.UnsupportedSessionProcedureError):
        public = UnsupportedSessionProcedureError
    elif isinstance(error, _harness_connectors.MistralConnectorNotFoundError):
        public = MistralConnectorNotFoundError
    elif isinstance(error, (ToolNameCollisionError, _harness_session.SessionCallbackRejectedError)):
        public = SdkError
    return _rebuild((public, type(error)), error.args, error.__dict__)


def sdk_runtime_error(message: str) -> AgentsError:
    """A ``RuntimeError`` the SDK raises itself, also an ``AgentsError``, with the builtin's name.

    For a state the SDK cannot go on from, such as a closed transport, which has no class of its own.
    """
    return _rebuild((AgentsError, RuntimeError), (message,), {})


def described_value(value: object) -> str:
    """``value`` as an error names it: its repr when it is a plain value, else its type."""
    if value is None or isinstance(value, bool | int | float | str | dict | list):
        text = repr(value)
        return text if len(text) <= 80 else f"{type(value).__name__} {text[:77]}..."
    return type(value).__name__


# Set on an error the caller's own code raised, such as an ``on_event`` handler: it is not wrapped.
_CALLER_ERROR = "_agents_caller_error"


def mark_caller_error(error: Exception) -> None:
    """Let an error the caller's own code raised, such as an ``on_event`` handler, reach the caller as it is.

    It never raises: a class that refuses the attribute keeps its error, which is only wrapped if it
    is an httpx or Harness error.
    """
    # ``object.__setattr__`` passes over a class's own ``__setattr__``, such as a frozen dataclass's.
    with contextlib.suppress(Exception):
        object.__setattr__(error, _CALLER_ERROR, True)


def _rebuild(
    cls: type[AgentsError] | tuple[type[AgentsError], type[Exception]], args: tuple[Any, ...], state: dict[str, Any]
) -> AgentsError:
    """An instance of ``cls``, or of the class ``as_agents_error`` makes from a pair, without calling ``__init__``."""
    if isinstance(cls, tuple):
        cls = _wrapped_class(*cls)
    copy = cls.__new__(cls, *args)
    copy.__dict__.update(state)
    return copy


# Harness subclasses of a class this module mirrors that keep their own name when wrapped.
_OWN_NAMES = frozenset({_harness_session.ChildSessionProcedureRefusedError})

_WRAPPED_CLASSES: dict[tuple[type[AgentsError], type[Exception]], type[AgentsError]] = {}
_WRAPPED_PAIRS: dict[type[AgentsError], tuple[type[AgentsError], type[Exception]]] = {}


def _wrapped_class(public: type[AgentsError], original: type[Exception]) -> type[AgentsError]:
    if issubclass(public, original):
        return public
    if (cached := _WRAPPED_CLASSES.get((public, original))) is not None:
        return cached
    # The public class names an HTTP error, or a Harness error's private subclass such as a local session's
    # busy error; any other error keeps the Harness name it was raised with, as does a subagent's refusal, which
    # the docs name.
    named = original if public is AgentsError or original in _OWN_NAMES else public
    wrapped = type(
        named.__name__,
        (public, original),
        {"__module__": named.__module__, "__qualname__": named.__qualname__, "__doc__": named.__doc__},
    )
    wrapped = _WRAPPED_CLASSES.setdefault((public, original), wrapped)
    _WRAPPED_PAIRS[wrapped] = (public, original)
    return wrapped


def public_errors[**P, R](function: Callable[P, Awaitable[R]]) -> Callable[P, Coroutine[Any, Any, R]]:
    """Re-raise the errors of an async SDK call as ``AgentsError`` (see ``as_agents_error``)."""

    @functools.wraps(function)
    async def call(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await function(*args, **kwargs)
        except Exception as error:
            public = as_agents_error(error)
            if public is error:
                raise
            raise public from error

    return call


def public_iter_errors[**P, Y](function: Callable[P, AsyncIterator[Y]]) -> Callable[P, AsyncIterator[Y]]:
    """``public_errors`` for an async generator: what it raises when opened or between items is an ``AgentsError``."""

    @functools.wraps(function)
    async def iterate(*args: P.args, **kwargs: P.kwargs) -> AsyncIterator[Y]:
        items: AsyncIterator[Y] | None = None
        try:
            items = function(*args, **kwargs)
            async for item in items:
                yield item
        except Exception as error:
            public = as_agents_error(error)
            if public is error:
                raise
            raise public from error
        finally:
            if isinstance(items, AsyncGenerator):
                await items.aclose()

    return iterate


if TYPE_CHECKING:
    # The 1.1.0rc12 names are plain aliases for type checkers, which report nothing, so rc12 code
    # type-checks as it is. At runtime `__getattr__` returns the same classes with a `DeprecationWarning`.
    RemoteSessionNotFoundError = SessionNotFoundError
    RemoteSessionOutcomeUnknownError = OutcomeUnknownError
    RemoteSessionStartupTimeoutError = SessionStartupTimeoutError
    RemoteSessionStreamLostError = RemoteStreamLostError


_RENAMED = {
    "RemoteSessionNotFoundError": "SessionNotFoundError",
    "RemoteSessionOutcomeUnknownError": "OutcomeUnknownError",
    "RemoteSessionStartupTimeoutError": "SessionStartupTimeoutError",
    "RemoteSessionStreamLostError": "ObservationLost",
}


def _renamed_warning(name: str) -> str:
    return f"agents.{name} is deprecated: use agents.{_RENAMED[name]}"


def _renamed_class(name: str) -> type[AgentsError]:
    # rc12 code builds and catches RemoteSessionStreamLostError with its keyword constructor, so the old
    # name stays the class the Session client raises, an ObservationLost, rather than ObservationLost itself.
    if name == "RemoteSessionStreamLostError":
        return RemoteStreamLostError
    renamed: type[AgentsError] = globals()[_RENAMED[name]]
    return renamed


def __getattr__(name: str) -> object:
    if name in _RENAMED:
        warnings.warn(_renamed_warning(name), DeprecationWarning, stacklevel=2)
        return _renamed_class(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "ClientToolAnswerError",
    "APIConnectionError",
    "APIStatusError",
    "APITimeoutError",
    "AgentsError",
    "AuthenticationError",
    "InternalServerError",
    "InvalidCursorError",
    "LegacySessionError",
    "MistralConnectorNotFoundError",
    "ObservationLost",
    "OutcomeUnknownError",
    "PermissionDeniedError",
    "RateLimitError",
    "RemoteAgentDeploymentNotFoundError",
    "SdkError",
    "SessionBusyError",
    "SessionConfigMismatchError",
    "SessionIdempotencyConflictError",
    "SessionInUseError",
    "SessionNotFoundError",
    "SessionStartupTimeoutError",
    "SessionTerminatedError",
    "TurnNotFoundError",
    "UnsupportedAgentFeatureError",
    "UnsupportedSessionProcedureError",
]
