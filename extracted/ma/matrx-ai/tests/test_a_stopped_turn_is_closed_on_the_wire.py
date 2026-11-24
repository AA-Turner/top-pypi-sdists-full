"""A stopped reply cut inside an open fence is closed on the WIRE; the saved turn never changes (2026-11-14).

Live defect: Stop pressed inside a ```python block, then "continue": the model carried on inside the code, and its
later closing fence inverted every fence after it. The wire now closes the open region and tells the model.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
from matrx_ai.config.stopped_turn import close_stopped_text
from matrx_ai.config.unified_config import UnifiedConfig

MARKER = "\n\n[⚠️ Response stopped by the person before completion.]"


def _config(assistant_text: str, *, stopped_meta: bool = True) -> UnifiedConfig:
    assistant: dict = {"role": "assistant", "content": [{"type": "text", "text": assistant_text}]}
    if stopped_meta:
        assistant["metadata"] = {"stopped": True}
    return UnifiedConfig(
        model="claude-sonnet-4-6",
        system_instruction="You help.",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": "Write a script"}]},
            assistant,
            {"role": "user", "content": [{"type": "text", "text": "continue"}]},
        ],
    )


def _assistant_text(config: UnifiedConfig) -> str:
    return next(m for m in config.messages if m.role == "assistant").content[0].text


@pytest.mark.asyncio
@pytest.mark.parametrize("stopped_meta", [True, False], ids=["metadata", "marker-only"])
async def test_a_stopped_turn_cut_in_a_fence_is_closed_on_the_wire_only(stopped_meta: bool) -> None:
    saved = "Here:\n```python\nimport os\nx =" + MARKER
    config = _config(saved, stopped_meta=stopped_meta)
    prep = await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    wire = _assistant_text(prep.wire_config)
    before_marker = wire.split("[⚠️")[0]
    assert before_marker.rstrip("\n").endswith("```"), wire
    assert before_marker.count("```") == 2, wire
    assert "stopped partway through a python code block" in wire
    assert "stopped_turn_regions" in prep.steps
    # THE SAVED ROW IS NEVER CHANGED
    assert _assistant_text(config) == saved


@pytest.mark.asyncio
async def test_a_stopped_turn_with_nothing_open_is_sent_as_it_is() -> None:
    saved = "Done.\n```py\nx\n```\nAll good" + MARKER
    prep_cfg = _config(saved)
    prep = await prepare_for_send(prep_cfg, stage=STAGE_LOOP, policy=TrimPolicy())
    assert _assistant_text(prep.wire_config or prep_cfg) == saved


@pytest.mark.asyncio
async def test_a_finished_turn_that_ends_in_a_fence_is_never_touched() -> None:
    saved = "Here:\n```python\nx ="
    prep_cfg = _config(saved, stopped_meta=False)
    prep = await prepare_for_send(prep_cfg, stage=STAGE_LOOP, policy=TrimPolicy())
    assert _assistant_text(prep.wire_config or prep_cfg) == saved


def test_math_and_svg_roots_are_closed_too() -> None:
    assert close_stopped_text("$$ x^2\n" + MARKER).split("[⚠️")[0].rstrip().endswith("$$")
    assert "</svg>" in close_stopped_text("<svg>\n<g>" + MARKER)
