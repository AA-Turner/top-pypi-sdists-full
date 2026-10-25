"""PB-03 defect 7: every drop, clamp and translation is visible to a person AND stored.

Live 2026-10-16: the three PB-03 copies lost or changed a dozen settings each
(top_k dropped, max_output_tokens 400000 -> the model maximum, reasoning translated
into each model's own shape) and the only trace was a yellow server-log banner. The
person saw one ``unrecognized_config`` line; the stored request held nothing.

Now the chat seam (``resolve_outbound_params``) — and the session, structural and
media seams through the same function — publishes ONE structured list:

    settings_adjustments = [{key, action: drop|clamp|translate, from, to, reason, ...}]

* on the run's ExecutionState, which the executor writes into
  ``chat.request_snapshot.metadata.settings_adjustments`` beside the wire payload;
* as one typed stream event, ``info`` code ``settings_adjusted`` (same event
  vocabulary as ``setting_not_supported``, which still fires only for an
  UNEXPECTED drop — Arman 2026-08-17: conversions are not warnings).
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.orchestrator.execution_state import ExecutionState, set_execution_state
from matrx_ai.providers.outbound_params import resolve_outbound_params

FIXTURE = Path(__file__).parent / "fixtures" / "pb03_offering_rules.json"


class _Recorder:
    def __init__(self) -> None:
        self.infos: list[Any] = []
        self.warnings: list[Any] = []

    async def send_info(self, payload: Any) -> None:
        self.infos.append(payload)

    async def send_warning(self, payload: Any) -> None:
        self.warnings.append(payload)


def _gemini_controls() -> CompiledControlsMap:
    rules = json.loads(FIXTURE.read_text())["google_gemini_flash_lite_latest"]["rules"]
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()}
    ).with_output_maximum(65536)


def _kitchen_sink_config() -> UnifiedConfig:
    return UnifiedConfig.from_dict(
        {
            "model": "gemini-flash-lite-latest",
            "messages": [],
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 40,
            "seed": 4471,
            "stop_sequences": ["ZZ-HALT"],
            "reasoning_effort": "high",
            "thinking_budget": 2048,
            "include_thoughts": True,
            "max_output_tokens": 400000,
        }
    )


async def test_adjustments_are_stored_and_streamed() -> None:
    recorder = _Recorder()
    ctx = AppContext(emitter=recorder, user_id="u", request_id="r", conversation_id="c")  # type: ignore[arg-type]
    ctx_token = set_app_context(ctx)
    state = ExecutionState()
    set_execution_state(state)
    try:
        params = resolve_outbound_params(_kitchen_sink_config(), _gemini_controls())
        await asyncio.sleep(0.05)  # the stream event is fire-and-forget
    finally:
        clear_app_context(ctx_token)

    stored = state.settings_adjustments
    assert stored, "nothing stored for the snapshot"
    by_key = {row["key"]: row for row in stored}
    assert by_key["top_k"]["action"] == "drop"
    assert by_key["max_output_tokens"]["action"] == "clamp"
    assert (by_key["max_output_tokens"]["from"], by_key["max_output_tokens"]["to"]) == (400000, 65536)
    # flash-lite-latest is a Gemini 3.x model (gemini_3 mode, thinking_level): a raw budget is
    # dropped with a record, the effort rides as the level.
    assert by_key["thinking_budget"]["action"] in {"translate", "drop"}
    assert params["thinking_config"].get("thinking_level")
    assert "thinking_config" in params
    for row in stored:
        assert set(row) >= {"key", "action", "from", "to", "reason"}
    json.dumps(stored)

    events = [p for p in recorder.infos if p.code == "settings_adjusted"]
    assert len(events) == 1
    streamed = events[0].metadata["settings_adjustments"]
    # Shown: only what changed for the person; a value carried in the provider's own
    # shape stays in the record and out of the notice.
    assert {r["key"] for r in streamed} == {r["key"] for r in stored if not r["faithful"]}
    assert "top_k" in events[0].system_message


async def test_one_event_per_request_across_iterations() -> None:
    recorder = _Recorder()
    ctx = AppContext(emitter=recorder, user_id="u", request_id="r", conversation_id="c")  # type: ignore[arg-type]
    ctx_token = set_app_context(ctx)
    try:
        for _ in range(3):  # each loop iteration runs the seam in its own task copy
            task = asyncio.create_task(_one_pass())
            await task
        await asyncio.sleep(0.05)
    finally:
        clear_app_context(ctx_token)
    assert len([p for p in recorder.infos if p.code == "settings_adjusted"]) == 1


async def _one_pass() -> None:
    set_execution_state(ExecutionState())
    resolve_outbound_params(_kitchen_sink_config(), _gemini_controls())


def _claude_controls() -> CompiledControlsMap:
    rules = json.loads(FIXTURE.read_text())["anthropic_claude_haiku_5_5"]["rules"]
    return CompiledControlsMap(rules={k: ControlRule.model_validate(v) for k, v in rules.items()})


async def test_a_faithful_translation_is_recorded_never_announced() -> None:
    """Arman 2026-10-24: nearly every Anthropic request said "settings were adjusted"
    because effort=medium was sent as Anthropic's own output_config.effort=medium."""
    recorder = _Recorder()
    ctx = AppContext(emitter=recorder, user_id="u", request_id="r", conversation_id="c")  # type: ignore[arg-type]
    ctx_token = set_app_context(ctx)
    state = ExecutionState()
    set_execution_state(state)
    try:
        resolve_outbound_params(
            UnifiedConfig.from_dict(
                {"model": "claude-haiku-5-5", "messages": [], "reasoning_effort": "medium"}
            ),
            _claude_controls(),
        )
        await asyncio.sleep(0.05)
    finally:
        clear_app_context(ctx_token)
    stored = state.settings_adjustments or []
    assert any(r["key"] == "reasoning_effort" and r["faithful"] for r in stored), stored
    assert not [p for p in recorder.infos if p.code == "settings_adjusted"]


def test_faithful_means_unchanged_in_meaning() -> None:
    from matrx_ai.catalog.controls import _carried_faithfully

    levels = {"none", "minimal", "low", "medium", "high"}
    # Same word in the provider's shape, or the same level on another scale: faithful.
    assert _carried_faithfully({"output_config": {"effort": "medium"}}, "medium", levels)
    assert _carried_faithfully({"thinking": {"type": "enabled", "budget_tokens": 1024}}, "low", levels)
    # A different level of the vocabulary is a real change and is announced.
    assert not _carried_faithfully({"thinking_config": {"thinking_level": "minimal"}}, "none", levels)
    # An off is faithful only as the provider's own off — never as thinking that still runs.
    assert _carried_faithfully({"thinking": {"type": "disabled"}}, "none", levels)
    assert not _carried_faithfully({"thinking": {"type": "enabled", "budget_tokens": 1024}}, "none", levels)
    # A number not sent as itself was capped; with no vocabulary loaded nothing is assumed.
    assert not _carried_faithfully({"thinking_config": {"thinking_budget": 4096}}, 8192, levels)
    assert not _carried_faithfully({"thinking_config": {"thinking_level": "minimal"}}, "none", set())
