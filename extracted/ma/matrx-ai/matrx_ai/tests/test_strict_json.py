"""Pure-unit tests for the ``llm_to_pydantic`` helper's pre/post-processing.

These tests don't make LLM calls — they cover ``strip_json_fences``
edge cases and the ``StrictJsonError`` shape.
"""

from __future__ import annotations

from types import SimpleNamespace

from pydantic import BaseModel

from matrx_ai.graph_nodes import _strict_json, mandates
from matrx_ai.graph_nodes._strict_json import StrictJsonError, strip_json_fences


class _Verdict(BaseModel):
    passed: bool


class _WorkflowContext:
    source_app = "workflow"

    def __init__(self, source_feature: str):
        self.source_feature = source_feature


async def test_run_completion_measured_resolves_workflow_holder_for_inline_and_worker_lanes(
    monkeypatch,
):
    """Both workflow execution contexts reach the actual executor with a Holder."""
    seen: dict = {}

    async def fake_hold(step, *, spec_type, consumer, metadata):
        seen.update(step=step, spec_type=spec_type, consumer=consumer, metadata=metadata)
        return mandates.HeldStep(
            config=step,
            metadata={"mandate_holder": {"agent_id": "holder"}},
        )

    async def fake_execute(_config, **kwargs):
        seen["executor_metadata"] = kwargs["metadata"]
        return object()

    monkeypatch.setattr(mandates, "hold_step", fake_hold)
    monkeypatch.setattr("matrx_ai.orchestrator.executor.execute_ai_request", fake_execute)
    monkeypatch.setattr(
        "matrx_ai.graph_nodes.shared.normalize_completed",
        lambda _completed: SimpleNamespace(final_text="done", finish_reason="stop"),
    )
    monkeypatch.setattr(
        "matrx_connect.context.app_context.try_get_app_context",
        lambda: _WorkflowContext("workflow_run"),
    )

    await _strict_json._run_completion_measured(
        [], "system", model="claude-opus-5", max_tokens=100, metadata={"source_feature": "action"}
    )
    assert seen["executor_metadata"] == {"mandate_holder": {"agent_id": "holder"}}
    assert seen["consumer"] == "workflow.strict_json"

    monkeypatch.setattr(
        "matrx_connect.context.app_context.try_get_app_context",
        lambda: _WorkflowContext("workflow_worker"),
    )
    await _strict_json._run_completion_measured([], "system", model="claude-opus-5", max_tokens=100)
    assert seen["spec_type"] == "workflow.strict_json"


async def test_run_completion_measured_preserves_non_workflow_metadata(monkeypatch):
    """A bench or other standalone caller keeps its own provenance unchanged."""
    seen: dict = {}

    async def fake_execute(_config, **kwargs):
        seen["metadata"] = kwargs["metadata"]
        return object()

    monkeypatch.setattr("matrx_ai.orchestrator.executor.execute_ai_request", fake_execute)
    monkeypatch.setattr(
        "matrx_ai.graph_nodes.shared.normalize_completed",
        lambda _completed: SimpleNamespace(final_text="done", finish_reason="stop"),
    )
    monkeypatch.setattr(
        "matrx_connect.context.app_context.try_get_app_context",
        lambda: _WorkflowContext("masterwork_bench"),
    )

    original = {"source_feature": "masterwork_bench", "audit": "keep"}
    await _strict_json._run_completion_measured([], "system", model="claude-opus-5", max_tokens=100, metadata=original)
    assert seen["metadata"] == original


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


class _StubResult:
    """What ``_wrapped_completion_measured`` returns: text, finish, and usage.

    The strict-JSON funnel is measured now — it can tell a caller what the call
    cost — so a double returning a bare ``(text, finish)`` tuple would be
    doubling a function that no longer exists.
    """

    class _Usage:
        input_tokens = 100
        output_tokens = 20
        cost_usd = 0.001

    def __init__(self, text, finish="stop"):
        self.final_text = text
        self.finish_reason = finish
        self.usage = _StubResult._Usage()
        self.duration_ms = 10

    def model_copy(self, *, update=None):
        clone = _StubResult(self.final_text, self.finish_reason)
        for key, value in (update or {}).items():
            setattr(clone, key, value)
        return clone


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
            return _StubResult("first attempt prose, not json", "stop")
        return _StubResult("second attempt prose, still not json", "stop")

    monkeypatch.setattr(
        _strict_json, "_wrapped_completion_measured", fake_wrapped_completion
    )
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
        return _StubResult('{"passed": tr', "max_tokens")

    monkeypatch.setattr(
        _strict_json, "_wrapped_completion_measured", fake_wrapped_completion
    )
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
            return _StubResult("not-json", "stop")
        return _StubResult('{"passed": true}', "stop")

    monkeypatch.setattr(
        _strict_json, "_wrapped_completion_measured", fake_wrapped_completion
    )
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
