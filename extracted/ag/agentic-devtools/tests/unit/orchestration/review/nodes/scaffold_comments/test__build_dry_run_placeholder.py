"""Tests for ``_build_dry_run_placeholder()``."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.scaffold_comments import (
    _build_dry_run_placeholder,
)


class TestBuildDryRunPlaceholder:
    """NFR-003: dry-run placeholder ReviewState construction."""

    def test_populates_metadata_from_state(self) -> None:
        """Metadata fields reflect the graph state values."""
        state = {
            "pr_id": 123,
            "repo_id": "repo-guid",
            "project": "MyProject",
            "organization": "https://dev.azure.com/org",
            "commit_hash": "abc123def",
        }
        result = _build_dry_run_placeholder(state, "my-repo", "gpt-4o", [])
        assert result.prId == 123
        assert result.repoId == "repo-guid"
        assert result.repoName == "my-repo"
        assert result.project == "MyProject"
        assert result.organization == "https://dev.azure.com/org"
        assert result.commitHash == "abc123def"
        assert result.modelId == "gpt-4o"

    def test_overall_summary_has_zero_ids(self) -> None:
        """Thread and comment IDs are zero in placeholder."""
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", [])
        assert result.overallSummary.threadId == 0
        assert result.overallSummary.commentId == 0
        assert result.overallSummary.status == "unreviewed"

    def test_file_entries_have_zero_ids(self) -> None:
        """File entry thread/comment IDs are zero in placeholder."""
        files = [{"path": "/src/main.py"}]
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", files)
        assert "/src/main.py" in result.files
        entry = result.files["/src/main.py"]
        assert entry.threadId == 0
        assert entry.commentId == 0
        assert entry.status == "unreviewed"

    def test_file_entries_have_correct_folder_and_filename(self) -> None:
        """Folder is top-level directory, fileName is basename."""
        files = [{"path": "/src/app/component.py"}]
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", files)
        entry = result.files["/src/app/component.py"]
        assert entry.folder == "src"
        assert entry.fileName == "component.py"

    def test_root_level_file_gets_root_folder(self) -> None:
        """Files without a directory get folder='root'."""
        files = [{"path": "/README.md"}]
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", files)
        entry = result.files["/README.md"]
        assert entry.folder == "root"

    def test_session_has_langchain_engine(self) -> None:
        """Placeholder session has engine='langchain'."""
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "gpt-4o", [])
        assert len(result.sessions) == 1
        assert result.sessions[0].engine == "langchain"
        assert result.sessions[0].status == "in_progress"
        assert result.sessions[0].modelId == "gpt-4o"
        assert result.sessions[0].sessionId == "dry-run-placeholder"

    def test_empty_files_list_produces_empty_entries(self) -> None:
        """Zero files produces valid state with empty files dict."""
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", [])
        assert len(result.files) == 0
        assert result.overallSummary.threadId == 0

    def test_skips_files_without_path(self) -> None:
        """Files without a 'path' key are skipped."""
        files = [{"path": "/src/main.py"}, {}]
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", files)
        assert len(result.files) == 1
        assert "/src/main.py" in result.files

    def test_skips_non_dict_and_blank_paths(self) -> None:
        """Non-dict file entries and blank string paths are skipped."""
        files = [{"path": "/src/main.py"}, None, "bad", {"path": "   "}]
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", files)
        assert len(result.files) == 1
        assert "/src/main.py" in result.files

    def test_normalizes_file_paths(self) -> None:
        """File paths are normalized with leading slash."""
        files = [{"path": "src/main.py"}]
        result = _build_dry_run_placeholder({"pr_id": 1}, "", "m", files)
        assert "/src/main.py" in result.files
        assert "src/main.py" not in result.files

    def test_latest_iteration_id_from_state(self) -> None:
        """Latest iteration ID is carried from state."""
        state = {"pr_id": 1, "latest_iteration_id": 7}
        result = _build_dry_run_placeholder(state, "", "m", [])
        assert result.latestIterationId == 7

    def test_non_int_latest_iteration_id_defaults_to_zero(self) -> None:
        """Non-int latest_iteration_id defaults to 0."""
        state = {"pr_id": 1, "latest_iteration_id": "not-an-int"}
        result = _build_dry_run_placeholder(state, "", "m", [])
        assert result.latestIterationId == 0
