"""Unit tests for TaskResult structured result contracts (#1316)."""

from __future__ import annotations

from anteroom.services.task_result import TaskResult

# ---------------------------------------------------------------------------
# Serialization round-trip
# ---------------------------------------------------------------------------


def test_to_dict_round_trip() -> None:
    original = TaskResult(
        status="completed",
        summary="hello world",
        exit_code=0,
        error=None,
        tool_calls=["read_file", "bash"],
        output_pointer="task-abc-123",
        truncated=False,
        duration_seconds=1.5,
    )
    restored = TaskResult.from_dict(original.to_dict())
    assert restored == original


# ---------------------------------------------------------------------------
# LLM view trust boundary
# ---------------------------------------------------------------------------


def test_to_llm_dict_strips_output_pointer() -> None:
    result = TaskResult(
        status="completed",
        summary="done",
        exit_code=0,
        error=None,
        tool_calls=[],
        output_pointer="task-secret-id",
        truncated=False,
        duration_seconds=0.5,
    )
    llm_view = result.to_llm_dict()
    assert "output_pointer" not in llm_view


def test_to_llm_dict_truncates_tool_calls() -> None:
    # 25 tool calls — should be capped at 20
    tool_calls = [f"tool_{i}" for i in range(25)]
    result = TaskResult(
        status="completed",
        summary="done",
        exit_code=0,
        error=None,
        tool_calls=tool_calls,
        output_pointer="run-xyz",
        truncated=False,
        duration_seconds=2.0,
    )
    llm_view = result.to_llm_dict()
    assert len(llm_view["tool_calls"]) == 20
    assert llm_view["tool_calls"] == tool_calls[:20]


# ---------------------------------------------------------------------------
# from_shell_task factory
# ---------------------------------------------------------------------------


def test_from_shell_task_success() -> None:
    result = TaskResult.from_shell_task(
        exit_code=0,
        stdout="output line\n",
        stderr="",
        duration=1.234,
        task_id="task-001",
    )
    assert result.status == "completed"
    assert result.exit_code == 0
    assert result.error is None
    assert "output line" in result.summary
    assert result.output_pointer == "task-001"
    assert result.tool_calls == []


def test_from_shell_task_failure() -> None:
    result = TaskResult.from_shell_task(
        exit_code=1,
        stdout="",
        stderr="something went wrong",
        duration=0.1,
        task_id="task-002",
    )
    assert result.status == "failed"
    assert result.exit_code == 1
    assert result.error is not None
    assert "something went wrong" in result.error
    assert result.output_pointer == "task-002"


def test_from_shell_task_summary_truncation() -> None:
    long_stdout = "x" * 500
    result = TaskResult.from_shell_task(
        exit_code=0,
        stdout=long_stdout,
        stderr="",
        duration=0.5,
        task_id="task-003",
    )
    assert len(result.summary) == 200
    assert result.truncated is True


# ---------------------------------------------------------------------------
# from_subagent_result factory
# ---------------------------------------------------------------------------


def test_from_subagent_result_success() -> None:
    subagent_result = {
        "output": "Analysis complete. Found 3 issues.",
        "tool_calls_made": ["read_file", "grep", "bash"],
        "model_used": "gpt-4o",
        "truncated": False,
        "error": None,
        "elapsed_seconds": 5.0,
    }
    result = TaskResult.from_subagent_result(subagent_result, run_id="run-abc")
    assert result.status == "completed"
    assert result.exit_code is None
    assert result.error is None
    assert "Analysis complete" in result.summary
    assert result.tool_calls == ["read_file", "grep", "bash"]
    assert result.output_pointer == "run-abc"
    assert result.truncated is False


def test_from_subagent_result_error() -> None:
    subagent_result = {
        "output": "",
        "tool_calls_made": [],
        "model_used": None,
        "truncated": False,
        "error": "API rate limit exceeded",
        "elapsed_seconds": 0.8,
    }
    result = TaskResult.from_subagent_result(subagent_result, run_id="run-def")
    assert result.status == "failed"
    assert result.error == "API rate limit exceeded"
    assert result.output_pointer == "run-def"


# ---------------------------------------------------------------------------
# from_dict with missing fields
# ---------------------------------------------------------------------------


def test_from_dict_missing_fields_uses_defaults() -> None:
    # Simulate an older record that pre-dates some fields
    old_dict: dict = {"status": "completed", "summary": "ok"}
    result = TaskResult.from_dict(old_dict)
    assert result.status == "completed"
    assert result.summary == "ok"
    assert result.exit_code is None
    assert result.error is None
    assert result.tool_calls == []
    assert result.output_pointer is None
    assert result.truncated is False
    assert result.duration_seconds == 0.0
