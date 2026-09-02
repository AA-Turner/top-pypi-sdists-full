"""`node_panel_hooks` — the narration contract for strict-JSON graph nodes.

The bug these lock down (measured on Study Pack v1, 2026-08-18):
`llm_to_pydantic` routes through `_DeltaEmitter`, which never forwards
`send_chunk` when `on_delta is None`. `docproc.content.structure` therefore
ran 72 seconds at `chars_streamed: 0` — the longest silence in the run.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.graph_nodes._strict_json import _DeltaEmitter, node_panel_hooks


class _RecordingEmitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.reasoning: list[str] = []
        self.phases: list[Any] = []
        self.resets = 0

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_reasoning_chunk(self, text: str) -> None:
        self.reasoning.append(text)

    async def send_phase(self, phase: Any) -> None:
        self.phases.append(phase)

    def reset_turn_text(self) -> None:
        self.resets += 1


@pytest.mark.asyncio
async def test_tokens_reach_the_node_emitter_through_the_delta_wrapper() -> None:
    """End-to-end through the REAL wrapper — a mock of `on_delta` alone would
    pass even if `_DeltaEmitter` went back to swallowing everything."""
    panel = _RecordingEmitter()
    on_delta, on_reset = node_panel_hooks(panel)
    wrapper = _DeltaEmitter(panel, on_delta, on_reset)

    await wrapper.send_chunk('{"title": ')
    await wrapper.send_chunk('"Photosynthesis"}')

    assert "".join(panel.chunks) == '{"title": "Photosynthesis"}'
    assert wrapper.get_turn_text() == '{"title": "Photosynthesis"}'


@pytest.mark.asyncio
async def test_reasoning_never_reaches_the_answer_channel() -> None:
    panel = _RecordingEmitter()
    on_delta, on_reset = node_panel_hooks(panel)
    wrapper = _DeltaEmitter(panel, on_delta, on_reset)

    await wrapper.send_chunk("<reasoning>")
    await wrapper.send_chunk("thinking out loud")
    await wrapper.send_chunk("</reasoning>")
    await wrapper.send_chunk('{"ok": true}')

    assert "".join(panel.chunks) == '{"ok": true}'
    assert "thinking out loud" in "".join(panel.reasoning)


@pytest.mark.asyncio
async def test_reset_before_any_token_is_turn_setup_not_a_restart() -> None:
    """The orchestrator resets at the START of every attempt, first included.
    Announcing that stamps `last_phase: "restarted"` on a normal run and
    leaves it there for the whole node."""
    panel = _RecordingEmitter()
    _on_delta, on_reset = node_panel_hooks(panel)

    await on_reset()

    assert panel.phases == []
    assert panel.resets == 0


@pytest.mark.asyncio
async def test_reset_after_streaming_retracts_and_announces_once() -> None:
    panel = _RecordingEmitter()
    on_delta, on_reset = node_panel_hooks(panel)

    await on_delta("half an answer")
    await on_reset()

    assert panel.resets == 1
    assert len(panel.phases) == 1
    assert "restart" in str(panel.phases[0]).lower()

    # A second reset with nothing new streamed must stay silent.
    await on_reset()
    assert panel.resets == 1
    assert len(panel.phases) == 1


@pytest.mark.asyncio
async def test_no_emitter_is_inert_not_a_crash() -> None:
    on_delta, on_reset = node_panel_hooks(None)
    await on_delta("text")
    await on_reset()


@pytest.mark.asyncio
async def test_a_failing_panel_never_breaks_the_generation() -> None:
    class _Broken:
        async def send_chunk(self, text: str) -> None:
            raise RuntimeError("panel is down")

    on_delta, _on_reset = node_panel_hooks(_Broken())
    await on_delta("text")  # must not raise
