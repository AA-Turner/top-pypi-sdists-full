"""Tests for ReviewGraphState TypedDict."""

import typing

from agentic_devtools.orchestration.review.state import ReviewGraphState


class TestReviewGraphState:
    """Tests for ReviewGraphState TypedDict validation."""

    def test_can_create_minimal_state(self) -> None:
        """A minimal state dict is valid for ReviewGraphState."""
        state: ReviewGraphState = {
            "pr_id": 123,
            "files": [],
            "threads": [],
            "config": {},
            "file_results": [],
            "errors": [],
        }
        assert state["pr_id"] == 123
        assert state["files"] == []

    def test_state_accepts_all_fields(self) -> None:
        """All defined fields can be set on ReviewGraphState."""
        state: ReviewGraphState = {
            "pr_id": 42,
            "repo_id": "repo-guid",
            "project": "MyProject",
            "organization": "https://dev.azure.com/org",
            "commit_hash": "abc123",
            "files": [{"path": "/src/a.py"}],
            "threads": [{"id": 1}],
            "config": {"review": {}},
            "iterations": [{"id": 1, "description": "Initial push"}],
            "jira_issue": {"key": "PROJ-1", "summary": "Fix bug"},
            "review_state_path": "/tmp/review-state.json",
            "file_results": [],
            "overall_decision": "approve",
            "summary": "All good",
            "errors": [],
            "source_context_enabled": True,
            "llm_config_path": "/repo/.agdt/config/llm-providers.yml",
            "model_config_raw": {"default-model": "gpt-4o"},
        }
        assert state["overall_decision"] == "approve"
        assert state["source_context_enabled"] is True
        assert state["llm_config_path"] == "/repo/.agdt/config/llm-providers.yml"
        assert state["iterations"] == [{"id": 1, "description": "Initial push"}]
        assert state["jira_issue"] == {"key": "PROJ-1", "summary": "Fix bug"}

    def test_state_is_typed_dict(self) -> None:
        """ReviewGraphState is a TypedDict subclass."""
        assert hasattr(ReviewGraphState, "__annotations__")
        annotations = ReviewGraphState.__annotations__
        assert "pr_id" in annotations
        assert "file_results" in annotations
        assert "errors" in annotations
        assert "_provider_factory" not in annotations

    def test_file_results_uses_last_writer_wins_semantics(self) -> None:
        """file_results is a plain list, not Annotated with operator.add.

        review_files_node writes the entire list in a single update; using
        append (Annotated[list, operator.add]) semantics would concatenate
        the full list onto any prior value on graph retry/resume, duplicating
        results.  This test guards against regressing that annotation.
        """
        ann = typing.get_type_hints(ReviewGraphState, include_extras=True)
        file_results_type = ann["file_results"]
        # Must NOT be an Annotated type (which would carry operator.add metadata)
        assert typing.get_origin(file_results_type) is not typing.Annotated

    def test_errors_uses_append_semantics(self) -> None:
        """errors is Annotated with operator.add for accumulation across nodes."""
        ann = typing.get_type_hints(ReviewGraphState, include_extras=True)
        errors_type = ann["errors"]
        assert typing.get_origin(errors_type) is typing.Annotated
