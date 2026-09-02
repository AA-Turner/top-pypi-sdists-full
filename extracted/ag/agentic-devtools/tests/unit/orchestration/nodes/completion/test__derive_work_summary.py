"""Tests for _derive_work_summary."""

from __future__ import annotations

from typing import Any, cast

from agentic_devtools.orchestration.nodes.completion import _derive_work_summary
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


class TestDeriveWorkSummary:
    """Tests for work summary derivation from checklist items and state."""

    def _state(self, **kwargs: Any) -> WorkOnIssueState:
        return cast(WorkOnIssueState, kwargs)

    def test_returns_empty_string_when_no_data(self) -> None:
        result = _derive_work_summary(self._state(), [])
        assert result == ""

    def test_includes_completed_checklist_items(self) -> None:
        items = [
            {"description": "Implement feature", "is_complete": True},
            {"description": "Write tests", "is_complete": False},
        ]
        result = _derive_work_summary(self._state(), items)
        assert "Implement feature" in result
        assert "Write tests" not in result

    def test_skips_whitespace_only_descriptions(self) -> None:
        items = [{"description": "  \t  ", "is_complete": True}]
        result = _derive_work_summary(self._state(), items)
        assert result == ""

    def test_includes_affected_paths(self) -> None:
        state = self._state(affected_paths=["src/a.py", "src/b.py"])
        result = _derive_work_summary(state, [])
        assert "src/a.py" in result
        assert "src/b.py" in result

    def test_deduplicates_affected_paths(self) -> None:
        state = self._state(affected_paths=["src/a.py", "src/a.py", "src/b.py"])
        result = _derive_work_summary(state, [])
        assert result.count("src/a.py") == 1

    def test_skips_empty_paths(self) -> None:
        state = self._state(affected_paths=["src/a.py", "", "  "])
        result = _derive_work_summary(state, [])
        assert "src/a.py" in result
        assert result.count("-") == 1

    def test_falls_back_to_implementation_log_count(self) -> None:
        state = self._state(
            affected_paths="not-a-list",
            implementation_log=[{"status": "completed"}, {"status": "completed"}, {"status": "failed"}],
        )
        result = _derive_work_summary(state, [])
        assert "2 implementation step(s)" in result

    def test_both_completed_items_and_paths_appear_in_summary(self) -> None:
        items = [{"description": "Refactor module", "is_complete": True}]
        state = self._state(affected_paths=["lib/mod.py"])
        result = _derive_work_summary(state, items)
        assert "Refactor module" in result
        assert "lib/mod.py" in result
