"""Copilot SDK provider for the LangGraph LLM abstraction.

The SDK transport is deliberately kept behind ``CopilotTransport``.  Tests and
offline callers can inject a deterministic transport without starting the
Copilot CLI or supplying credentials.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import time
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from typing import Any, Protocol, cast

import jsonschema

from agentic_devtools.orchestration.llm.base_provider import LLMProvider, omit_none_values
from agentic_devtools.orchestration.llm.errors import (
    AuthenticationError,
    ModelNotAvailableError,
    RateLimitExhaustedError,
    RetryExhaustedError,
    StreamInterruptedError,
    StructuredOutputValidationError,
)
from agentic_devtools.orchestration.llm.retry import execute_with_retry
from agentic_devtools.orchestration.llm.types import (
    LLMMessage,
    LLMResponse,
    ProviderType,
    StreamChunk,
    TokenUsage,
)


@dataclass(frozen=True)
class CopilotTransportResponse:
    """Normalized response returned by a Copilot transport."""

    text: str
    model: str | None = None
    usage: TokenUsage | None = None
    finish_reason: str | None = None


@dataclass(frozen=True)
class CopilotTransportChunk:
    """Normalized streaming delta returned by a Copilot transport."""

    text_delta: str = ""
    finish_reason: str | None = None
    usage: TokenUsage | None = None
    model: str | None = None


class CopilotTransport(Protocol):
    """Narrow async boundary implemented by the Copilot SDK adapter or a fake."""

    async def preflight(self, model: str, *, timeout_seconds: int | None = None) -> set[str] | None:
        """Authenticate and return the authoritative model ids when available."""

    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        timeout_seconds: int | None = None,
        tools: Any = None,
        **kwargs: Any,
    ) -> CopilotTransportResponse:
        """Complete one request."""

    async def stream(
        self,
        messages: list[LLMMessage],
        *,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        timeout_seconds: int | None = None,
        tools: Any = None,
        **kwargs: Any,
    ) -> AsyncIterator[CopilotTransportChunk]:
        """Stream one request."""
        yield CopilotTransportChunk()  # pragma: no cover

    async def close(self) -> None:
        """Release the SDK client and any active sessions."""


class CopilotProvider(LLMProvider):
    """LLM provider backed by the authenticated GitHub Copilot runtime."""

    def __init__(
        self,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        timeout_seconds: int | None = None,
        *,
        transport: CopilotTransport | None = None,
        transport_factory: Callable[[], CopilotTransport] | None = None,
    ) -> None:
        if not isinstance(model, str) or not model.strip():
            raise ValueError("Copilot provider requires a non-empty model")
        if timeout_seconds is not None and timeout_seconds < 0:
            raise ValueError(f"timeout_seconds must be non-negative, got {timeout_seconds}")
        if transport is not None and transport_factory is not None:
            raise ValueError("Provide either transport or transport_factory, not both")
        self._model = model.strip()
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._timeout_seconds = timeout_seconds
        self._transport = transport
        self._transport_factory = transport_factory
        self._known_models: set[str] | None = None

    def _get_transport(self) -> CopilotTransport:
        if self._transport is None:
            if self._transport_factory is not None:
                self._transport = self._transport_factory()
            else:
                self._transport = CopilotSDKTransport()
        return self._transport

    async def preflight(self, models: list[str] | None = None) -> None:
        """Authenticate and validate the configured and requested models."""
        requested: list[str] = []
        if models:
            for candidate in models:
                if isinstance(candidate, str):
                    normalized = candidate.strip()
                    if normalized and normalized not in requested:
                        requested.append(normalized)
        if not requested:
            requested = [self._model]
        transport = self._get_transport()
        try:
            available = await execute_with_retry(
                transport.preflight, self._model, timeout_seconds=self._timeout_seconds
            )
        except RetryExhaustedError as exc:
            raise _map_retry_exhausted_error(exc, model=self._model, operation="preflight") from exc
        except asyncio.CancelledError:
            await self.close()
            raise
        except AuthenticationError:
            raise
        except Exception as exc:
            raise _map_transport_error(exc) from exc
        if available is not None:
            self._known_models = {item for item in available if isinstance(item, str) and item}
            for model in requested:
                self._validate_model(model)

    def _validate_model(self, model: str) -> None:
        if not isinstance(model, str) or not model.strip():
            raise ModelNotAvailableError(
                provider_type=ProviderType.COPILOT.value,
                model=model if isinstance(model, str) else "",
            )
        if self._known_models is not None and model not in self._known_models:
            raise ModelNotAvailableError(
                f"Model {model!r} is not available from provider 'copilot'",
                provider_type=ProviderType.COPILOT.value,
                model=model,
            )

    async def _ensure_model(self, model: str) -> None:
        self._validate_model(model)
        if self._known_models is None:
            transport = self._get_transport()
            preflight = getattr(transport, "preflight", None)
            if preflight is not None:
                await self.preflight([model])

    def _request_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        passthrough = {
            k: v for k, v in kwargs.items() if k not in {"temperature", "max_tokens", "timeout_seconds", "tools"}
        }
        timeout_override = kwargs.get("timeout_seconds", self._timeout_seconds)
        if timeout_override is not None and timeout_override < 0:
            raise ValueError(f"timeout_seconds must be non-negative, got {timeout_override}")
        values: dict[str, Any] = {
            "temperature": kwargs.get("temperature", self._temperature),
            "max_tokens": kwargs.get("max_tokens", self._max_tokens),
            "timeout_seconds": timeout_override,
        }
        tools = kwargs.get("tools", None)
        if tools is not None:
            values["tools"] = tools
        values.update(omit_none_values(passthrough))
        return values

    async def complete(self, messages: list[LLMMessage], **kwargs: Any) -> LLMResponse:
        """Make a Copilot completion request."""
        request = dict(kwargs)
        model = request.pop("model", self._model)
        await self._ensure_model(model)
        transport = self._get_transport()
        start = time.perf_counter()
        try:
            response = await execute_with_retry(
                transport.complete,
                messages,
                model=model,
                **self._request_kwargs(request),
            )
        except RetryExhaustedError as exc:
            raise _map_retry_exhausted_error(exc, model=model, operation="complete") from exc
        except asyncio.CancelledError:
            await self.close()
            raise
        except Exception as exc:
            raise _map_transport_error(exc, model=model) from exc
        return LLMResponse(
            text=response.text,
            model=response.model or model,
            provider_type=ProviderType.COPILOT,
            usage=response.usage,
            latency_ms=int((time.perf_counter() - start) * 1000),
            finish_reason=response.finish_reason,
        )

    async def complete_structured(
        self,
        messages: list[LLMMessage],
        schema: dict[str, Any],
        **kwargs: Any,
    ) -> LLMResponse:
        """Request JSON and validate it against ``schema`` deterministically."""
        schema_instruction = (
            f"\nRespond with valid JSON conforming to this schema:\n{json.dumps(schema, sort_keys=True)}"
        )
        augmented = list(messages)
        if augmented and augmented[0].role == "system":
            first = augmented[0]
            augmented[0] = LLMMessage(role="system", content=first.content + schema_instruction, name=first.name)
        else:
            augmented.insert(0, LLMMessage(role="system", content=schema_instruction.strip()))
        response = await self.complete(augmented, **kwargs)
        try:
            parsed = json.loads(response.text)
            jsonschema.validate(parsed, schema)
        except (json.JSONDecodeError, jsonschema.ValidationError) as exc:
            raise StructuredOutputValidationError(
                "Copilot response does not conform to the requested JSON schema",
                schema=schema,
                response_text=response.text,
                validation_errors=[exc.message if isinstance(exc, jsonschema.ValidationError) else "invalid JSON"],
            ) from exc
        return response

    async def stream(self, messages: list[LLMMessage], **kwargs: Any) -> AsyncIterator[StreamChunk]:
        """Stream Copilot deltas without replaying an interrupted response."""
        request = dict(kwargs)
        model = request.pop("model", self._model)
        await self._ensure_model(model)
        transport = self._get_transport()
        partial_response = ""
        chunks_received = 0
        start = time.perf_counter()
        request_kwargs = self._request_kwargs(request)
        try:

            async def open_stream() -> tuple[AsyncIterator[CopilotTransportChunk], CopilotTransportChunk | None]:
                result = transport.stream(messages, model=model, **request_kwargs)
                if inspect.isawaitable(result):
                    result = await result
                iterator = result.__aiter__()
                try:
                    first = await iterator.__anext__()
                except StopAsyncIteration:
                    first = None
                return iterator, first

            response_stream, first_chunk = await execute_with_retry(open_stream)

            async def all_chunks() -> AsyncIterator[CopilotTransportChunk]:
                if first_chunk is not None:
                    yield first_chunk
                async for chunk in response_stream:
                    yield chunk

            async for chunk in all_chunks():
                partial_response += chunk.text_delta
                emitted = StreamChunk(
                    text_delta=chunk.text_delta,
                    chunk_index=chunks_received,
                    finish_reason=chunk.finish_reason,
                    token_usage=chunk.usage,
                    model=chunk.model or model,
                )
                chunks_received += 1
                yield emitted
        except asyncio.CancelledError:
            await self.close()
            raise
        except RetryExhaustedError as exc:
            await self.close()
            raise _map_retry_exhausted_error(exc, model=model, operation="stream") from exc
        except Exception as exc:
            await self.close()
            if chunks_received:
                raise StreamInterruptedError(
                    "Copilot stream interrupted",
                    partial_response=partial_response,
                    chunks_received=chunks_received,
                ) from exc
            raise _map_transport_error(exc, model=model) from exc
        _ = start  # Keep timing available to transports without changing StreamChunk's contract.

    async def close(self) -> None:
        """Close the injected or SDK transport."""
        if self._transport is not None:
            await self._transport.close()

    shutdown = close


def _status_code(exc: BaseException) -> int | None:
    value = getattr(exc, "status_code", getattr(exc, "last_status_code", None))
    if isinstance(value, int):
        return value
    response = getattr(exc, "response", None)
    value = getattr(response, "status_code", None)
    return value if isinstance(value, int) else None


def _re_raise_with_traceback(exc: BaseException) -> None:
    raise exc.with_traceback(exc.__traceback__)


def _map_retry_exhausted_error(exc: RetryExhaustedError, *, model: str = "", operation: str) -> Exception:
    code = _status_code(exc)
    if code in {401, 403}:
        return AuthenticationError(
            "Copilot authentication is unavailable; sign in to the Copilot runtime and retry",
            provider_type=ProviderType.COPILOT.value,
        )
    if code == 404:
        return ModelNotAvailableError(
            f"Model {model!r} is not available from provider 'copilot'",
            provider_type=ProviderType.COPILOT.value,
            model=model,
        )
    if isinstance(exc, RateLimitExhaustedError):
        return exc
    if operation == "preflight":
        if code == 504:
            return _StatusError("Copilot request timed out", 504)
        if code is not None and code != 503:
            return _StatusError("Copilot request failed", code)
        return _StatusError("Copilot model inventory is unavailable", 503)
    return exc


async def _cleanup_with_primary_error(
    primary_error: BaseException | None,
    *cleanup_steps: Callable[[], Any],
) -> None:
    cleanup_error: BaseException | None = None
    for cleanup_step in cleanup_steps:
        try:
            await cleanup_step()
        except Exception as exc:  # pragma: no cover - branches exercised by SDK fakes
            if cleanup_error is None:
                cleanup_error = exc
    if primary_error is None and cleanup_error is not None:
        _re_raise_with_traceback(cleanup_error)


def _usage_sum(values: list[Any]) -> TokenUsage | None:
    total_input = 0
    total_output = 0
    total_tokens = 0
    saw_usage = False
    for value in values:
        usage = _usage_from(value)
        if usage is None:
            continue
        saw_usage = True
        total_input += usage.input_tokens
        total_output += usage.output_tokens
        total_tokens += usage.total_tokens
    if not saw_usage:
        return None
    return TokenUsage(
        input_tokens=total_input,
        output_tokens=total_output,
        total_tokens=total_tokens,
    )


def _map_transport_error(exc: Exception, *, model: str = "") -> Exception:
    """Map SDK failures to stable, non-secret-bearing LLM errors."""
    if isinstance(exc, (AuthenticationError, ModelNotAvailableError)):
        return exc
    code = _status_code(exc)
    if code in {401, 403}:
        return AuthenticationError(
            "Copilot authentication is unavailable; sign in to the Copilot runtime and retry",
            provider_type=ProviderType.COPILOT.value,
        )
    if code == 404:
        return ModelNotAvailableError(
            f"Model {model!r} is not available from provider 'copilot'",
            provider_type=ProviderType.COPILOT.value,
            model=model,
        )
    if isinstance(exc, (asyncio.TimeoutError, TimeoutError)):
        return _StatusError("Copilot request timed out", 504)
    if code is not None:
        return _StatusError("Copilot request failed", code)
    return exc


class _StatusError(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


class CopilotSDKTransport:
    """Production transport using the user's existing Copilot login.

    Each ``complete``, ``stream``, and ``preflight`` call starts a fresh SDK
    client and stops it in a ``finally`` block.  This keeps the client lifetime
    scoped to a single ``asyncio.run()`` invocation so that loop-bound SDK
    state (locks, background I/O) is never shared across the separate event
    loops used by ``_ReasoningAdapter.invoke()`` in ``context_factory.py``.
    """

    def __init__(self, client_factory: Callable[..., Any] | None = None) -> None:
        self._client_factory = client_factory
        self._models: set[str] | None = None

    def _make_client(self) -> Any:
        if self._client_factory is None:  # pragma: no cover
            from copilot import CopilotClient  # pragma: no cover

            self._client_factory = CopilotClient  # pragma: no cover
        return self._client_factory(use_logged_in_user=True)

    def _session_kwargs(
        self,
        model: str,
        temperature: float | None,
        max_tokens: int | None,
        *,
        system_message: str | None = None,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": model,
            "streaming": True,
            "available_tools": [],
            "skip_custom_instructions": True,
            "enable_config_discovery": False,
            "enable_on_demand_instruction_discovery": False,
        }
        unsupported: list[str] = []
        if temperature is not None:
            unsupported.append("temperature")
        if max_tokens is not None:
            unsupported.append("max_tokens")
        if unsupported:
            names = ", ".join(unsupported)
            raise _StatusError(
                f"Copilot runtime does not support request options for this provider: {names}",
                400,
            )
        if system_message is not None:
            kwargs["system_message"] = {"mode": "append", "content": system_message}
        return kwargs

    async def preflight(self, model: str, *, timeout_seconds: int | None = None) -> set[str]:
        client = self._make_client()
        primary_error: BaseException | None = None
        request_timeout = float(timeout_seconds if timeout_seconds is not None else 60)
        deadline = time.monotonic() + request_timeout if request_timeout > 0 else None

        async def _await_with_budget(awaitable: Any) -> Any:
            if deadline is None:
                return await awaitable
            remaining = max(0.0, deadline - time.monotonic())
            return await asyncio.wait_for(awaitable, timeout=remaining)

        try:
            await _await_with_budget(client.start())
            try:
                auth = await _await_with_budget(client.get_auth_status())
            except TimeoutError:
                raise _StatusError("Copilot request timed out", 504)
            except (AuthenticationError, ModelNotAvailableError):
                raise
            except Exception as exc:
                mapped = _map_transport_error(exc)
                if mapped is exc:
                    raise _StatusError(
                        "Copilot authentication status could not be read; retry in a moment", 503
                    ) from exc
                raise mapped from exc
            if not bool(getattr(auth, "isAuthenticated", getattr(auth, "is_authenticated", False))):
                raise AuthenticationError(
                    "Copilot authentication is unavailable; sign in to the Copilot runtime and retry",
                    provider_type=ProviderType.COPILOT.value,
                )
            try:
                models = await _await_with_budget(client.list_models())
                self._models = {str(getattr(item, "id", "")) for item in models if getattr(item, "id", None)}
            except TimeoutError:
                raise _StatusError("Copilot request timed out", 504)
            except Exception as exc:
                mapped = _map_transport_error(exc, model=model)
                if mapped is exc:
                    raise _StatusError("Copilot model inventory is unavailable", 503) from exc
                raise mapped from exc
            if not self._models:
                raise _StatusError("Copilot model inventory is unavailable", 503)
            return self._models
        except TimeoutError:
            primary_error = _StatusError("Copilot request timed out", 504)
            raise primary_error
        except BaseException as exc:
            primary_error = exc
            raise
        finally:
            await _cleanup_with_primary_error(primary_error, client.stop)

    @staticmethod
    def _system_message(messages: list[LLMMessage]) -> str | None:
        content = "\n\n".join(message.content for message in messages if message.role == "system")
        return content or None

    @staticmethod
    def _prompt(messages: list[LLMMessage]) -> str:
        return "\n\n".join(f"{message.role}: {message.content}" for message in messages if message.role != "system")

    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        timeout_seconds: int | None = None,
        **extra: Any,
    ) -> CopilotTransportResponse:
        if extra:
            names = ", ".join(sorted(extra))
            raise _StatusError(
                f"Copilot runtime does not support request options for this provider: {names}",
                400,
            )
        client = self._make_client()
        session: Any | None = None
        primary_error: BaseException | None = None
        request_timeout = float(timeout_seconds if timeout_seconds is not None else 60)
        deadline = time.monotonic() + request_timeout

        def _remaining_budget() -> float:
            return max(0.0, deadline - time.monotonic())

        def _sdk_timeout() -> float | None:
            if request_timeout == 0:
                return None
            return _remaining_budget()

        async def _await_with_budget(awaitable: Any) -> Any:
            if request_timeout == 0:
                return await awaitable
            return await asyncio.wait_for(awaitable, timeout=_remaining_budget())

        try:
            await _await_with_budget(client.start())
            session = await _await_with_budget(
                client.create_session(
                    **self._session_kwargs(
                        model,
                        temperature,
                        max_tokens,
                        system_message=self._system_message(messages),
                    )
                ),
            )
            usage_events: list[Any] = []
            session_error_status: int | None = None

            def on_event(event: Any) -> None:
                nonlocal session_error_status
                ename = getattr(getattr(event, "type", None), "value", getattr(event, "type", ""))
                data = getattr(event, "data", event)
                if ename == "assistant.usage":
                    usage_events.append(data)
                elif ename in {"session.error", "error", "assistant.error"}:
                    session_error_status = _status_code(data) or _status_code(event)

            unsubscribe = session.on(on_event)
            try:
                event = await _await_with_budget(
                    session.send_and_wait(
                        self._prompt(messages),
                        timeout=_sdk_timeout(),
                    )
                )
            except TimeoutError:
                raise _StatusError("Copilot request timed out", 504)
            except Exception as exc:
                if session_error_status is not None and _status_code(exc) is None:
                    raise _StatusError("Copilot request failed", session_error_status) from exc
                raise
            finally:
                if callable(unsubscribe):
                    unsubscribe()
            if event is None:
                raise _StatusError("Copilot request timed out", 504)
            data = getattr(event, "data", event)
            text = getattr(data, "content", "") or ""
            usage_data = usage_events[-1] if usage_events else None
            usage = _usage_sum(usage_events)
            served_model = (
                getattr(usage_data, "model", None) if usage_data is not None else getattr(data, "model", None)
            )
            finish_reason_value = getattr(usage_data, "finish_reason", None) if usage_data is not None else None
            finish_reason = finish_reason_value if isinstance(finish_reason_value, str) else None
            return CopilotTransportResponse(
                text=text,
                model=served_model,
                usage=usage,
                finish_reason=finish_reason,
            )
        except TimeoutError:
            primary_error = _StatusError("Copilot request timed out", 504)
            raise primary_error
        except BaseException as exc:
            primary_error = exc
            raise
        finally:
            cleanup_steps: list[Callable[[], Any]] = []
            if session is not None:
                cleanup_steps.append(session.disconnect)
            cleanup_steps.append(client.stop)
            await _cleanup_with_primary_error(primary_error, *cleanup_steps)

    async def stream(
        self,
        messages: list[LLMMessage],
        *,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        timeout_seconds: int | None = None,
        **extra: Any,
    ) -> AsyncIterator[CopilotTransportChunk]:
        if extra:
            names = ", ".join(sorted(extra))
            raise _StatusError(
                f"Copilot runtime does not support request options for this provider: {names}",
                400,
            )
        queue: asyncio.Queue[CopilotTransportChunk | BaseException | None] = asyncio.Queue()
        loop = asyncio.get_running_loop()
        client = self._make_client()
        session = None
        unsubscribe = None
        primary_error: BaseException | None = None
        request_timeout = float(timeout_seconds if timeout_seconds is not None else 60)
        deadline = time.monotonic() + request_timeout

        def _remaining_budget() -> float:
            return max(0.0, deadline - time.monotonic())

        async def _await_with_budget(awaitable: Any) -> Any:
            if request_timeout == 0:
                return await awaitable
            return await asyncio.wait_for(awaitable, timeout=_remaining_budget())

        try:
            await _await_with_budget(client.start())
            session = await _await_with_budget(
                client.create_session(
                    **self._session_kwargs(
                        model,
                        temperature,
                        max_tokens,
                        system_message=self._system_message(messages),
                    )
                )
            )
            sent_terminal_signal = False
            usage_events: list[Any] = []

            def on_event(event: Any) -> None:
                nonlocal sent_terminal_signal
                event_name = getattr(getattr(event, "type", None), "value", getattr(event, "type", ""))
                data = getattr(event, "data", event)
                if event_name == "assistant.message_delta":
                    loop.call_soon_threadsafe(
                        queue.put_nowait,
                        CopilotTransportChunk(text_delta=getattr(data, "delta_content", "") or ""),
                    )
                elif event_name == "assistant.usage":
                    usage_events.append(data)
                elif event_name == "session.idle":
                    if not sent_terminal_signal:
                        sent_terminal_signal = True
                        usage_data = usage_events[-1] if usage_events else None
                        if usage_data is not None:
                            tok = _usage_sum(usage_events)
                            finish_reason_v = getattr(usage_data, "finish_reason", None)
                            model_v = getattr(usage_data, "model", None)
                            loop.call_soon_threadsafe(
                                queue.put_nowait,
                                CopilotTransportChunk(
                                    finish_reason=finish_reason_v if isinstance(finish_reason_v, str) else None,
                                    usage=tok,
                                    model=model_v if isinstance(model_v, str) else None,
                                ),
                            )
                        loop.call_soon_threadsafe(queue.put_nowait, None)
                elif event_name in {"session.error", "error", "assistant.error"}:
                    status_code = _status_code(data) or _status_code(event) or 503
                    loop.call_soon_threadsafe(
                        queue.put_nowait,
                        _StatusError("Copilot stream failed", status_code),
                    )

            unsubscribe = session.on(on_event)
            try:
                await _await_with_budget(session.send(self._prompt(messages)))
            except TimeoutError:
                raise _StatusError("Copilot request timed out", 504)
            while True:
                try:
                    item = await _await_with_budget(queue.get())
                except TimeoutError:
                    raise _StatusError("Copilot request timed out", 504)
                if item is None:
                    return
                if isinstance(item, BaseException):
                    raise item
                yield item
        except TimeoutError:
            primary_error = _StatusError("Copilot request timed out", 504)
            raise primary_error
        except BaseException as exc:
            primary_error = exc
            raise
        finally:
            if callable(unsubscribe):
                unsubscribe()
            await _cleanup_with_primary_error(
                primary_error,
                *((session.disconnect,) if session is not None else ()),
                client.stop,
            )

    async def close(self) -> None:
        pass  # Clients are scoped to each invocation; nothing to close here.


def _usage_from(value: Any) -> TokenUsage | None:
    if value is None:
        return None
    usage = getattr(value, "usage", None)
    usage_source = usage if usage is not None else value
    input_tokens: object = getattr(usage_source, "input_tokens", getattr(usage_source, "prompt_tokens", None))
    output_tokens: object = getattr(
        usage_source,
        "output_tokens",
        getattr(usage_source, "completion_tokens", None),
    )
    total_tokens: object = getattr(usage_source, "total_tokens", None)
    if not isinstance(total_tokens, int) and isinstance(input_tokens, int) and isinstance(output_tokens, int):
        total_tokens = input_tokens + output_tokens
    if not all(isinstance(item, int) for item in (input_tokens, output_tokens, total_tokens)):
        return None
    return TokenUsage(
        input_tokens=cast(int, input_tokens),
        output_tokens=cast(int, output_tokens),
        total_tokens=cast(int, total_tokens),
    )
