"""Together runs on the OpenAI client, never the ``together`` SDK (CASA 6.1.1).

That SDK caps ``filelock`` below its fixed release, so the lock must not carry it (the lock
itself is the host's: tests/package_host_contracts/test_the_lock_never_carries_the_together_sdk.py).
Each test drives the real adapter and the real OpenAI client over a fake network
and reads the bytes sent: same hosts, same flat JSON body as the SDK produced.
"""

from __future__ import annotations

import json
from typing import Any

import openai as openai_sdk
import pytest
from openai import AsyncOpenAI

from matrx_ai.providers.outbound_capture import resolve_sdk_httpx
from matrx_ai.providers.sdk_drift import _ANNOUNCED, route_undeclared_params
from matrx_ai.providers.together import client as together_client
from matrx_ai.providers.together.together_api import TogetherChat
from matrx_ai.providers.together.together_image_api import TogetherImageGeneration
from matrx_ai.providers.together.together_video_api import TogetherVideoGeneration

FLAVOR = resolve_sdk_httpx(openai_sdk)


def _client(base_url: str, replies: list[Any]) -> tuple[AsyncOpenAI, list[Any]]:
    sent: list[Any] = []

    def handler(request: Any) -> Any:
        sent.append(request)
        return FLAVOR.Response(200, json=replies.pop(0))

    client = AsyncOpenAI(
        api_key="sk-test",
        base_url=base_url,
        max_retries=0,
        http_client=FLAVOR.AsyncClient(transport=FLAVOR.MockTransport(handler)),
    )
    return client, sent


async def test_chat_goes_to_the_inference_host_with_together_fields_flat_and_reasoning_read() -> None:
    reply = {
        "id": "r1",
        "model": "m",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"role": "assistant", "content": "hi", "reasoning_content": "thinking"},
            }
        ],
        "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
    }
    client, sent = _client(together_client.TOGETHER_INFERENCE_BASE_URL, [reply])
    chat = TogetherChat()
    chat.client = client
    request = {
        "model": "m",
        "messages": [{"role": "user", "content": "hi"}],
        "reasoning": {"enabled": True},
        "top_k": 5,
    }

    response = await client.chat.completions.create(
        **route_undeclared_params(
            client.chat.completions.create, request, provider="together", body_extras_expected=True
        )
    )
    unified = chat.to_unified_response(response, "m")

    assert str(sent[0].url) == "https://api-inference.together.ai/v1/chat/completions"
    assert json.loads(sent[0].content) == request
    assert [type(c).__name__ for c in unified.messages[0].content] == ["ThinkingContent", "TextContent"]
    assert unified.usage.input_tokens == 3


async def test_image_body_is_flat_on_the_api_host_and_assets_are_read_from_the_reply() -> None:
    image = {"id": "img1", "model": "m", "object": "list", "data": [{"index": 0, "type": "url", "url": "https://x/1.jpg"}]}
    client, sent = _client(together_client.TOGETHER_API_BASE_URL, [image])
    adapter = TogetherImageGeneration()
    adapter.client = client
    request = {"model": "m", "prompt": "cat", "steps": 4, "width": 512, "image_url": "https://x/in.png"}

    raw = await adapter._call_provider(dict(request))

    assert str(sent[0].url) == "https://api.together.ai/v1/images/generations"
    assert json.loads(sent[0].content) == request
    assert raw.id == "img1"
    assert [a.url for a in adapter._extract_assets(raw)] == ["https://x/1.jpg"]


async def test_video_is_created_and_polled_on_v2_and_failures_stop_the_poll(monkeypatch) -> None:
    job = {"id": "v1", "model": "m", "status": "in_progress"}
    failed = {"id": "v1", "model": "m", "status": "failed"}
    client, sent = _client(together_client.TOGETHER_API_BASE_URL, [job, failed])
    adapter = TogetherVideoGeneration()
    adapter.client = client
    request = {"model": "m", "prompt": "cat", "media": {"image": "https://x/in.png"}}

    async def no_wait(_seconds: float) -> None:
        return None

    monkeypatch.setattr("asyncio.sleep", no_wait)
    raw = await adapter._call_provider(dict(request))
    assert (raw.id, raw.status) == ("v1", "in_progress")
    with pytest.raises(RuntimeError, match="status=failed"):
        await adapter._poll_if_long_running(raw)

    assert sent[0].method == "POST" and str(sent[0].url) == "https://api.together.ai/v2/videos"
    assert json.loads(sent[0].content) == request
    assert sent[1].method == "GET" and str(sent[1].url) == "https://api.together.ai/v2/videos/v1"


async def test_the_bare_array_model_list_is_read(monkeypatch) -> None:
    from matrx_ai.providers.data_sync import together_model_sync

    client, sent = _client(together_client.TOGETHER_API_BASE_URL, [[{"id": "a"}, {"id": "b"}]])
    monkeypatch.setattr(together_model_sync, "get_together_client", lambda: client)

    assert await together_model_sync.list_together_models() == [{"id": "a"}, {"id": "b"}]
    assert str(sent[0].url) == "https://api.together.ai/v1/models"


def test_together_fields_on_the_openai_client_are_not_reported_as_sdk_drift() -> None:
    client = AsyncOpenAI(api_key="sk-test")
    before = set(_ANNOUNCED)

    kwargs = route_undeclared_params(
        client.images.generate, {"prompt": "p", "steps": 4}, provider="together", body_extras_expected=True
    )

    assert kwargs == {"prompt": "p", "extra_body": {"steps": 4}}
    assert _ANNOUNCED == before
