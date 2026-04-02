"""Tests for ai/hume_client.py — Hume AI TTS HTTP client."""

from __future__ import annotations

import base64
import json

import httpx
import pytest

from heylead.ai.hume_client import (
    HumeAuthError,
    HumeClient,
    HumeError,
    HumeRateLimitError,
)


# ── Fixtures ──


SAMPLE_AUDIO = b"\xff\xfb\x90\x00" * 100  # Fake MP3 bytes
SAMPLE_AUDIO_B64 = base64.b64encode(SAMPLE_AUDIO).decode()

SAMPLE_VOICE_CONFIG = {
    "acting_instructions": "Confident, direct sales professional",
    "speed": 1.05,
    "output_format": "mp3",
    "sample_rate": 48000,
    "sliders": {"assertiveness": 60, "confidence": 50},
}


def _mock_hume_response(status=200, audio=SAMPLE_AUDIO_B64, duration=5.2, gen_id="abc123"):
    """Build a mock Hume TTS JSON response."""
    body = {
        "generations": [{
            "audio": audio,
            "duration": duration,
            "generation_id": gen_id,
        }],
        "request_id": "req-123",
    }
    return httpx.Response(status, json=body)


def _mock_error_response(status, text="error"):
    return httpx.Response(status, text=text)


# ── Tests ──


class TestGenerateAudio:
    @pytest.mark.asyncio
    async def test_success(self):
        transport = httpx.MockTransport(lambda req: _mock_hume_response())
        client = HumeClient("test-key")
        client._client = httpx.AsyncClient(transport=transport)

        result = await client.generate_audio("Hello world", SAMPLE_VOICE_CONFIG)

        assert result["audio"] == SAMPLE_AUDIO
        assert result["duration_seconds"] == 5.2
        assert result["generation_id"] == "abc123"

        await client.close()

    @pytest.mark.asyncio
    async def test_request_format(self):
        """Verify the request body sent to Hume API."""
        captured = {}

        def handler(request):
            captured["url"] = str(request.url)
            captured["headers"] = dict(request.headers)
            captured["body"] = json.loads(request.content)
            return _mock_hume_response()

        transport = httpx.MockTransport(handler)
        client = HumeClient("my-api-key")
        client._client = httpx.AsyncClient(transport=transport)

        await client.generate_audio("Test text", SAMPLE_VOICE_CONFIG)

        assert captured["headers"]["x-hume-api-key"] == "my-api-key"
        body = captured["body"]
        assert len(body["utterances"]) == 1
        assert body["utterances"][0]["text"] == "Test text"
        assert body["utterances"][0]["description"] == "Confident, direct sales professional"
        assert body["utterances"][0]["speed"] == 1.05
        assert body["format"]["type"] == "mp3"

        await client.close()

    @pytest.mark.asyncio
    async def test_default_speed_omitted(self):
        """Speed of 1.0 should not be included in request."""
        captured = {}

        def handler(request):
            captured["body"] = json.loads(request.content)
            return _mock_hume_response()

        transport = httpx.MockTransport(handler)
        client = HumeClient("key")
        client._client = httpx.AsyncClient(transport=transport)

        config = {**SAMPLE_VOICE_CONFIG, "speed": 1.0}
        await client.generate_audio("Text", config)

        assert "speed" not in captured["body"]["utterances"][0]

        await client.close()

    @pytest.mark.asyncio
    async def test_rate_limit_error(self):
        transport = httpx.MockTransport(lambda req: _mock_error_response(429))
        client = HumeClient("key")
        client._client = httpx.AsyncClient(transport=transport)

        with pytest.raises(HumeRateLimitError, match="rate limit"):
            await client.generate_audio("Text", SAMPLE_VOICE_CONFIG)

        await client.close()

    @pytest.mark.asyncio
    async def test_auth_error(self):
        transport = httpx.MockTransport(lambda req: _mock_error_response(401))
        client = HumeClient("bad-key")
        client._client = httpx.AsyncClient(transport=transport)

        with pytest.raises(HumeAuthError, match="authentication"):
            await client.generate_audio("Text", SAMPLE_VOICE_CONFIG)

        await client.close()

    @pytest.mark.asyncio
    async def test_server_error(self):
        transport = httpx.MockTransport(lambda req: _mock_error_response(500, "Internal error"))
        client = HumeClient("key")
        client._client = httpx.AsyncClient(transport=transport)

        with pytest.raises(HumeError, match="Internal error"):
            await client.generate_audio("Text", SAMPLE_VOICE_CONFIG)

        await client.close()

    @pytest.mark.asyncio
    async def test_empty_generations(self):
        resp = httpx.Response(200, json={"generations": []})
        transport = httpx.MockTransport(lambda req: resp)
        client = HumeClient("key")
        client._client = httpx.AsyncClient(transport=transport)

        with pytest.raises(HumeError, match="no generations"):
            await client.generate_audio("Text", SAMPLE_VOICE_CONFIG)

        await client.close()

    @pytest.mark.asyncio
    async def test_empty_audio(self):
        resp = httpx.Response(200, json={
            "generations": [{"audio": "", "duration": 0, "generation_id": "x"}]
        })
        transport = httpx.MockTransport(lambda req: resp)
        client = HumeClient("key")
        client._client = httpx.AsyncClient(transport=transport)

        with pytest.raises(HumeError, match="empty audio"):
            await client.generate_audio("Text", SAMPLE_VOICE_CONFIG)

        await client.close()

    @pytest.mark.asyncio
    async def test_no_description(self):
        """Config without acting_instructions should omit description."""
        captured = {}

        def handler(request):
            captured["body"] = json.loads(request.content)
            return _mock_hume_response()

        transport = httpx.MockTransport(handler)
        client = HumeClient("key")
        client._client = httpx.AsyncClient(transport=transport)

        config = {"speed": 1.0, "output_format": "mp3"}
        await client.generate_audio("Text", config)

        assert "description" not in captured["body"]["utterances"][0]

        await client.close()


class TestContextManager:
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with HumeClient("key") as client:
            assert client.api_key == "key"
