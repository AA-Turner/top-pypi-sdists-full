"""Tests for the record/replay LLM executor.

The key properties we care about:

1. **Stubs win.** A ``stub_response`` match short-circuits network + disk,
   making unit tests deterministic and zero-cost.
2. **Record-then-replay.** First run writes a JSON file; second run reads it.
3. **ReplayMiss.** In explicit ``replay`` mode, a missing recording raises
   a clear error (no silent real-provider fallback).
4. **End-to-end through the scheduler.** The monkeypatched executor plugs
   into ``ai.llm.chat`` without changing action code, and the resulting
   ``AiExecutionResult`` round-trips correctly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from matrx_ai.testing.record_replay import (
    RecordReplayExecutor,
    ReplayMiss,
    _make_key,
    clear_stubs,
    install_record_replay,
    stub_response,
)


@dataclass
class _Cfg:
    model: str = "gpt-5"
    messages: list | None = None
    system_instruction: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    tools: list | None = None


def _make_app_context() -> Any:
    """Minimal AppContext for tests that drive the scheduler end-to-end."""
    from matrx_connect.context.app_context import AppContext

    class _NoOpEmitter:
        async def send_chunk(self, *a, **kw):
            pass

        async def send_reasoning_chunk(self, *a, **kw):
            pass

        async def send_phase(self, *a, **kw):
            pass

        async def send_data(self, *a, **kw):
            pass

        async def send_init(self, *a, **kw):
            pass

        async def send_completion(self, *a, **kw):
            pass

        async def send_error(self, *a, **kw):
            pass

        async def send_tool_event(self, *a, **kw):
            pass

        async def send_end(self, *a, **kw):
            pass

    return AppContext(
        emitter=_NoOpEmitter(),
        user_id="test-user",
        is_authenticated=True,
        conversation_id="rr-test-conv",
        request_id="rr-test-req",
    )


@pytest.fixture(autouse=True)
def _reset_stubs():
    clear_stubs()
    yield
    clear_stubs()


# ---------------------------------------------------------------------------
# Keying
# ---------------------------------------------------------------------------


def test_key_is_stable_across_calls():
    cfg = _Cfg(messages=[{"role": "user", "content": "hi"}])
    k1 = _make_key(cfg)
    k2 = _make_key(cfg)
    assert k1 == k2
    assert len(k1) == 16


def test_key_differs_for_different_prompts():
    a = _Cfg(messages=[{"role": "user", "content": "hi"}])
    b = _Cfg(messages=[{"role": "user", "content": "hello"}])
    assert _make_key(a) != _make_key(b)


def test_key_differs_for_different_models():
    a = _Cfg(model="gpt-5", messages=[{"role": "user", "content": "x"}])
    b = _Cfg(model="claude-opus-4-7", messages=[{"role": "user", "content": "x"}])
    assert _make_key(a) != _make_key(b)


# ---------------------------------------------------------------------------
# Stub matching
# ---------------------------------------------------------------------------


async def test_stub_matches_on_prompt_substring(tmp_path):
    stub_response(
        response="stubbed answer",
        prompt_contains="summarize",
    )
    exec_ = RecordReplayExecutor(tmp_path, mode="replay")
    cfg = _Cfg(messages=[{"role": "user", "content": "please summarize this text"}])

    result = await exec_(cfg)

    assert result.final_response.text == "stubbed answer"
    assert result.iterations == 1
    assert result.metadata["source"] == "record_replay_stub"


async def test_stub_matches_on_model(tmp_path):
    stub_response(response="claude answer", model="claude")
    stub_response(response="gpt answer", model="gpt")
    exec_ = RecordReplayExecutor(tmp_path, mode="replay")

    r1 = await exec_(_Cfg(model="gpt-5", messages=[{"role": "user", "content": "x"}]))
    r2 = await exec_(_Cfg(model="claude-opus-4-7", messages=[{"role": "user", "content": "x"}]))

    assert r1.final_response.text == "gpt answer"
    assert r2.final_response.text == "claude answer"


async def test_stub_with_no_match_falls_through_to_replay(tmp_path):
    stub_response(response="won't match", prompt_contains="xxxx")
    exec_ = RecordReplayExecutor(tmp_path, mode="replay")
    cfg = _Cfg(messages=[{"role": "user", "content": "different prompt"}])

    with pytest.raises(ReplayMiss):
        await exec_(cfg)


# ---------------------------------------------------------------------------
# Replay mode
# ---------------------------------------------------------------------------


async def test_replay_miss_raises_with_clear_error(tmp_path):
    exec_ = RecordReplayExecutor(tmp_path, mode="replay")
    cfg = _Cfg(messages=[{"role": "user", "content": "unrecorded"}])

    with pytest.raises(ReplayMiss) as exc_info:
        await exec_(cfg)

    assert "gpt-5" in str(exc_info.value)
    assert "mode='record'" in str(exc_info.value)


async def test_replay_reads_existing_recording(tmp_path):
    import json

    cfg = _Cfg(messages=[{"role": "user", "content": "canned"}])
    key = _make_key(cfg)
    path = tmp_path / f"{key}.json"
    path.write_text(
        json.dumps(
            {
                "final_text": "recorded reply",
                "iterations": 2,
                "conversation_id": "c-123",
                "request_id": "r-456",
                "duration_ms": 500,
                "tool_calls_made": 0,
                "input_tokens": 42,
                "output_tokens": 7,
                "total_tokens": 49,
                "messages": [
                    {"role": "user", "content": "canned"},
                    {"role": "assistant", "content": "recorded reply"},
                ],
            }
        )
    )

    exec_ = RecordReplayExecutor(tmp_path, mode="replay")
    result = await exec_(cfg)

    assert result.final_response.text == "recorded reply"
    assert result.iterations == 2
    assert result.request.conversation_id == "c-123"
    assert result.total_usage.totals.total_tokens == 49


async def test_replay_stub_is_normalize_compatible(tmp_path):
    """The _CompletedStub we return must satisfy normalize_completed."""
    from matrx_ai.graph_nodes.shared import normalize_completed

    stub_response(response="integration reply")
    exec_ = RecordReplayExecutor(tmp_path, mode="replay")
    cfg = _Cfg(messages=[{"role": "user", "content": "test"}])

    completed = await exec_(cfg)
    normalized = normalize_completed(completed)

    assert normalized.final_text == "integration reply"
    assert normalized.iterations == 1


# ---------------------------------------------------------------------------
# install_record_replay — the monkeypatch seam
# ---------------------------------------------------------------------------


def test_install_monkeypatches_executor(tmp_path):
    from matrx_ai.orchestrator import executor as _exec_mod

    original = _exec_mod.execute_ai_request
    uninstall = install_record_replay(tmp_path, mode="replay")
    try:
        assert _exec_mod.execute_ai_request is not original
        assert isinstance(_exec_mod.execute_ai_request, RecordReplayExecutor)
    finally:
        uninstall()

    assert _exec_mod.execute_ai_request is original


async def test_install_plus_stub_short_circuits_llm_chat(tmp_path):
    """Stub + install → ai.llm.chat returns deterministically with no network,
    no DB, no credentials."""
    uninstall = install_record_replay(tmp_path, mode="replay")
    stub_response(
        response="two plus two is four",
        prompt_contains="two plus two",
    )

    try:
        from matrx_graph.types.result import Success

        from matrx_ai.graph_nodes.llm_action import LlmChatInput, llm_chat

        inputs = LlmChatInput(model="gpt-5", prompt="what is two plus two?")
        # ai.llm.chat returns NodeResult[AiExecutionResult] since the Node
        # Result System migration (eac3b53c4); the scheduler unwraps in real
        # runs, so a direct call unwraps here.
        node_result = await llm_chat(None, inputs)  # type: ignore[arg-type]
        assert isinstance(node_result, Success)
        result = node_result.result

        assert result.final_text == "two plus two is four"
        assert result.iterations == 1
        assert result.metadata.get("source") == "record_replay_stub"
    finally:
        uninstall()


# ---------------------------------------------------------------------------
# End-to-end: scheduler runs a graph whose only node is ai.llm.chat
# ---------------------------------------------------------------------------


async def test_end_to_end_scheduler_with_stubbed_llm(tmp_path):
    from matrx_graph import (
        Definition,
        MemoryCheckpointer,
        RunStatus,
        Scheduler,
        compile_graph,
        default_registry,
    )

    from matrx_ai.graph_nodes import register_with_graph

    register_with_graph()

    uninstall = install_record_replay(tmp_path, mode="replay")
    stub_response(
        response="forty-two",
        prompt_contains="meaning of life",
    )

    try:
        defn = Definition.model_validate(
            {
                "nodes": [
                    {
                        "id": "ask",
                        "type": "ai.llm.chat",
                        "position": {"x": 0, "y": 0},
                        "data": {},
                    }
                ],
                "edges": [],
            }
        )
        graph = compile_graph(defn, registry=default_registry())
        scheduler = Scheduler(
            graph,
            MemoryCheckpointer(),
            _make_app_context(),
            registry=default_registry(),
        )
        result = await scheduler.run(
            run_id="rr-e2e-1",
            inputs={
                "model": "gpt-5",
                "prompt": "what is the meaning of life?",
            },
        )

        assert result.status is RunStatus.COMPLETED
        out = result.last_outputs["ask"]
        assert out["final_text"] == "forty-two"
        assert out["iterations"] == 1
    finally:
        uninstall()
