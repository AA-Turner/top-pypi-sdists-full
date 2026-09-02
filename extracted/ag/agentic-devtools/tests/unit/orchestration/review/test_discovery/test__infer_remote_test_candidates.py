"""Tests for _infer_remote_test_candidates."""

from __future__ import annotations

from agentic_devtools.orchestration.review.test_discovery import _infer_remote_test_candidates


class TestInferRemoteTestCandidates:
    """Tests for _infer_remote_test_candidates."""

    def test_non_python_path_returns_empty(self) -> None:
        """Non-Python source paths have no inferred candidates."""
        assert _infer_remote_test_candidates("docs/README.md", "# doc\n") == []

    def test_non_symbol_top_level_nodes_do_not_create_1to1_candidates(self) -> None:
        """Only top-level functions and classes contribute 1:1:1 candidates."""
        assert _infer_remote_test_candidates("agentic_devtools/state.py", "VALUE = 1\n") == ["tests/test_state.py"]
