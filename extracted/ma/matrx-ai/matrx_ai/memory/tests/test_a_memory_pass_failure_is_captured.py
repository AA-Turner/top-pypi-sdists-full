"""A memory pass that fails is CAPTURED as a system error, and an image-bearing turn observes.

2026-11-15 (failure register entry 23): "[OM] Observer failed: Object of type ImageContent is not
JSON serializable" right after a cloud_browser screenshot — caught and only logged, so memory
silently stopped for that conversation. The serializer is fixed (``types.dumps_safe``); these tests
run the WHOLE observe step (``process_output_step``) on a conversation whose tool returned a
screenshot, and prove every swallow site (buffer, observe, reflect) now reaches the capture sink.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.tools_config import ToolResultContent
from matrx_ai.memory import (
    InMemoryStorage,
    ObservationalMemory,
    ObservationalMemoryConfig,
    ObservationConfig,
    ReflectionConfig,
)
from matrx_ai.memory.adapter import convert_to_om_messages
from matrx_ai.memory.observational_memory import MEMORY_PASS_FAILED_KIND


def _screenshot_turns() -> list[Any]:
    shot = ImageContent(url="https://example.com/shot.png", mime_type="image/png")
    result = ToolResultContent(
        tool_use_id="toolu_1",
        name="cloud_browser",
        content=[{"type": "text", "text": "navigated to the billing page " * 20}, shot],
    )
    raw = [
        {"role": "user", "content": "open the billing page and tell me the weekly cap " * 10},
        {"role": "tool", "content": [result]},
        {"role": "user", "content": [shot, "what does this show? " * 10]},
    ]
    return convert_to_om_messages(raw, thread_id="t", resource_id="r")


def _om(llm: Any, *, observe_at: int = 10, reflect_at: int = 100000) -> tuple[ObservationalMemory, Any]:
    storage = InMemoryStorage()
    cfg = ObservationalMemoryConfig(
        observation=ObservationConfig(token_threshold=observe_at, buffer_tokens=None),
        reflection=ReflectionConfig(token_threshold=reflect_at),
    )
    return ObservationalMemory(
        config=cfg, storage=storage, count_tokens_fn=lambda t: len(t) // 4, llm_call_fn=llm
    ), storage


@pytest.fixture()
def captured():
    from matrx_connect.streaming import error_capture

    seen: list[dict[str, Any]] = []

    async def _sink(exc: BaseException, *, kind: str, **fields: Any) -> None:
        seen.append({"exc": exc, "kind": kind, **fields})

    error_capture.configure_error_capture(_sink, allow_in_tests=True)
    yield seen
    error_capture.configure_error_capture(None)


def test_an_image_bearing_turn_observes_through_the_whole_step(captured) -> None:
    prompts: list[str] = []

    async def llm(*, mandate_key, messages=None, model=None, variables=None):
        prompts.append(str(variables or messages))
        return (
            "<observations>\n* (16:57) User asked for the weekly cap from a screenshot\n</observations>"
            "\n<current-task>read the cap</current-task>\n<suggested-response>s</suggested-response>"
        )

    om, storage = _om(llm)

    async def run() -> Any:
        await om.process_output_step(_screenshot_turns(), "t", "r")
        return await storage.get_record("r", "t", om.config.scope)

    record = asyncio.run(run())
    assert captured == [], captured
    assert "weekly cap from a screenshot" in (record.active_observations or "")
    assert "[image content]" in prompts[0], "the observer is told an image was there"


@pytest.mark.parametrize("stage", ["observe", "reflect"])
def test_a_failed_pass_is_captured_never_only_logged(captured, stage: str) -> None:
    async def llm(*, mandate_key, messages=None, model=None, variables=None):
        if (stage == "observe" and mandate_key == "memory.observer") or (
            stage == "reflect" and mandate_key != "memory.observer"
        ):
            raise TypeError("Object of type ImageContent is not JSON serializable")
        return "<observations>\n" + ("* a long observation line\n" * 40) + "</observations>"

    om, _storage = _om(llm, reflect_at=20 if stage == "reflect" else 100000)
    asyncio.run(om.process_output_step(_screenshot_turns(), "t", "r"))
    kinds = [(c["kind"], c["payload"]["stage"]) for c in captured]
    assert (MEMORY_PASS_FAILED_KIND, stage) in kinds, captured


def test_a_failed_buffer_pass_is_captured(captured) -> None:
    async def llm(**_: Any):
        raise TypeError("Object of type ImageContent is not JSON serializable")

    om, _storage = _om(llm)
    asyncio.run(om.buffer("t", "r", _screenshot_turns()))
    assert [(c["kind"], c["payload"]["stage"]) for c in captured] == [(MEMORY_PASS_FAILED_KIND, "buffer")]


def test_a_pass_held_by_a_spend_cap_is_a_refusal_never_filed(captured) -> None:
    """Live 2026-11-18: an observer pass stopped by "daily spend cap reached" filed
    observational_memory_pass_failed. The adapter re-raises it chained (llm_adapter), and a hold is
    an expected refusal the gate already recorded — never a system error. A real fault still files."""
    from matrx_ai.providers.guardrail_gate import GuardrailStopError

    stop = GuardrailStopError(
        kind="limit",
        subject_kind="system_process",
        subject_id="memory.observer",
        limit=200000,
        observed=200701,
        message="Stopped: limit — daily spend cap reached (200,701 points of 200,000 points).",
        pauses=True,
    )

    async def llm(**_: Any):
        raise RuntimeError(f"GuardrailStopError: {stop}") from stop

    om, _storage = _om(llm)
    asyncio.run(om.process_output_step(_screenshot_turns(), "t", "r"))
    assert captured == [], captured
