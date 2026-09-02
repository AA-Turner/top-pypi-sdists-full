"""Tests for _build_completion_data."""

from typing import Any, cast

from agentic_devtools.orchestration.nodes.completion import _build_completion_data
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


class TestBuildCompletionData:
    """Tests for completion formatter input derivation."""

    def test_prefers_explicit_summary_and_quality_gates(self) -> None:
        state: dict[str, Any] = {
            "what_was_done": "Explicit summary",
            "quality_gates": [{"name": "Lint", "status": "pass", "details": "ok"}],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="https://example.com/pr/1",
            checklist_items=[],
            token_usage_prompt=1,
            token_usage_completion=2,
        )

        assert result["what_was_done"] == "Explicit summary"
        assert result["quality_gates"] == [{"name": "Lint", "status": "pass", "details": "ok"}]

    def test_derives_summary_from_completed_items_and_unique_paths(self) -> None:
        state: dict[str, Any] = {
            "affected_paths": ["src/a.py", "", "src/a.py", 5, "src/b.py"],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[
                {"description": "Implement feature", "is_complete": True},
                {"description": "   ", "is_complete": True},
                {"description": "Write tests", "is_complete": True},
                {"description": "Incomplete", "is_complete": False},
                {"is_complete": True},
            ],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert "Implement feature" in result["what_was_done"]
        assert "Write tests" in result["what_was_done"]
        assert result["what_was_done"].count("src/a.py") == 1
        assert "src/b.py" in result["what_was_done"]
        assert result["quality_gates"] == []

    def test_derives_summary_from_paths_when_no_completed_items(self) -> None:
        state: dict[str, Any] = {
            "affected_paths": ["src/only.py"],
            "implementation_log": "not-a-list",
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["what_was_done"] == "Affected files:\n- src/only.py"

    def test_falls_back_to_implementation_log_count_without_items_or_paths(self) -> None:
        state: dict[str, Any] = {
            "affected_paths": "not-a-list",
            "implementation_log": [{"status": "completed"}, {"status": "failed"}],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["what_was_done"] == "Completed 1 implementation step(s)."

    def test_returns_empty_summary_when_no_derived_inputs_exist(self) -> None:
        state: dict[str, Any] = {
            "affected_paths": "not-a-list",
            "implementation_log": "not-a-list",
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["what_was_done"] == ""

    def test_derives_and_truncates_quality_gate_details(self) -> None:
        state: dict[str, Any] = {
            "quality_gates": "invalid",
            "verification_output": "word " * 60,
            "events": [{"event": "verification_passed", "timestamp": "2026-01-01T00:00:00Z"}],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["quality_gates"][0]["name"] == "Targeted checks"
        assert result["quality_gates"][0]["status"] == "pass"
        assert result["quality_gates"][0]["details"].endswith("...")

    def test_derives_failed_quality_gate_status_from_verification_event(self) -> None:
        state: dict[str, Any] = {
            "quality_gates": "invalid",
            "verification_output": "targeted checks failed",
            "events": [{"event": "verification_failed", "timestamp": "2026-01-01T00:00:00Z"}],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["quality_gates"][0]["status"] == "fail"

    def test_missing_verification_events_fails_closed(self) -> None:
        state: dict[str, Any] = {
            "quality_gates": "invalid",
            "verification_output": "checks output present",
            "events": [],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["quality_gates"][0]["status"] == "fail"

    def test_non_dict_or_irrelevant_events_fall_back_to_fail(self) -> None:
        state: dict[str, Any] = {
            "quality_gates": "invalid",
            "verification_output": "checks output present",
            "events": [123, {"event": "implementation_completed", "timestamp": "2026-01-01T00:00:00Z"}],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["quality_gates"][0]["status"] == "fail"

    def test_non_list_events_fall_back_to_fail(self) -> None:
        state: dict[str, Any] = {
            "quality_gates": "invalid",
            "verification_output": "checks output present",
            "events": {"event": "verification_passed"},
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["quality_gates"][0]["status"] == "fail"

    def test_whitespace_padded_path_duplicate_is_deduplicated(self) -> None:
        """Whitespace-padded duplicate paths (e.g. ' src/a.py' vs 'src/a.py') must not
        produce double entries after normalization."""
        state: dict[str, Any] = {
            "affected_paths": [" src/a.py", "src/a.py", "  src/b.py  "],
        }
        result = _build_completion_data(
            cast(WorkOnIssueState, state),
            pr_url="",
            checklist_items=[],
            token_usage_prompt=0,
            token_usage_completion=0,
        )

        assert result["what_was_done"].count("src/a.py") == 1
        assert result["what_was_done"].count("src/b.py") == 1
