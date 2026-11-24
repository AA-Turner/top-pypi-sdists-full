"""THE BACKGROUND-HELPER CAP IS NEVER A PLATFORM ERROR (2026-11-19).

Live: a ``tool_execution_failed`` row "agent (limit_reached): 8 background agents are already
running here (the limit is 8). Wait for one to report back, or stop one with task_stop." The cap
is a limit by design (``aidream/services/agent_harness/children.py`` ``_background_cap_refusal``)
and the sealed real test expects starts past it to end ``limit_reached``; the model reads the
sentence and waits or stops one. Only the two tools the cap guards are spared: the same code from
any other tool is still filed.

SUT: the executor's real ``_is_expected_domain_failure``.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.executor import _is_expected_domain_failure

SENTENCE = (
    "8 background agents are already running here (the limit is 8). "
    "Wait for one to report back, or stop one with task_stop."
)


@pytest.mark.parametrize("tool_name", ["agent", "send_message"])
def test_the_background_cap_is_tool_feedback(tool_name: str) -> None:
    assert _is_expected_domain_failure(tool_name=tool_name, error_type="limit_reached", message=SENTENCE)


def test_limit_reached_from_another_tool_is_still_filed() -> None:
    assert not _is_expected_domain_failure(tool_name="web_search", error_type="limit_reached", message="x")


def test_a_real_agent_tool_failure_is_still_filed() -> None:
    assert not _is_expected_domain_failure(tool_name="agent", error_type="execution", message="boom")
