"""A child agent refused for empty required inputs is the CALLER's to fix, never a platform error.

Live 2026-11-12: agent_call → 'DB Cartographer' without ``task`` returned ``agent_execution`` and
the tool executor filed a ``tool_execution_failed`` system_error each time. SUT: the real
``child_required_inputs_refusal`` mapping and the executor's real ``_is_expected_domain_failure``."""

from __future__ import annotations

from matrx_ai.agents.required_variables import RequiredVariablesMissing
from matrx_ai.tools.executor import _is_expected_domain_failure
from matrx_ai.tools.implementations.agent_call import child_required_inputs_refusal


def test_missing_required_inputs_map_to_an_expected_refusal() -> None:
    exc = RequiredVariablesMissing(["task", "scope"], agent_name="DB Cartographer")
    refusal = child_required_inputs_refusal(exc, "DB Cartographer")
    assert refusal is not None
    error_type, message, action = refusal
    assert error_type == "required_variables_missing"
    assert "task, scope" in message and "task, scope" in action
    assert _is_expected_domain_failure(tool_name="agent", error_type=error_type, message=message)
    assert _is_expected_domain_failure(tool_name="agent_call", error_type=error_type, message=message)


def test_any_other_child_failure_is_still_filed() -> None:
    assert child_required_inputs_refusal(RuntimeError("provider down"), "X") is None
    assert child_required_inputs_refusal(None, "X") is None
    assert not _is_expected_domain_failure(tool_name="agent", error_type="agent_execution", message="boom")


def test_the_persons_own_setup_is_not_a_platform_error() -> None:
    """Live 2026-11-09/10: desktop_contacts with no computer connected, and memory in a temporary chat,
    each filed a tool_execution_failed system_error. Both are the person's setup, said to the model."""
    assert _is_expected_domain_failure(tool_name="desktop_contacts", error_type="no_computer", message="x")
    assert _is_expected_domain_failure(tool_name="memory", error_type="person_memory_off", message="x")
    # The owner ruling stands: the nesting limit stays red.
    assert not _is_expected_domain_failure(tool_name="agent", error_type="recursion_limit", message="x")
