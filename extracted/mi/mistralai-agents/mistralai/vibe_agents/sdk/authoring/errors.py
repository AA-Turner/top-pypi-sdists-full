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
from typing import TYPE_CHECKING, Any

import httpx

from mistralai.vibe.harness.app_server import session as _harness_session
from mistralai.vibe.harness.app_server.session import SessionEventStreamLostError


class AgentsError(Exception):
    """The base of the errors the Agents SDK raises.

    ``except agents.AgentsError`` catches a failed session or turn call on both hosts, including an
    HTTP error (``APIStatusError``), a connection error (``APIConnectionError``) or an error the
    Harness reported, such as ``SessionBusyError``. Argument errors stay ``ValueError`` or
    ``TypeError``, and a cancelled call raises ``asyncio.CancelledError``.
    """

    def __reduce__(self) -> tuple[Any, ...]:
        # Rebuild from the arguments and attributes: each class's ``__init__`` takes other arguments,
        # and a class ``as_agents_error`` made is found by the pair of classes it joins, not by name.
        cls = type(self)
        return (_rebuild, (_WRAPPED_PAIRS.get(cls, cls), self.args, self.__dict__))


class SdkError(AgentsError, ValueError):
    """Raised when an Agents SDK operation is invalid."""


class UnsupportedAgentFeatureError(SdkError, RuntimeError):
    """An Agents SDK feature has no implementation in the selected backend."""

    def __init__(self, feature: str, reason: str) -> None:
        self.feature = feature
        self.reason = reason
        super().__init__(f"Unsupported Agents SDK feature {feature!r}: {reason}")


class SessionNotFoundError(AgentsError, LookupError):
    """A call named a session its host does not know.

    On a deployment, either no session has this ID, or the API key in use belongs to a
    workspace that cannot read it. On the local host, no session with this ID ran in this process.
    """

    def __init__(self, session_id: str, detail: str | None = None) -> None:
        self.session_id = session_id
        message = f"Session {session_id} was not found; check the ID and that your API key can read it"
        super().__init__(f"{message} ({detail})" if detail else message)


class SessionBusyError(AgentsError, _harness_session.SessionBusyError):
    """The session cannot take the message yet, and nothing was applied.

    Each host retries for a bounded time before it raises this error: retry the same request later.
    It is still the Harness's ``SessionBusyError``, so an ``except`` on that class catches it.
    """


class SessionTerminatedError(AgentsError, _harness_session.SessionTerminatedError):
    """The session is closed or has ended, and takes no more calls.

    It is still the Harness's ``SessionTerminatedError``, so an ``except`` on that class catches it.
    """


class LocalSessionNotFoundError(AgentsError, LookupError):
    """A local listing named, as ``root=`` or ``parent=``, a Session this event loop's local runtime
    does not have."""

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        super().__init__(f"Session {session_id} is not a session of this event loop's local runtime")


class SessionInUseError(AgentsError, RuntimeError):
    """Another process has this saved local Session open, so this one cannot continue it.

    Saved local Sessions (``journal_factory=`` of ``agents.local_runtime()``) take a lock on
    their journal while a process has them open. Retry once the other process has left its
    ``agents.local_runtime()`` block or exited.
    """

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        super().__init__(f"Session {session_id} is open in another process")


class SessionConfigMismatchError(AgentsError, RuntimeError):
    """The Agent that continues a saved local Session is not the Agent that started it.

    A saved Session continues only with the same model, instructions, tools and other settings
    it was saved with. Continue it with that Agent, or start a new Session.
    """

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        super().__init__(f"Session {session_id} was saved with a different Agent configuration")


class TurnNotFoundError(AgentsError, LookupError):
    """A turn handle named a turn its Session does not have."""

    def __init__(self, session_id: str, turn_id: str) -> None:
        self.session_id = session_id
        self.turn_id = turn_id
        super().__init__(f"Session {session_id} has no turn {turn_id}")


class ClientToolAnswerError(AgentsError, RuntimeError):
    """A client tool answer ran, but sending it to the session failed.

    ``callback_id``, ``session_id`` and ``turn_id`` name the call: a subagent's call has the
    subagent's session and turn. The send error is the ``__cause__``. The turn goes on, and its host
    fails the call at its callback timeout: the model gets a tool error. To follow the turn, use
    ``agent.session(session_id).turn(turn_id)``.
    """

    def __init__(self, *, callback_id: str, session_id: str, turn_id: str | None) -> None:
        self.callback_id = callback_id
        self.session_id = session_id
        self.turn_id = turn_id
        super().__init__(
            f"The answer to client tool call {callback_id} (session {session_id}, turn {turn_id}) could not be sent"
        )


class RemoteAgentDeploymentNotFoundError(AgentsError, RuntimeError):
    """Raised when the Agent Deployment behind a handle no longer exists.

    The usual cause is a shutdown: the agent id stays a valid UUID, but the control
    plane stops resolving it. Without this the caller sees a bare transport 404 from
    the name lookup and cannot tell a gone agent from a broken request.
    """


class OutcomeUnknownError(AgentsError, RuntimeError):
    """The SDK did not observe retained Session readiness or a command outcome in time.

    ``idempotency_key`` is the key to retry with, including one the SDK generated, or the
    callback id for a callback answer. It is ``None`` for an operation without a key, and
    for a start refused without a report while another Turn ran (an agent deployed with an
    older Agents SDK, or a control plane that does not report the refusal): that key would
    be refused again, so start again with a new key. Passing ``None`` as
    ``idempotency_key`` does that.
    """

    def __init__(self, message: str, *, idempotency_key: str | None = None) -> None:
        super().__init__(message)
        self.idempotency_key = idempotency_key


class SessionStartupTimeoutError(OutcomeUnknownError):
    """Creation returned a Session ID, but readiness was not observed before the deadline.

    The remote Session is not cancelled. Use ``agent.session(session_id)`` (or
    ``Agent.load_from(agent_name=...).session(session_id)`` elsewhere) to attach again
    without creating a replacement Session.
    """

    def __init__(self, session_id: str, timeout_seconds: float) -> None:
        self.session_id = session_id
        self.timeout_seconds = timeout_seconds
        super().__init__(
            f"Session {session_id} was created, but readiness was not observed within "
            f"{timeout_seconds:g} seconds; attach again with agent.session({session_id!r}) instead of starting another"
        )


class ObservationLost(AgentsError, RuntimeError):
    """The session's events, or the open callbacks of its subagents, could not be read again after
    the connection was lost, or the events' stream ended.

    Nothing was stopped on the host. ``cursor`` is the position up to which the events were given,
    or ``None`` when none was; continue reading after it: no event is missed.
    """

    def __init__(self, session_id: str, cursor: str | None) -> None:
        super().__init__(session_id, cursor)
        self.session_id = session_id
        self.cursor = cursor

    def __str__(self) -> str:
        return (
            f"Lost the events of session {self.session_id}, or its subagents' callbacks, after cursor "
            f"{self.cursor!r}; the session goes on"
        )


class RemoteStreamLostError(ObservationLost, SessionEventStreamLostError):
    """A Session client lost a deployment-backed Session's event stream and could not reconnect.

    Nothing was interrupted: the Session and its active Turn may still be running. Call
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
    """The control plane answered an HTTP request with an error status.

    ``status_code`` is the status, and ``response`` the response. It is an ``httpx.HTTPStatusError``.
    """

    @property
    def status_code(self) -> int:
        return self.response.status_code


class AuthenticationError(APIStatusError):
    """The control plane refused the API key: HTTP 401."""


class PermissionDeniedError(APIStatusError):
    """The API key may not do this: HTTP 403."""


class RateLimitError(APIStatusError):
    """Too many requests: HTTP 429. The same request may succeed later."""


class InternalServerError(APIStatusError):
    """The control plane failed: HTTP 500 or above."""


class APIConnectionError(AgentsError, httpx.TransportError):
    """An HTTP request got no answer: the connection failed, or the network dropped it.

    It is an ``httpx.TransportError``, and an instance of the httpx class that failed, such as
    ``httpx.ConnectError``. It is not a builtin ``ConnectionError``.
    """


class APITimeoutError(APIConnectionError, httpx.TimeoutException):
    """An HTTP request timed out. It is an ``httpx.TimeoutException``, not a builtin ``TimeoutError``."""


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
    httpx transport error an ``APIConnectionError``. The Harness's ``SessionBusyError`` and
    ``SessionTerminatedError`` become the classes of the same names here. Any other error of httpx, the
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
    return _rebuild((public, type(error)), error.args, error.__dict__)


def sdk_runtime_error(message: str) -> AgentsError:
    """A ``RuntimeError`` the SDK raises itself, also an ``AgentsError``, with the builtin's name.

    For a state the SDK cannot go on from, such as a closed transport, which has no class of its own.
    """
    return _rebuild((AgentsError, RuntimeError), (message,), {})


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


_WRAPPED_CLASSES: dict[tuple[type[AgentsError], type[Exception]], type[AgentsError]] = {}
_WRAPPED_PAIRS: dict[type[AgentsError], tuple[type[AgentsError], type[Exception]]] = {}


def _wrapped_class(public: type[AgentsError], original: type[Exception]) -> type[AgentsError]:
    if issubclass(public, original):
        return public
    if (cached := _WRAPPED_CLASSES.get((public, original))) is not None:
        return cached
    # The public class names an HTTP error; any other keeps the Harness name it was raised with.
    named = public if public is not AgentsError else original
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
    "LocalSessionNotFoundError",
    "ObservationLost",
    "OutcomeUnknownError",
    "PermissionDeniedError",
    "RateLimitError",
    "RemoteAgentDeploymentNotFoundError",
    "SdkError",
    "SessionBusyError",
    "SessionConfigMismatchError",
    "SessionInUseError",
    "SessionNotFoundError",
    "SessionStartupTimeoutError",
    "SessionTerminatedError",
    "TurnNotFoundError",
    "UnsupportedAgentFeatureError",
]
