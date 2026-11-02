"""Tests for CopilotSDKTransport."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from agentic_devtools.orchestration.llm.errors import AuthenticationError
from agentic_devtools.orchestration.llm.providers.copilot import CopilotSDKTransport, _StatusError
from agentic_devtools.orchestration.llm.types import LLMMessage


def _messages() -> list[LLMMessage]:
    return [LLMMessage(role="user", content="Review this")]


def test_prompt_formats_role_and_content():
    assert CopilotSDKTransport._prompt(_messages()) == "user: Review this"


def test_prompt_separates_system_message_from_conversation():
    messages = [LLMMessage(role="system", content="Follow these rules"), *_messages()]

    assert CopilotSDKTransport._system_message(messages) == "Follow these rules"
    assert CopilotSDKTransport._prompt(messages) == "user: Review this"


class _FakeAuth:
    def __init__(self, authenticated: bool = True) -> None:
        self.isAuthenticated = authenticated


class _FakeModel:
    def __init__(self, model_id: str) -> None:
        self.id = model_id


class _FakePreflight:
    """Minimal client that exercises preflight paths."""

    def __init__(
        self,
        *,
        auth_error: Exception | None = None,
        authenticated: bool = True,
        list_models_error: Exception | None = None,
        models: list[str] | None = None,
        start_error: Exception | None = None,
        stop_error: Exception | None = None,
    ) -> None:
        self._auth_error = auth_error
        self._authenticated = authenticated
        self._list_models_error = list_models_error
        self._models = models if models is not None else ["gemini-3.7-flash"]
        self._start_error = start_error
        self._stop_error = stop_error
        self.stopped = False

    async def start(self) -> None:
        if self._start_error is not None:
            raise self._start_error

    async def stop(self) -> None:
        self.stopped = True
        if self._stop_error is not None:
            raise self._stop_error

    async def get_auth_status(self) -> Any:
        if self._auth_error:
            raise self._auth_error
        return _FakeAuth(self._authenticated)

    async def list_models(self) -> list[Any]:
        if self._list_models_error:
            raise self._list_models_error
        return [_FakeModel(m) for m in self._models]


class _FakeSession:
    def __init__(self, disconnect_error: Exception | None = None) -> None:
        self._handler = None
        self.disconnected = False
        self.last_timeout: float | None = None
        self.disconnect_error = disconnect_error

    def on(self, handler):
        self._handler = handler

        def _unsubscribe() -> None:
            self._handler = None

        return _unsubscribe

    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="a")
            )
        )
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="b")
            )
        )
        self._handler(
            SimpleNamespace(type=SimpleNamespace(value="assistant.message"), data=SimpleNamespace(content="ab"))
        )
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.idle"), data=SimpleNamespace()))

    async def send_and_wait(self, _prompt: str, timeout: float):
        self.last_timeout = timeout
        return SimpleNamespace(data=SimpleNamespace(content="ok"))

    async def disconnect(self) -> None:
        self.disconnected = True
        if self.disconnect_error is not None:
            raise self.disconnect_error


class _FakeSessionWithUsageEvent(_FakeSession):
    """Session that fires assistant.usage in send_and_wait before returning."""

    async def send_and_wait(self, _prompt: str, timeout: float) -> Any:
        _ = timeout
        if self._handler is not None:
            self._handler(
                SimpleNamespace(
                    type=SimpleNamespace(value="assistant.usage"),
                    data=SimpleNamespace(
                        input_tokens=5,
                        output_tokens=3,
                        total_tokens=8,
                        finish_reason="stop",
                        model="gpt-4o",
                    ),
                )
            )
        return SimpleNamespace(data=SimpleNamespace(content="reply"))


class _FakeSessionWithMultipleUsageEvents(_FakeSession):
    """Session that fires multiple assistant.usage events before returning."""

    async def send_and_wait(self, _prompt: str, timeout: float | None) -> Any:
        _ = timeout
        if self._handler is not None:
            self._handler(
                SimpleNamespace(
                    type=SimpleNamespace(value="assistant.usage"),
                    data=SimpleNamespace(
                        input_tokens=5,
                        output_tokens=3,
                        total_tokens=8,
                        finish_reason="tool_call",
                        model="gpt-4o-mini",
                    ),
                )
            )
            self._handler(
                SimpleNamespace(
                    type=SimpleNamespace(value="assistant.usage"),
                    data=SimpleNamespace(
                        input_tokens=7,
                        output_tokens=4,
                        total_tokens=11,
                        finish_reason="stop",
                        model="gpt-4o",
                    ),
                )
            )
        return SimpleNamespace(data=SimpleNamespace(content="reply"))


class _FakeSessionWithErrorOnComplete(_FakeSession):
    """Session that reports a structured error before send_and_wait fails."""

    async def send_and_wait(self, _prompt: str, timeout: float) -> Any:
        _ = timeout
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="session.error"),
                data=SimpleNamespace(status_code=401),
            )
        )
        raise RuntimeError("SDK dropped the status code")


class _FakeSessionWithGenericCompleteError(_FakeSession):
    """Session that raises an error without a preceding SDK error event."""

    async def send_and_wait(self, _prompt: str, timeout: float) -> Any:
        _ = timeout
        raise RuntimeError("generic SDK failure")


class _FakeSessionTimeout(_FakeSession):
    """Session that raises TimeoutError on send_and_wait."""

    async def send_and_wait(self, _prompt: str, timeout: float):
        _ = timeout
        raise TimeoutError("timed out")


class _FakeSessionNullResponse(_FakeSession):
    """Session that returns None from send_and_wait (server-side timeout sentinel)."""

    async def send_and_wait(self, _prompt: str, timeout: float):
        _ = timeout
        return None


class _FakeSessionNonCallableUnsubscribe(_FakeSession):
    """Session whose on() returns a non-callable, exercising the callable guard."""

    def on(self, handler):
        self._handler = handler
        return None  # not callable


class _FakeSessionWithUsage(_FakeSession):
    """Session that emits an assistant.usage event before the terminal idle."""

    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="hi")
            )
        )
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.usage"),
                data=SimpleNamespace(
                    input_tokens=10,
                    output_tokens=5,
                    total_tokens=15,
                    finish_reason="stop",
                    model="gemini-3.7-flash",
                ),
            )
        )
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.idle"), data=SimpleNamespace()))


class _FakeSessionWithMultipleUsageEventsInStream(_FakeSession):
    """Session that emits multiple assistant.usage events before session.idle."""

    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="hi")
            )
        )
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.usage"),
                data=SimpleNamespace(
                    input_tokens=10,
                    output_tokens=5,
                    total_tokens=15,
                    finish_reason="tool_call",
                    model="gemini-3.7-flash-thinking",
                ),
            )
        )
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.usage"),
                data=SimpleNamespace(
                    input_tokens=3,
                    output_tokens=2,
                    total_tokens=5,
                    finish_reason="stop",
                    model="gemini-3.7-flash",
                ),
            )
        )
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.idle"), data=SimpleNamespace()))


class _FakeSessionWithErrorEvent(_FakeSession):
    """Session that sends an error event during streaming."""

    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="x")
            )
        )
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.error"), data=SimpleNamespace()))


class _FakeSessionWithUnknownEvent(_FakeSession):
    """Session that fires an unknown event name (no-op) then terminates normally."""

    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(SimpleNamespace(type=SimpleNamespace(value="unknown.custom.event"), data=SimpleNamespace()))
        # Complete normally so the stream terminates
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.idle"), data=SimpleNamespace()))


class _FakeSessionSlowSend(_FakeSession):
    """Session whose send call can exceed the configured request timeout."""

    async def send(self, _prompt: str) -> None:
        await asyncio.sleep(2.0)
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="late")
            )
        )
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.idle"), data=SimpleNamespace()))


class _FakeSessionCancelledOnComplete(_FakeSession):
    """Session that is cancelled during send_and_wait."""

    async def send_and_wait(self, _prompt: str, timeout: float | None) -> Any:
        _ = timeout
        raise asyncio.CancelledError


class _FakeSessionWithNonUsageOnComplete(_FakeSession):
    """Session that fires a non-usage event via the usage listener in complete()."""

    async def send_and_wait(self, _prompt: str, timeout: float) -> Any:
        _ = timeout
        if self._handler is not None:
            # Fire a non-usage event — the on_usage handler should ignore it
            self._handler(
                SimpleNamespace(
                    type=SimpleNamespace(value="assistant.some_other_event"),
                    data=SimpleNamespace(),
                )
            )
        return SimpleNamespace(data=SimpleNamespace(content="done"))


class _FakeClient:
    def __init__(
        self,
        session: _FakeSession | None = None,
        create_error: Exception | None = None,
        start_error: Exception | None = None,
        disconnect_error: Exception | None = None,
        stop_error: Exception | None = None,
        start_delay_seconds: float = 0.0,
        create_delay_seconds: float = 0.0,
    ) -> None:
        self.session = session or _FakeSession()
        self.create_error = create_error
        self.start_error = start_error
        self.disconnect_error = disconnect_error
        self.stop_error = stop_error
        self.start_delay_seconds = start_delay_seconds
        self.create_delay_seconds = create_delay_seconds
        self.stopped = False
        self.session_kwargs: dict[str, Any] | None = None

    async def start(self) -> None:
        if self.start_delay_seconds > 0:
            await asyncio.sleep(self.start_delay_seconds)
        if self.start_error is not None:
            raise self.start_error
        return None

    async def create_session(self, **_kwargs):
        if self.create_delay_seconds > 0:
            await asyncio.sleep(self.create_delay_seconds)
        if self.create_error is not None:
            raise self.create_error
        self.session_kwargs = _kwargs
        return self.session

    async def stop(self) -> None:
        self.stopped = True
        if self.stop_error is not None:
            raise self.stop_error


class _FakeSessionNoIdle(_FakeSession):
    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="a")
            )
        )
        self._handler(
            SimpleNamespace(type=SimpleNamespace(value="assistant.message"), data=SimpleNamespace(content="a"))
        )


class _FakeSessionCancelledOnStream(_FakeSession):
    """Session that is cancelled during send()."""

    async def send(self, _prompt: str) -> None:
        raise asyncio.CancelledError


class _FakeSessionAssistantIdleOnly(_FakeSession):
    """Session that emits assistant.idle without completing the session."""

    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="a")
            )
        )
        self._handler(SimpleNamespace(type=SimpleNamespace(value="assistant.idle"), data=SimpleNamespace()))


class _FakeSessionDoubleIdle(_FakeSession):
    async def send(self, _prompt: str) -> None:
        assert self._handler is not None
        self._handler(
            SimpleNamespace(
                type=SimpleNamespace(value="assistant.message_delta"), data=SimpleNamespace(delta_content="a")
            )
        )
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.idle"), data=SimpleNamespace()))
        self._handler(SimpleNamespace(type=SimpleNamespace(value="session.idle"), data=SimpleNamespace()))
        self._handler(SimpleNamespace(type=SimpleNamespace(value="assistant.idle"), data=SimpleNamespace()))


# ---------------------------------------------------------------------------
# preflight tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_preflight_returns_model_set_on_success():
    client = _FakePreflight(models=["gemini-3.7-flash", "gpt-4o"])
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    result = await transport.preflight("gemini-3.7-flash")
    assert result == {"gemini-3.7-flash", "gpt-4o"}
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_stops_client_when_start_fails():
    client = _FakePreflight(start_error=RuntimeError("startup failed"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(RuntimeError, match="startup failed"):
        await transport.preflight("gemini-3.7-flash")

    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_preserves_primary_error_when_stop_fails():
    client = _FakePreflight(
        list_models_error=RuntimeError("inventory unavailable"),
        stop_error=RuntimeError("stop failed"),
    )
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="model inventory is unavailable"):
        await transport.preflight("gemini-3.7-flash")

    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_preserves_cancellation_when_stop_fails():
    client = _FakePreflight(
        auth_error=asyncio.CancelledError(),
        stop_error=RuntimeError("stop failed"),
    )
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(asyncio.CancelledError):
        await transport.preflight("gemini-3.7-flash")

    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_preserves_generic_error_without_session_status():
    session = _FakeSessionWithGenericCompleteError()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(RuntimeError, match="generic SDK failure"):
        await transport.complete(_messages(), model="gemini-3.7-flash")

    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_stops_client_when_disconnect_fails():
    session = _FakeSession(disconnect_error=RuntimeError("disconnect failed"))
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(RuntimeError, match="disconnect failed"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_stops_client_when_start_fails():
    client = _FakeClient(start_error=RuntimeError("startup failed"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(RuntimeError, match="startup failed"):
        await transport.complete(_messages(), model="gemini-3.7-flash")

    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_preserves_primary_error_when_cleanup_fails():
    session = _FakeSessionTimeout(disconnect_error=RuntimeError("disconnect failed"))
    client = _FakeClient(session=session, stop_error=RuntimeError("stop failed"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="timed out") as exc_info:
        await transport.complete(_messages(), model="gemini-3.7-flash")

    assert exc_info.value.status_code == 504
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_preserves_session_error_status_when_sdk_drops_it():
    session = _FakeSessionWithErrorOnComplete()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError) as exc_info:
        await transport.complete(_messages(), model="gemini-3.7-flash")

    assert exc_info.value.status_code == 401
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_raises_status_error_when_auth_check_transport_fails():
    client = _FakePreflight(auth_error=RuntimeError("network"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.preflight("gemini-3.7-flash")
    assert exc_info.value.status_code == 503
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_waits_for_session_idle_after_assistant_idle():
    session = _FakeSessionAssistantIdleOnly()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="timed out"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash", timeout_seconds=0.001)]


@pytest.mark.asyncio
async def test_stream_stops_client_when_start_fails():
    client = _FakeClient(start_error=RuntimeError("startup failed"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(RuntimeError, match="startup failed"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_preserves_primary_error_when_cleanup_fails():
    session = _FakeSessionWithErrorEvent(disconnect_error=RuntimeError("disconnect failed"))
    client = _FakeClient(session=session, stop_error=RuntimeError("stop failed"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="stream failed") as exc_info:
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert exc_info.value.status_code == 503
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_preserves_cancellation_when_cleanup_fails():
    session = _FakeSessionCancelledOnStream(disconnect_error=RuntimeError("disconnect failed"))
    client = _FakeClient(session=session, stop_error=RuntimeError("stop failed"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(asyncio.CancelledError):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_reraises_authentication_error_from_auth_check():
    client = _FakePreflight(auth_error=AuthenticationError("already structured", provider_type="copilot"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(AuthenticationError, match="already structured"):
        await transport.preflight("gemini-3.7-flash")
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_preserves_error_event_status_code():
    class _StatusSession(_FakeSessionWithErrorEvent):
        async def send(self, _prompt: str) -> None:
            assert self._handler is not None
            self._handler(
                SimpleNamespace(
                    type=SimpleNamespace(value="session.error"),
                    data=SimpleNamespace(status_code=401),
                )
            )

    session = _StatusSession()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError) as exc_info:
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_preflight_maps_http_401_from_auth_check_to_authentication_error():
    class _Http401(RuntimeError):
        status_code = 401

    client = _FakePreflight(auth_error=_Http401("unauthorized"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(AuthenticationError):
        await transport.preflight("gemini-3.7-flash")
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_raises_authentication_error_when_not_authenticated():
    client = _FakePreflight(authenticated=False)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(AuthenticationError):
        await transport.preflight("gemini-3.7-flash")
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_raises_status_error_when_model_list_fails():
    client = _FakePreflight(list_models_error=RuntimeError("unavailable"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.preflight("gemini-3.7-flash")
    assert exc_info.value.status_code == 503
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_preserves_structured_status_from_model_list_failure():
    client = _FakePreflight(list_models_error=_StatusError("rate limited", 429))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.preflight("gemini-3.7-flash")
    assert exc_info.value.status_code == 429
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_raises_status_error_when_model_list_is_empty():
    client = _FakePreflight(models=[])
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.preflight("gemini-3.7-flash")
    assert exc_info.value.status_code == 503
    assert client.stopped is True


class _SlowStart:
    """Client whose start() never returns within a short deadline."""

    def __init__(self) -> None:
        self.stopped = False

    async def start(self) -> None:
        await asyncio.sleep(10)

    async def stop(self) -> None:
        self.stopped = True

    async def get_auth_status(self) -> Any:
        return _FakeAuth()

    async def list_models(self) -> list[Any]:
        return [_FakeModel("gemini-3.7-flash")]


class _SlowAuthCheck:
    """Client whose get_auth_status() never returns within a short deadline."""

    def __init__(self) -> None:
        self.stopped = False

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        self.stopped = True

    async def get_auth_status(self) -> Any:
        await asyncio.sleep(10)

    async def list_models(self) -> list[Any]:
        return [_FakeModel("gemini-3.7-flash")]  # pragma: no cover


class _SlowListModels:
    """Client whose list_models() never returns within a short deadline."""

    def __init__(self) -> None:
        self.stopped = False

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        self.stopped = True

    async def get_auth_status(self) -> Any:
        return _FakeAuth()

    async def list_models(self) -> list[Any]:
        await asyncio.sleep(10)
        return []  # pragma: no cover - sleep is always cancelled by the deadline


@pytest.mark.asyncio
async def test_preflight_raises_status_error_when_start_exceeds_timeout():
    client = _SlowStart()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.preflight("gemini-3.7-flash", timeout_seconds=1)
    assert exc_info.value.status_code == 504
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_raises_status_error_when_auth_check_exceeds_timeout():
    client = _SlowAuthCheck()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.preflight("gemini-3.7-flash", timeout_seconds=1)
    assert exc_info.value.status_code == 504
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_raises_status_error_when_list_models_exceeds_timeout():
    client = _SlowListModels()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.preflight("gemini-3.7-flash", timeout_seconds=1)
    assert exc_info.value.status_code == 504
    assert client.stopped is True


@pytest.mark.asyncio
async def test_preflight_applies_default_timeout_when_none():
    """Omitting timeout_seconds must still bound preflight (default 60 s), not block forever."""
    from unittest.mock import patch

    wait_for_calls: list[float] = []

    async def _fake_wait_for(awaitable: Any, timeout: float) -> Any:
        wait_for_calls.append(timeout)
        awaitable.close()
        raise TimeoutError()

    client = _SlowListModels()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with patch("agentic_devtools.orchestration.llm.providers.copilot.asyncio.wait_for", side_effect=_fake_wait_for):
        with pytest.raises(_StatusError) as exc_info:
            await transport.preflight("gemini-3.7-flash", timeout_seconds=None)
    assert exc_info.value.status_code == 504
    # A finite 60-second deadline must have been applied — wait_for must have been called.
    assert wait_for_calls, "asyncio.wait_for was never called — no deadline was applied"
    assert all(t <= 60.0 for t in wait_for_calls), f"Expected ≤60 s deadline, got: {wait_for_calls}"


@pytest.mark.asyncio
async def test_preflight_zero_timeout_disables_deadline():
    """Explicit timeout_seconds=0 must opt out of the deadline (no asyncio.wait_for calls)."""
    from unittest.mock import patch

    wait_for_calls: list[float] = []

    async def _fake_wait_for(awaitable: Any, timeout: float) -> Any:  # pragma: no cover
        wait_for_calls.append(timeout)
        return await awaitable

    client = _FakePreflight(models=["gemini-3.7-flash"])
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with patch("agentic_devtools.orchestration.llm.providers.copilot.asyncio.wait_for", side_effect=_fake_wait_for):
        result = await transport.preflight("gemini-3.7-flash", timeout_seconds=0)
    assert result == {"gemini-3.7-flash"}
    assert wait_for_calls == [], "asyncio.wait_for must not be called when timeout_seconds=0"


# ---------------------------------------------------------------------------
# complete tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_complete_returns_text_on_success():
    session = _FakeSession()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    result = await transport.complete(_messages(), model="gemini-3.7-flash")
    assert result.text == "ok"
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_captures_usage_event():
    session = _FakeSessionWithUsageEvent()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    result = await transport.complete(_messages(), model="gemini-3.7-flash")
    assert result.text == "reply"
    assert result.finish_reason == "stop"
    assert result.model == "gpt-4o"
    assert result.usage is not None
    assert result.usage.total_tokens == 8
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_aggregates_usage_events_and_uses_last_metadata():
    session = _FakeSessionWithMultipleUsageEvents()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    result = await transport.complete(_messages(), model="gemini-3.7-flash")

    assert result.text == "reply"
    assert result.finish_reason == "stop"
    assert result.model == "gpt-4o"
    assert result.usage is not None
    assert result.usage.input_tokens == 12
    assert result.usage.output_tokens == 7
    assert result.usage.total_tokens == 19
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_raises_on_timeout():
    session = _FakeSessionTimeout()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.complete(_messages(), model="gemini-3.7-flash")
    assert exc_info.value.status_code == 504
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_raises_on_null_response():
    session = _FakeSessionNullResponse()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    with pytest.raises(_StatusError) as exc_info:
        await transport.complete(_messages(), model="gemini-3.7-flash")
    assert exc_info.value.status_code == 504
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_handles_non_callable_unsubscribe():
    session = _FakeSessionNonCallableUnsubscribe()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    # The non-callable unsubscribe should not cause an error
    result = await transport.complete(_messages(), model="gemini-3.7-flash")
    assert result.text == "ok"
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_on_usage_handler_ignores_non_usage_events():
    session = _FakeSessionWithNonUsageOnComplete()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    # Non-usage event should be ignored; response should still contain no usage metadata
    result = await transport.complete(_messages(), model="gemini-3.7-flash")
    assert result.text == "done"
    assert result.usage is None
    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_rejects_unsupported_generation_options():
    client = _FakeClient()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="does not support request options"):
        await transport.complete(_messages(), model="gemini-3.7-flash", temperature=0.1)

    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_disables_tools_and_custom_instruction_discovery():
    client = _FakeClient()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    await transport.complete(_messages(), model="gemini-3.7-flash")

    assert client.session_kwargs is not None
    assert client.session_kwargs["available_tools"] == []
    assert client.session_kwargs["skip_custom_instructions"] is True
    assert client.session_kwargs["enable_config_discovery"] is False
    assert client.session_kwargs["enable_on_demand_instruction_discovery"] is False


@pytest.mark.asyncio
async def test_complete_passes_system_message_to_session():
    client = _FakeClient()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    await transport.complete(
        [LLMMessage(role="system", content="System rules"), *_messages()],
        model="gemini-3.7-flash",
    )

    assert client.session_kwargs is not None
    assert client.session_kwargs["system_message"] == {"mode": "append", "content": "System rules"}


@pytest.mark.asyncio
async def test_complete_rejects_max_tokens():
    client = _FakeClient()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="max_tokens"):
        await transport.complete(_messages(), model="gemini-3.7-flash", max_tokens=100)

    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_rejects_unknown_extra_kwargs():
    client = _FakeClient()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="does not support request options.*tools"):
        await transport.complete(_messages(), model="gemini-3.7-flash", tools=[])


@pytest.mark.asyncio
async def test_complete_preserves_zero_timeout():
    session = _FakeSession()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    await transport.complete(_messages(), model="gemini-3.7-flash", timeout_seconds=0)

    assert session.last_timeout is None


@pytest.mark.asyncio
async def test_complete_preserves_cancellation_when_cleanup_fails():
    session = _FakeSessionCancelledOnComplete(disconnect_error=RuntimeError("disconnect failed"))
    client = _FakeClient(session=session, stop_error=RuntimeError("stop failed"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(asyncio.CancelledError):
        await transport.complete(_messages(), model="gemini-3.7-flash")

    assert client.stopped is True


@pytest.mark.asyncio
async def test_complete_times_out_when_start_exceeds_budget():
    client = _FakeClient(start_delay_seconds=2.0)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="timed out"):
        await transport.complete(_messages(), model="gemini-3.7-flash", timeout_seconds=0.01)

    assert client.stopped is True


# ---------------------------------------------------------------------------
# stream tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_stream_emits_only_deltas_not_final_full_message():
    session = _FakeSession()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    chunks = [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert [chunk.text_delta for chunk in chunks] == ["a", "b"]
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_emits_usage_metadata_chunk_when_usage_event_precedes_terminal():
    session = _FakeSessionWithUsage()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    chunks = [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    content_chunks = [c for c in chunks if c.text_delta]
    meta_chunks = [c for c in chunks if not c.text_delta and (c.usage or c.finish_reason or c.model)]
    assert [c.text_delta for c in content_chunks] == ["hi"]
    assert len(meta_chunks) == 1
    assert meta_chunks[0].finish_reason == "stop"
    assert meta_chunks[0].model == "gemini-3.7-flash"
    assert meta_chunks[0].usage is not None
    assert meta_chunks[0].usage.total_tokens == 15
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_aggregates_usage_events_and_uses_last_metadata():
    session = _FakeSessionWithMultipleUsageEventsInStream()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    chunks = [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    meta_chunks = [c for c in chunks if not c.text_delta and (c.usage or c.finish_reason or c.model)]
    assert len(meta_chunks) == 1
    assert meta_chunks[0].finish_reason == "stop"
    assert meta_chunks[0].model == "gemini-3.7-flash"
    assert meta_chunks[0].usage is not None
    assert meta_chunks[0].usage.input_tokens == 13
    assert meta_chunks[0].usage.output_tokens == 7
    assert meta_chunks[0].usage.total_tokens == 20
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_times_out_when_no_idle_event_arrives():
    session = _FakeSessionNoIdle()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="timed out"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash", timeout_seconds=0.001)]
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_times_out_when_send_exceeds_budget():
    session = _FakeSessionSlowSend()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="timed out"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash", timeout_seconds=1)]
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_ignores_second_idle_terminal_signal():
    session = _FakeSessionDoubleIdle()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    chunks = [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert [chunk.text_delta for chunk in chunks] == ["a"]
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_stops_client_when_session_creation_fails():
    client = _FakeClient(create_error=RuntimeError("boom"))
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(RuntimeError, match="boom"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_rejects_unknown_extra_kwargs():
    client = _FakeClient()
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="does not support request options.*tools"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash", tools=[])]


@pytest.mark.asyncio
async def test_stream_raises_on_error_event():
    session = _FakeSessionWithErrorEvent()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError) as exc_info:
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert exc_info.value.status_code == 503
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_ignores_unknown_event_names():
    session = _FakeSessionWithUnknownEvent()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    chunks = [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    # Unknown event produces no content; stream terminates cleanly on idle
    assert chunks == []
    assert session.disconnected is True
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_raises_on_queue_timeout():
    from unittest.mock import AsyncMock, patch

    session = _FakeSession()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with patch(
        "agentic_devtools.orchestration.llm.providers.copilot.asyncio.wait_for", new_callable=AsyncMock
    ) as mock_wf:
        mock_wf.side_effect = TimeoutError("queue get timeout")
        with pytest.raises(_StatusError) as exc_info:
            [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash")]

    assert exc_info.value.status_code == 504
    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_preserves_zero_timeout():
    session = _FakeSession()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    chunks = [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash", timeout_seconds=0)]

    assert [chunk.text_delta for chunk in chunks] == ["a", "b"]


@pytest.mark.asyncio
async def test_stream_times_out_during_session_creation():
    client = _FakeClient(create_delay_seconds=2.0)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)

    with pytest.raises(_StatusError, match="timed out"):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash", timeout_seconds=0.01)]

    assert client.stopped is True


@pytest.mark.asyncio
async def test_stream_timeout_budget_is_not_reset_between_chunks():
    session = _FakeSession()
    client = _FakeClient(session=session)
    transport = CopilotSDKTransport(client_factory=lambda **_: client)
    observed: list[float] = []

    async def immediate_wait_for(awaitable, timeout):
        observed.append(timeout)
        return await awaitable

    from unittest.mock import patch

    monotonic_values = iter([100.0, 100.5, 101.0, 101.5])

    def fake_monotonic() -> float:
        try:
            return next(monotonic_values)
        except StopIteration:
            return 101.5

    with (
        patch("agentic_devtools.orchestration.llm.providers.copilot.asyncio.wait_for", side_effect=immediate_wait_for),
        patch("agentic_devtools.orchestration.llm.providers.copilot.time.monotonic", side_effect=fake_monotonic),
    ):
        [chunk async for chunk in transport.stream(_messages(), model="gemini-3.7-flash", timeout_seconds=3)]

    assert len(observed) >= 3
    assert observed[0] <= 3.0
    assert observed[0] > 0
    assert any(timeout < observed[0] for timeout in observed[1:])


# ---------------------------------------------------------------------------
# close test
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_close_is_a_no_op():
    transport = CopilotSDKTransport()
    await transport.close()  # must not raise
