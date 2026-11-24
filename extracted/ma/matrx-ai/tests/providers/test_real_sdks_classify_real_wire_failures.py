"""The INSTALLED provider SDKs, fed real HTTP failures, classify the way we promise.

Every other classifier test builds the SDK's exception object by hand, so it proves the
classifier — never that the SDK still RAISES that object for that status. An SDK bump can
change both halves: a new exception class for 529, a new HTTP library under the client
(anthropic 1.0 and openai 3.0 moved to httpx2), a mid-stream drop wrapped differently.
This drives each SDK's real client over a fake wire — the transport flavor the SDK itself
is built on (``resolve_sdk_httpx``) — so the upgrade campaign's first red is here, for
free, not on a paid call in production.

Promises held, per SDK: a bad key is ``auth_error`` (never retried); a rate limit is
``rate_limit`` (retried); an oversized body is ``request_too_large`` (never retried); a
5xx is retried; a stream the server cuts off mid-body is a retryable transport failure,
never an ``unknown_error``.
"""

from __future__ import annotations

import importlib
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import pytest

from matrx_ai.providers import errors as e
from matrx_ai.providers.outbound_capture import resolve_sdk_httpx

_MESSAGES = [{"role": "user", "content": "hi"}]


@dataclass(frozen=True)
class Sdk:
    id: str
    module: str
    client_attr: str
    classify: Callable[[Exception], e.RetryableError]
    call: Callable[[Any, bool], Awaitable[Any]]


async def _anthropic_call(client: Any, stream: bool) -> Any:
    return await client.messages.create(
        model="claude-x", max_tokens=8, messages=_MESSAGES, stream=stream
    )


async def _chat_completions_call(client: Any, stream: bool) -> Any:
    return await client.chat.completions.create(model="m-x", messages=_MESSAGES, stream=stream)


SDKS = [
    Sdk("anthropic", "anthropic", "AsyncAnthropic", e.classify_anthropic_error, _anthropic_call),
    Sdk("openai", "openai", "AsyncOpenAI", e.classify_openai_error, _chat_completions_call),
    Sdk("groq", "groq", "AsyncGroq", e.classify_groq_error, _chat_completions_call),
    Sdk(
        "cerebras",
        "cerebras.cloud.sdk",
        "AsyncCerebras",
        e.classify_cerebras_error,
        _chat_completions_call,
    ),
    Sdk("together", "openai", "AsyncOpenAI", e.classify_together_error, _chat_completions_call),
]


def _client(sdk: Sdk, handler: Callable[[Any], Any]) -> Any:
    module = importlib.import_module(sdk.module)
    flavor = resolve_sdk_httpx(module)
    http_client = flavor.AsyncClient(transport=flavor.MockTransport(handler))
    return getattr(module, sdk.client_attr)(
        api_key="sk-test", base_url="http://provider.test", max_retries=0, http_client=http_client
    )


async def _raised(sdk: Sdk, handler: Callable[[Any], Any], *, stream: bool = False) -> Exception:
    client = _client(sdk, handler)
    with pytest.raises(Exception) as caught:
        result = await sdk.call(client, stream)
        if stream:
            async for _ in result:
                pass
    return caught.value


def _status(status: int, message: str, error_type: str = "api_error") -> Callable[[Any], Any]:
    def handler(request: Any) -> Any:
        flavor = type(request).__module__.split(".")[0]
        body = {"type": "error", "error": {"type": error_type, "message": message}}
        return importlib.import_module(flavor).Response(status, json=body, request=request)

    return handler


@pytest.mark.parametrize("sdk", SDKS, ids=lambda s: s.id)
@pytest.mark.parametrize(
    ("status", "message", "expected", "retryable"),
    [
        (401, "invalid x-api-key", "auth_error", False),
        (429, "rate limit reached for requests", "rate_limit", True),
        (413, "request entity too large", "request_too_large", False),
        (500, "internal server error", "server_error", True),
    ],
    ids=["bad_key", "rate_limit", "too_large", "server_error"],
)
async def test_a_real_status_from_the_wire_classifies_as_promised(
    sdk, status, message, expected, retryable
) -> None:
    pytest.importorskip(sdk.module)
    exc = await _raised(sdk, _status(status, message))
    info = sdk.classify(exc)
    assert (info.error_type, info.is_retryable) == (expected, retryable), (type(exc), info)


async def test_anthropic_529_overloaded_is_retried_as_overload() -> None:
    sdk = SDKS[0]
    exc = await _raised(sdk, _status(529, "Overloaded", "overloaded_error"))
    info = sdk.classify(exc)
    assert (info.error_type, info.is_retryable) == ("provider_overloaded", True), (type(exc), info)


def _cut_off_stream(first_event: bytes, error: str, message: str) -> Callable[[Any], Any]:
    def handler(request: Any) -> Any:
        flavor = importlib.import_module(type(request).__module__.split(".")[0])

        class _Body(flavor.AsyncByteStream):
            async def __aiter__(self) -> AsyncIterator[bytes]:
                yield first_event
                raise getattr(flavor, error)(message)

        return flavor.Response(
            200, headers={"content-type": "text/event-stream"}, stream=_Body(), request=request
        )

    return handler


_FIRST_EVENT = {
    "anthropic": b'event: message_start\ndata: {"type":"message_start","message":{"id":"m","type":"message",'
    b'"role":"assistant","model":"claude-x","content":[],"stop_reason":null,"stop_sequence":null,'
    b'"usage":{"input_tokens":1,"output_tokens":0}}}\n\n',
}
_CHAT_CHUNK = (
    b'data: {"id":"c","object":"chat.completion.chunk","created":0,"model":"m-x",'
    b'"choices":[{"index":0,"delta":{"role":"assistant","content":"Hel"},"finish_reason":null}]}\n\n'
)


# The blank-message cases matter most: a real ``ReadError`` usually stringifies to "", so
# the classifier's wording fallback has nothing to read and only the TYPED branch can name it.
@pytest.mark.parametrize("sdk", SDKS, ids=lambda s: s.id)
@pytest.mark.parametrize(
    ("error", "message"),
    [
        ("RemoteProtocolError", "peer closed connection without sending complete message body"),
        ("RemoteProtocolError", ""),
        ("ReadError", ""),
    ],
    ids=["worded_cut", "blank_cut", "blank_read_error"],
)
async def test_a_stream_cut_off_mid_body_is_a_retryable_transport_failure(
    sdk, error, message
) -> None:
    pytest.importorskip(sdk.module)
    first_event = _FIRST_EVENT.get(sdk.id, _CHAT_CHUNK)
    exc = await _raised(sdk, _cut_off_stream(first_event, error, message), stream=True)
    info = sdk.classify(exc)
    assert info.is_retryable is True, (type(exc), info)
    assert info.error_type in {"incomplete_response", "connection_error"}, (type(exc), info)
