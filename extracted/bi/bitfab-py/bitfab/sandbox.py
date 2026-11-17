from __future__ import annotations

import copy
import datetime
import json
import sys
import threading
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from bitfab.constants import _replay_context
from bitfab.mock_override import MockOverrideCtx, SpanNodeMeta

SANDBOX_SESSION_KEY = "sandbox_session"
SANDBOX_REPORT_CONTEXT_KEY = "__bitfabSandbox"
SANDBOX_FIXTURE_PREFIX = "sandbox:"


@dataclass(frozen=True)
class RecordedSpan:
    """One span from the original trace, as ``SandboxStartCtx.recorded_spans`` returns it.

    Attributes:
        span_name: The span's name in the original trace.
        trace_function_key: Its trace function key, or ``None`` for a span an
            integration recorded without one.
        input: The recorded input.
        output: The recorded output.
    """

    span_name: str
    trace_function_key: str | None
    input: Any
    output: Any


@dataclass(frozen=True)
class SandboxStartCtx:
    """What a sandbox's ``start`` receives when one replay item first calls it.

    Attributes:
        name: The sandbox's name.
        original_trace_id: The trace being replayed.
        trace_started_at: When the original trace started (ISO 8601), or
            ``None`` when it is not known.
        attempt: The replay attempt for this item, starting at 0.
        recorded_state: The state recorded for this sandbox on the original
            trace with ``get_current_trace().record_sandbox_state``, or
            ``None`` when nothing was recorded.
    """

    name: str
    original_trace_id: str | None
    trace_started_at: str | None
    attempt: int
    recorded_state: Any
    load_recorded_spans: Callable[[str | None], list[RecordedSpan]] = field(repr=False)

    def recorded_spans(self, name: str | None = None) -> list[RecordedSpan]:
        """Spans of the original trace, in the order they started.

        Args:
            name: Only spans with this span name. ``None`` returns every span
                below the root, which downloads each one, so pass a name
                when you can.

        Each span is downloaded from Bitfab the first time any sandbox in the
        item asks for it, then reused.
        """
        return self.load_recorded_spans(name)


@dataclass(frozen=True)
class Sandbox:
    """A stand-in for one outside service that answers its calls during replay.

    Unlike a mock, a sandbox keeps state for the length of one replay item, so
    a write followed by a read sees the write.

    Args:
        name: The service it stands in for, such as ``"Gmail"`` or
            ``"Payments"``. Shown on every call it answers.
        match: Chooses the calls it answers, from the same span metadata a
            mock override's ``match`` receives.
        handle: ``handle(state, call)`` answers one call and may change
            ``state``. ``call`` carries the call's ``node``, ``inputs`` and
            ``kwargs``. What it returns is the call's result.
        start: ``start(ctx)`` builds the starting state for one replay item,
            before its first matched call. ``None`` starts from the state the
            original trace recorded for this sandbox, or ``{}``. Change the
            state here to replay a different scenario. The state must be
            JSON.
        integration: The ``Bitfab(integrations=...)`` name that covers this
            service's data, such as ``"gmail"``. While the client has it off,
            the replay trace shows how many calls the sandbox answered but
            not its state. ``None`` (default) always shows the state.
    """

    name: str
    match: Callable[[SpanNodeMeta], bool]
    handle: Callable[[Any, MockOverrideCtx], Any]
    start: Callable[[SandboxStartCtx], Any] | None = None
    integration: str | None = None


def _ensure_json(name: str, state: Any) -> None:
    try:
        json.dumps(state)
    except (TypeError, ValueError) as error:
        raise TypeError(
            f"The {name} sandbox's state must be JSON ({error}); return dicts, "
            "lists, strings, numbers, booleans and None from start."
        ) from error


def recorded_state(start_ctx: SandboxStartCtx) -> Any:
    return {} if start_ctx.recorded_state is None else start_ctx.recorded_state


@dataclass
class SandboxSession:
    sandboxes: Sequence[Sandbox]
    client: Any
    make_start_ctx: Callable[[Sandbox], SandboxStartCtx]
    trace_started_at: str | None = None
    started: float = field(default_factory=time.monotonic)
    _states: dict[str, Any] = field(default_factory=dict)
    _reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    _lock: threading.RLock = field(default_factory=threading.RLock)

    def elapsed_ms(self) -> int:
        return int((time.monotonic() - self.started) * 1000)

    def find(self, node: SpanNodeMeta) -> Sandbox | None:
        return next(
            (sandbox for sandbox in self.sandboxes if sandbox.match(node)), None
        )

    def has(self, name: str) -> bool:
        return any(sandbox.name == name for sandbox in self.sandboxes)

    def answer(
        self,
        sandbox: Sandbox,
        call: MockOverrideCtx,
        attach_report: Callable[[dict[str, Any]], None],
    ) -> Any:
        with self._lock:
            state = self._state_for(sandbox, attach_report)
            result = sandbox.handle(state, call)
            self._reports[sandbox.name]["calls"] += 1
            return result

    def find_named(self, name: str) -> Sandbox | None:
        return next(
            (
                sandbox
                for sandbox in self.sandboxes
                if sandbox.name == name and sandbox.match is not _never
            ),
            None,
        )

    def state_of(
        self, sandbox: Sandbox, attach_report: Callable[[dict[str, Any]], None]
    ) -> Any:
        with self._lock:
            return self._state_for(sandbox, attach_report)

    def _state_for(
        self, sandbox: Sandbox, attach_report: Callable[[dict[str, Any]], None]
    ) -> Any:
        if sandbox.name in self._states:
            return self._states[sandbox.name]
        start_ctx = self.make_start_ctx(sandbox)
        state = (sandbox.start or recorded_state)(start_ctx)
        _ensure_json(sandbox.name, state)
        self._states[sandbox.name] = state
        report: dict[str, Any] = {
            "name": sandbox.name,
            "traceStartedAt": start_ctx.trace_started_at,
            "calls": 0,
        }
        if sandbox.integration in getattr(self.client, "_disabled_integrations", ()):
            report["stateWithheldBecauseOff"] = sandbox.integration
        else:
            report["startState"] = copy.deepcopy(state)
            report["endState"] = state
        self._reports[sandbox.name] = report
        attach_report({SANDBOX_REPORT_CONTEXT_KEY: report})
        return state


def _never(_node: SpanNodeMeta) -> bool:
    return False


def _unreachable(_state: Any, _call: MockOverrideCtx) -> Any:
    raise RuntimeError("A sandbox turned off answers no calls.")


def without_sandbox(name: str) -> Sandbox:
    """Turn a built-in sandbox off for a replay, by name.

    Pass it in ``sandboxes``: ``sandboxes=[without_sandbox("Gmail")]``. Calls
    that sandbox would answer then get their recorded output when the replay
    mocks them, and are otherwise refused, never sent to the real service.
    """
    return Sandbox(name=name, match=_never, handle=_unreachable)


def combine_sandboxes(
    chosen: Sequence[Sandbox] | None, defaults: Sequence[Sandbox]
) -> list[Sandbox]:
    explicit = list(chosen or [])
    names = [sandbox.name for sandbox in explicit]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(
            f"sandboxes has more than one sandbox named {', '.join(duplicates)}; "
            "each name answers one service."
        )
    return [
        *explicit,
        *(sandbox for sandbox in defaults if sandbox.name not in names),
    ]


def current_session() -> SandboxSession | None:
    session = (_replay_context.get() or {}).get(SANDBOX_SESSION_KEY)
    return session if isinstance(session, SandboxSession) else None


def _attach_to_replay_root(context: dict[str, Any]) -> None:
    from_client = sys.modules.get("bitfab.client")
    if from_client is not None:
        from_client._attach_to_trace_root(context)


def sandbox_active(name: str) -> bool:
    """Whether the sandbox named ``name`` answers this service's calls right now.

    True only inside a replay item whose replay has that sandbox on, so code
    that refuses to reach a service during its own simulations can let the
    call through to the sandbox instead. False in production and outside a
    replay.
    """
    session = current_session()
    return session is not None and session.find_named(name) is not None


def sandbox_state(name: str) -> Any:
    """The live state of the sandbox named ``name`` in the current replay item.

    Starts the sandbox if no call has reached it yet. Read it to learn what
    the sandbox holds, such as which accounts a Gmail sandbox has mailboxes
    for. Returns ``None`` outside a replay item or when that sandbox is off.
    """
    session = current_session()
    sandbox = session.find_named(name) if session is not None else None
    if session is None or sandbox is None:
        return None
    return session.state_of(sandbox, _attach_to_replay_root)


def sandbox_elapsed_ms() -> int:
    session = current_session()
    return session.elapsed_ms() if session is not None else 0


def parse_timestamp(value: str | None) -> datetime.datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed


def sandbox_now() -> datetime.datetime | None:
    """The time sandboxes use in the current replay item.

    It starts at the moment the original trace started and moves forward as
    the replay item runs, so a sandbox answers as if the run were happening
    again at its original time. Use it in a sandbox's ``handle`` to date what
    the call writes. Returns ``None`` outside a replay item, or when the
    original start time is not known. ``datetime.now()`` is not changed.
    """
    session = current_session()
    started_at = parse_timestamp(session.trace_started_at) if session else None
    if session is None or started_at is None:
        return None
    return started_at + datetime.timedelta(milliseconds=session.elapsed_ms())
