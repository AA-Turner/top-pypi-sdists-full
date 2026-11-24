"""A device turn's ``chat_template_kwargs`` is never reported as SDK drift.

Live 2026-11-10: every device chat turn (smollm2-135m) wrote a
``provider.sdk_signature_drift`` issue saying the OpenAI SDK "no longer declares"
``chat_template_kwargs``. It never did: that is a llama.cpp field and extra_body
is its normal road. The real DeviceChat send path is driven here against the real
OpenAI client and the real drift guard; only the network is fake.
"""

from __future__ import annotations

import json
from typing import Any

import openai as openai_sdk
import pytest
from openai import AsyncOpenAI

from matrx_ai.providers.device.device_api import DeviceChat
from matrx_ai.providers.generic_openai import generic_openai_api
from matrx_ai.providers.generic_openai.generic_openai_api import GenericOpenAIChat
from matrx_ai.providers.outbound_capture import resolve_sdk_httpx
from matrx_ai.providers.sdk_drift import _ANNOUNCED

FLAVOR = resolve_sdk_httpx(openai_sdk)


class _Sent(Exception):
    pass


@pytest.mark.asyncio
async def test_device_template_kwargs_ride_extra_body_without_a_drift_voice(monkeypatch) -> None:
    sent: list[Any] = []

    def handler(request: Any) -> Any:
        sent.append(request)
        raise _Sent  # the bytes are what we came for

    chat = DeviceChat()
    chat.client = AsyncOpenAI(
        api_key="device",
        base_url="http://device.invalid/v1",
        max_retries=0,
        http_client=FLAVOR.AsyncClient(transport=FLAVOR.MockTransport(handler)),
    )
    monkeypatch.setattr(generic_openai_api, "capture_request_payload", lambda *a, **k: None, raising=False)
    monkeypatch.setattr("matrx_ai.providers.snapshot.recapture_final_payload", lambda *_a, **_k: None)
    voiced: list[Any] = []
    monkeypatch.setattr("matrx_ai.providers.sdk_drift._voice", lambda *a, **k: voiced.append(a))
    _ANNOUNCED.discard("device:AsyncCompletions.create:chat_template_kwargs")

    config = {
        "model": "smollm2-135m",
        "messages": [{"role": "user", "content": "hi"}],
        "chat_template_kwargs": {"enable_thinking": False},
    }
    with pytest.raises(Exception):
        await chat._execute_non_streaming(dict(config), emitter=None, matrx_model_name="m")

    assert sent, "the request never reached the wire"
    body = json.loads(sent[0].content)
    assert body["chat_template_kwargs"] == {"enable_thinking": False}
    assert voiced == []


def test_a_plain_openai_compatible_server_still_voices_drift() -> None:
    assert GenericOpenAIChat.body_extras_expected is False
    assert DeviceChat.body_extras_expected is True
