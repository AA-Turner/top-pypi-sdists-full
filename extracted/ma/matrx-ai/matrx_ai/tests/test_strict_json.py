"""Pure-unit tests for the ``llm_to_pydantic`` helper's pre/post-processing.

These tests don't make LLM calls — they cover ``strip_json_fences``
edge cases and the ``StrictJsonError`` shape.
"""

from __future__ import annotations

from pydantic import BaseModel

from matrx_ai.graph_nodes import _strict_json
from matrx_ai.graph_nodes._strict_json import StrictJsonError, strip_json_fences


class _Verdict(BaseModel):
    passed: bool


def test_strip_json_fences_plain_object_passes_through():
    assert strip_json_fences('{"a": 1}') == '{"a": 1}'


def test_strip_json_fences_with_fences():
    raw = '```json\n{"a": 1, "b": [2,3]}\n```'
    assert strip_json_fences(raw) == '{"a": 1, "b": [2,3]}'


def test_strip_json_fences_with_unlabeled_fences():
    raw = '```\n{"x": "y"}\n```'
    assert strip_json_fences(raw) == '{"x": "y"}'


def test_strip_json_fences_with_prose_preamble():
    raw = 'Sure, here is the JSON:\n{"answer": 42}'
    assert strip_json_fences(raw) == '{"answer": 42}'


def test_strip_json_fences_with_array_top_level():
    raw = "Here you go: [1, 2, 3]"
    assert strip_json_fences(raw) == "[1, 2, 3]"


def test_strip_json_fences_empty_input():
    assert strip_json_fences("") == ""


def test_strict_json_error_is_exception():
    err = StrictJsonError("oops")
    assert isinstance(err, Exception)
    assert str(err) == "oops"
    assert err.raw_output == ""


async def test_double_parse_failure_carries_full_raw_output(monkeypatch):
    """PAID-OUTPUT-DISCARDED guard: both failed attempts' raw text must ride
    the exception as ``raw_output`` (latest attempt), not just an exception
    message fragment."""
    calls: list[dict] = []

    async def fake_wrapped_completion(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return "first attempt prose, not json", "stop"
        return "second attempt prose, still not json", "stop"

    monkeypatch.setattr(_strict_json, "_wrapped_completion", fake_wrapped_completion)
    try:
        await _strict_json.llm_messages_to_pydantic(
            model="test-model",
            system="judge",
            messages=[{"role": "user", "content": "rate"}],
            output_cls=_Verdict,
        )
    except StrictJsonError as exc:
        assert exc.raw_output == "second attempt prose, still not json"
    else:
        raise AssertionError("expected StrictJsonError")


async def test_truncation_error_carries_raw_output(monkeypatch):
    async def fake_wrapped_completion(**kwargs):
        return '{"passed": tr', "max_tokens"

    monkeypatch.setattr(_strict_json, "_wrapped_completion", fake_wrapped_completion)
    try:
        await _strict_json.llm_messages_to_pydantic(
            model="test-model",
            system="judge",
            messages=[{"role": "user", "content": "rate"}],
            output_cls=_Verdict,
        )
    except _strict_json.StrictJsonTruncatedError as exc:
        assert exc.raw_output == '{"passed": tr'
    else:
        raise AssertionError("expected StrictJsonTruncatedError")


async def test_multimodal_retry_preserves_original_image(monkeypatch):
    calls: list[dict] = []

    async def fake_wrapped_completion(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return "not-json", "stop"
        return '{"passed": true}', "stop"

    monkeypatch.setattr(_strict_json, "_wrapped_completion", fake_wrapped_completion)
    image = {"type": "image", "base64_data": "aGVsbG8=", "mime_type": "image/png"}
    result = await _strict_json.llm_messages_to_pydantic(
        model="test-model",
        system="judge",
        messages=[{"role": "user", "content": [image, {"type": "text", "text": "rate"}]}],
        output_cls=_Verdict,
        internal_web_search=True,
    )

    assert result.passed is True
    assert calls[0]["messages"][0]["content"][0] == image
    assert calls[1]["messages"][0]["content"][0] == image
    assert calls[0]["internal_web_search"] is True
    assert calls[1]["internal_web_search"] is False
    assert calls[0]["on_delta"] is None
    assert calls[0]["response_format"]["type"] == "json_schema"
