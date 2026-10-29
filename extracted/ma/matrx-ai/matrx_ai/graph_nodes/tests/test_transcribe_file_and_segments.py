"""Transcribe Audio takes a platform file and returns timed segments.

- ``file_id`` goes to the host's ``managed_file_transcriber`` seam (never fetched by URL here);
- verbose_json segments come out as ``{index, start_s, end_s, text}``, in order;
- the text format (no segments) gives an empty list, never a missing key;
- both or neither of ``file_id`` / ``audio_source`` is refused with a plain sentence.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from pydantic import ValidationError

from matrx_ai import _ext
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx
from matrx_ai.graph_nodes.transcribe_action import (
    MANAGED_FILE_TRANSCRIBER_EXT,
    TranscribeInput,
    ai_transcribe,
)


def _handler():
    return getattr(ai_transcribe, "__wrapped__", ai_transcribe)


async def _run(inputs: TranscribeInput) -> Any:
    result = await _handler()(_ctx(), inputs)
    return result.result


def _fake_stt(monkeypatch, *, segments):
    from matrx_ai.processing.audio import stt as stt_module

    usage = SimpleNamespace(
        duration_seconds=3.0,
        matrx_model_name="whisper-fake",
        to_token_usage=lambda: SimpleNamespace(calculate_cost=lambda: 0.001),
    )

    async def _fake_execute_stt(_request: Any) -> Any:
        return SimpleNamespace(text="hi there", language="en", duration=3.0, usage=usage, segments=segments)

    async def _no_pricing() -> None:
        return None

    monkeypatch.setattr(stt_module, "execute_stt", _fake_execute_stt)
    monkeypatch.setattr("matrx_ai.config.usage_config.ensure_pricing_lookup", _no_pricing)


@pytest.mark.asyncio
async def test_file_id_goes_through_the_host_seam(monkeypatch):
    seen: dict[str, Any] = {}

    async def _host(file_id: str, *, model: str, language: str | None, organization_id: str | None):
        seen.update(file_id=file_id, model=model, organization_id=organization_id)
        return SimpleNamespace(
            text="hello world",
            language="en",
            duration=4.0,
            segments=[SimpleNamespace(start=0.0, end=1.5, text="hello"), SimpleNamespace(start=1.5, end=4.0, text="world")],
            meta=SimpleNamespace(model="whisper-large"),
        )

    monkeypatch.setitem(_ext._registry, MANAGED_FILE_TRANSCRIBER_EXT, _host)
    out = await _run(TranscribeInput(file_id="f-123"))
    assert seen == {"file_id": "f-123", "model": "stt-default", "organization_id": "test-org"}
    assert [s.model_dump() for s in out.segments] == [
        {"index": 0, "start_s": 0.0, "end_s": 1.5, "text": "hello"},
        {"index": 1, "start_s": 1.5, "end_s": 4.0, "text": "world"},
    ]
    assert out.model == "whisper-large"
    assert out.usage.duration_seconds == 4.0


@pytest.mark.asyncio
async def test_file_id_without_a_host_seam_says_so(monkeypatch):
    monkeypatch.delitem(_ext._registry, MANAGED_FILE_TRANSCRIBER_EXT, raising=False)
    with pytest.raises(RuntimeError, match="cannot open a platform file"):
        await _run(TranscribeInput(file_id="f-123"))


@pytest.mark.asyncio
async def test_verbose_json_segments_come_out_in_order(monkeypatch):
    _fake_stt(monkeypatch, segments=[{"start": 0.0, "end": 1.0, "text": " hi"}, {"start": 1.0, "end": 3.0, "text": " there"}])
    out = await _run(TranscribeInput(audio_source="/tmp/fake.wav"))
    assert [(s.index, s.start_s, s.end_s, s.text) for s in out.segments] == [(0, 0.0, 1.0, " hi"), (1, 1.0, 3.0, " there")]


@pytest.mark.asyncio
async def test_text_format_gives_an_empty_segment_list(monkeypatch):
    _fake_stt(monkeypatch, segments=None)
    out = await _run(TranscribeInput(audio_source="/tmp/fake.wav", response_format="text"))
    assert out.segments == []
    assert "segments" in out.model_dump()


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"file_id": "f-1", "audio_source": "/tmp/a.wav"}, "both a file and an audio source"),
        ({}, "needs something to transcribe"),
        ({"file_id": "  "}, "needs something to transcribe"),
    ],
)
def test_both_or_neither_source_is_refused(kwargs, message):
    with pytest.raises(ValidationError, match=message):
        TranscribeInput(**kwargs)
