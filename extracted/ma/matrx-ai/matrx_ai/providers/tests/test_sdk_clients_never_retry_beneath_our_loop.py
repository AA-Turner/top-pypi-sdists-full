"""A provider SDK client never retries on its own beneath our retry loop.

THE BREAK THIS GUARDS (2026-10-01 review). The Stainless SDKs (openai,
anthropic, groq, cerebras, together) retry every connection error, timeout,
429 and 5xx TWICE by default (``max_retries=2``), silently. Every adapter here
already sits under one of OUR retry loops — the executor's provider retry
(schedules, the visible "retrying" state, admission's 429 accounting) or
aidream's ``transcribe_audio`` (3 attempts, billing-classified). Stacked, a
timed-out paid Groq transcription could be bought up to 9 times, and a 429 the
SDK absorbed never reached admission or the person's retry indicator.

Two halves:
* the forcing function — a real ``GroqSTT`` call against a provider answering
  500 reaches the wire exactly ONCE (the SDK default sends it three times);
* the census — every Stainless client constructed in an adapter passes
  ``max_retries``; a new adapter that forgets it turns this red.

Doubles: the network (an ``httpx.MockTransport`` counting requests) and the
catalog profile.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from matrx_ai.providers.groq import stt as groq_stt

PROVIDERS = Path(__file__).resolve().parents[1]

STAINLESS_CLIENTS = {"AsyncOpenAI", "AsyncAnthropic", "AsyncGroq", "AsyncCerebras", "AsyncTogether"}

#: Files that build a Stainless client NOT beneath one of our retry loops — the
#: SDK's own retry is the only retry they have. Each needs its reason.
NOT_UNDER_OUR_LOOP = {
    # Free model-list calls for the catalog sync jobs; no paid call, no loop.
    "openai/client.py",
    "anthropic/client.py",
    "groq/client.py",
    "cerebras/client.py",
    "together/client.py",
    "xai/client.py",
    # A one-shot reachability probe of a user-registered endpoint.
    "generic_openai/endpoint_probe.py",
    # The docstring example of the keyed client descriptor.
    "keys.py",
}


async def test_a_failed_transcription_is_sent_once_not_three_times(monkeypatch) -> None:
    sent: list[str] = []

    def _provider(request: httpx.Request) -> httpx.Response:
        sent.append(str(request.url))
        return httpx.Response(500, json={"error": {"message": "internal error", "type": "server_error"}})

    monkeypatch.setattr(groq_stt, "resolve_api_key", lambda *_a, **_k: "gsk_test_transcribe_retry")
    groq_stt._clients.clear()
    client = groq_stt._client()
    # Same client, same retry policy — only the network is replaced.
    monkeypatch.setitem(
        groq_stt._clients,
        "gsk_test_transcribe_retry",
        client.with_options(http_client=httpx.AsyncClient(transport=httpx.MockTransport(_provider))),
    )

    async def _prepared(*_a, **_k):
        return ("standup.m4a", b"\x00" * 2048, "audio/mp4"), 0.002

    monkeypatch.setattr(groq_stt, "prepare_audio_file", _prepared)
    monkeypatch.setattr(groq_stt, "resolve_outbound_params", lambda *_a, **_k: {})
    profile = SimpleNamespace(
        offering_metadata={"stt": {}},
        controls={},
        provider_model_id="whisper-large-v3-turbo",
        model_name="stt-default",
        vendor="groq",
        offering_id="groq-whisper-large-v3-turbo",
        usage_basis="audio_seconds",
    )
    request = SimpleNamespace(
        audio_source=b"\x00" * 2048,
        operation="transcription",
        response_format="verbose_json",
        timestamp_granularities=None,
        language=None,
    )

    with pytest.raises(Exception):
        await groq_stt.GroqSTT().execute(request, profile)  # type: ignore[arg-type]
    groq_stt._clients.clear()

    assert len(sent) == 1, f"the SDK retried a paid transcription on its own: {len(sent)} sends"


def _unretried_constructions() -> list[str]:
    found: list[str] = []
    for path in PROVIDERS.rglob("*.py"):
        rel = path.relative_to(PROVIDERS).as_posix()
        if rel.startswith("tests/") or rel in NOT_UNDER_OUR_LOOP:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", None)
            if name in STAINLESS_CLIENTS and not any(k.arg == "max_retries" for k in node.keywords):
                found.append(f"{rel}:{node.lineno} {name}")
    return found


def test_every_adapter_client_turns_the_sdk_retry_off() -> None:
    assert _unretried_constructions() == []


def test_the_census_sees_a_planted_unretried_client(tmp_path, monkeypatch) -> None:
    """The census can fail: a planted adapter without ``max_retries`` is named."""
    planted = tmp_path / "acme_rerank_api.py"
    planted.write_text("client = AsyncOpenAI(api_key='k')\n", encoding="utf-8")
    monkeypatch.setattr(
        "matrx_ai.providers.tests.test_sdk_clients_never_retry_beneath_our_loop.PROVIDERS", tmp_path
    )
    assert _unretried_constructions() == ["acme_rerank_api.py:1 AsyncOpenAI"]
