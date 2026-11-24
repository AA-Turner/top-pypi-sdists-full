"""A RUN-END NOTICE NEVER REACHES THE NEXT RUN AS CURRENT (P8-RUNS 2026-11-15).

Live defect (Company Setup stranger, conversation 2015130e): the run stopped at its budget with the host notice
"ALL TOOLS ARE NOW DISABLED ... only this one reply fits" stored in the chat; the person typed "continue", the new
run got its tools and a fresh budget back, but the model read the stale notice and answered with a status line.
The wire now retires a run-end notice the person has spoken after; the saved row never changes; a notice of the
CURRENT run (no person turn after it) still goes out as written.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.message_config import host_authored_user_turn
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
from matrx_ai.config.spent_run_notices import SPENT_RUN_NOTICE
from matrx_ai.config.unified_config import UnifiedConfig

WRAP_UP = (
    "SYSTEM NOTICE (not from the user): this run has used 26,614 points of its 40,000 points budget, and only this "
    "one reply fits. ALL TOOLS ARE NOW DISABLED: do not attempt any tool call."
)


def _config(*, continued: bool) -> UnifiedConfig:
    config = UnifiedConfig(
        model="claude-sonnet-4-6",
        system_instruction="You help.",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": "Set up my social media agency"}]},
            {"role": "assistant", "content": [{"type": "text", "text": "Building the Posts table."}]},
        ],
    )
    config.messages.append(host_authored_user_turn(WRAP_UP, reason="budget_wrap_up"))
    if continued:
        config.messages.append({"role": "assistant", "content": [{"type": "text", "text": "Stopped at the budget."}]})
        config.messages.append({"role": "user", "content": [{"type": "text", "text": "continue"}]})
    return config


def _texts(config: UnifiedConfig) -> list[str]:
    return [getattr(b, "text", "") for m in config.messages for b in (m.content or [])]


@pytest.mark.asyncio
async def test_continue_after_a_budget_wrap_up_is_a_new_run_with_its_tools() -> None:
    config = _config(continued=True)
    prep = await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    wire = _texts(prep.wire_config or config)
    assert not any("ALL TOOLS ARE NOW DISABLED" in t for t in wire), wire
    assert SPENT_RUN_NOTICE in wire
    assert wire[-1] == "continue"
    assert "spent_run_notices" in prep.steps
    # THE SAVED ROW IS NEVER CHANGED
    assert any("ALL TOOLS ARE NOW DISABLED" in t for t in _texts(config))


@pytest.mark.asyncio
async def test_the_current_runs_wrap_up_goes_out_as_written() -> None:
    config = _config(continued=False)
    prep = await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    wire = _texts(prep.wire_config or config)
    assert wire[-1] == WRAP_UP
    assert SPENT_RUN_NOTICE not in wire
