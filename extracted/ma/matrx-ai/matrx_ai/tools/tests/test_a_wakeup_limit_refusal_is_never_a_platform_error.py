"""A WAKE-UP REFUSED BY ITS OWN LIMITS IS TOOL FEEDBACK, NEVER A PLATFORM ERROR (2026-11-19).

Live (phone/voice-agent): a ``tool_execution_failed`` row "schedule_wakeup (limit_reached):
2028-01-01T20:00:00+00:00 is more than 31536000s (365 days) ahead, the longest a wake-up may wait,
so none was scheduled." Every refusal ``agent_harness.wakeups.schedule`` returns (too far ahead,
unclear time, bad repeat, daily budget spent, pending cap) is a limit by design whose sentence tells
the model what to do instead; ``agent_harness_tool`` hands each one back as ``limit_reached``. Only
``schedule_wakeup`` is spared: the same code from another tool is still filed.

SUT: the executor's real ``_is_expected_domain_failure``.
"""

from __future__ import annotations

from matrx_ai.tools.executor import _is_expected_domain_failure

SENTENCE = (
    "2028-01-01T20:00:00+00:00 is more than 31536000s (365 days) ahead, the longest a wake-up "
    "may wait, so none was scheduled."
)


def test_a_wakeup_past_its_window_is_tool_feedback() -> None:
    assert _is_expected_domain_failure(tool_name="schedule_wakeup", error_type="limit_reached", message=SENTENCE)


def test_limit_reached_from_another_tool_is_still_filed() -> None:
    assert not _is_expected_domain_failure(tool_name="web_search", error_type="limit_reached", message="x")


def test_a_real_schedule_wakeup_failure_is_still_filed() -> None:
    assert not _is_expected_domain_failure(tool_name="schedule_wakeup", error_type="execution", message="boom")
