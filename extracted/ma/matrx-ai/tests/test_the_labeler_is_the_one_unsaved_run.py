"""THE ONE UNSAVED RUN (owner ruling 2026-10-23): only the conversation labeler is not recorded.

* the labeler's held call is sent with ``store=False``;
* the executor's refusal admits exactly the labeler's two mandate keys and refuses every other
  machine caller.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.agent_runners.conversation_labeler as runner
from matrx_ai.code_call_mandate_keys import (
    CONVERSATION_LABEL_AGENT_RUN_MANDATE,
    CONVERSATION_LABEL_CHAT_MANDATE,
)
from matrx_ai.orchestrator.unsaved_runs import (
    UNSAVED_RUN_EXEMPTION,
    MachineUnsavedRunRefused,
    refuse_machine_unsaved_run,
)


async def test_the_labeler_sends_its_held_call_unsaved(monkeypatch: pytest.MonkeyPatch) -> None:
    sent: list[dict[str, Any]] = []

    async def hold(*_a: Any, **_k: Any) -> Any:
        return SimpleNamespace(model="m")

    async def run(_held: Any, **kwargs: Any) -> Any:
        sent.append(kwargs)
        return SimpleNamespace(final_text='{"label": "x"}')

    import matrx_ai.mandates as mandates

    monkeypatch.setattr(mandates, "hold_code_call", hold)
    monkeypatch.setattr(mandates, "run_held_call", run)
    result = await runner._run_labeler(CONVERSATION_LABEL_CHAT_MANDATE, {}, conversation_id=None)
    assert result.success, result.error
    assert sent == [{"store": False}]


def test_the_exemption_is_exactly_the_labeler() -> None:
    assert UNSAVED_RUN_EXEMPTION == {CONVERSATION_LABEL_CHAT_MANDATE, CONVERSATION_LABEL_AGENT_RUN_MANDATE}
    for key in UNSAVED_RUN_EXEMPTION:
        refuse_machine_unsaved_run(door="execute_ai_request", metadata={"mandate_key": key})


@pytest.mark.parametrize("key", ["search_decide.brand_result", "conversation.condense", ""])
def test_every_other_machine_caller_is_refused(key: str) -> None:
    with pytest.raises(MachineUnsavedRunRefused):
        refuse_machine_unsaved_run(door="execute_ai_request", metadata={"mandate_key": key})
