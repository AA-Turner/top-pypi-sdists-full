"""Tests for ``scaffold_comments_node()``."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.orchestration.review.nodes.scaffold_comments import scaffold_comments_node

# ---------------------------------------------------------------------------
# Fixtures & helpers
# ---------------------------------------------------------------------------


def _base_state(**overrides):
    """Build a minimal valid graph state dict."""
    base = {
        "pr_id": 123,
        "repo_id": "repo-guid",
        "project": "MyProject",
        "organization": "https://dev.azure.com/org",
        "commit_hash": "abc123def456",
        "latest_iteration_id": 3,
        "files": [
            {"path": "/src/main.py"},
            {"path": "/src/utils.py"},
        ],
    }
    base.update(overrides)
    return base


def _make_review_state(sessions=None, **kwargs):
    """Build a minimal ReviewState-like object."""
    from agentic_devtools.cli.azure_devops.review_state import (
        FileEntry,
        OverallSummary,
        ReviewState,
    )

    defaults = {
        "prId": 123,
        "repoId": "repo-guid",
        "repoName": "my-repo",
        "project": "MyProject",
        "organization": "https://dev.azure.com/org",
        "latestIterationId": 3,
        "scaffoldedUtc": "2026-01-01T00:00:00+00:00",
        "overallSummary": OverallSummary(threadId=42, commentId=43, status="unreviewed"),
        "files": {
            "/src/main.py": FileEntry(
                threadId=0,
                commentId=0,
                folder="src",
                fileName="main.py",
                status="unreviewed",
            ),
        },
        "commitHash": "abc123def456",
        "modelId": "gpt-4o",
        "sessions": sessions or [],
    }
    defaults.update(kwargs)
    return ReviewState(**defaults)


# Shared patch targets
_PATCH_GET_VALUE = "agentic_devtools.state.get_value"
_PATCH_GET_STATE_DIR = "agentic_devtools.state.get_state_dir"
_PATCH_SAVE = "agentic_devtools.cli.azure_devops.review_state.save_review_state"
_PATCH_LOAD = "agentic_devtools.cli.azure_devops.review_state.load_review_state"
_PATCH_ADO_CONFIG = "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state"
_PATCH_GET_PAT = "agentic_devtools.cli.azure_devops.auth.get_pat"
_PATCH_GET_AUTH = "agentic_devtools.cli.azure_devops.auth.get_auth_headers"
_PATCH_SCAFFOLD = "agentic_devtools.cli.azure_devops.review_scaffold.scaffold_review_threads"


# ---------------------------------------------------------------------------
# US1: First-Time PR Review Scaffolding
# ---------------------------------------------------------------------------


class TestFirstTimeScaffold:
    """US1: First-time PR review scaffolding (FR-001, FR-002, FR-007)."""

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={"Authorization": "Basic pat"})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_delegates_to_scaffold_review_threads(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-001: scaffold_review_threads() is called with correct params."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="my-repo")
        rs = _make_review_state()
        mock_scaffold.return_value = rs

        result = scaffold_comments_node(_base_state())

        mock_scaffold.assert_called_once()
        call_kwargs = mock_scaffold.call_args.kwargs
        assert call_kwargs["pull_request_id"] == 123
        assert call_kwargs["repo_id"] == "repo-guid"
        assert call_kwargs["repo_name"] == "my-repo"
        assert call_kwargs["commit_hash"] == "abc123def456"
        assert set(call_kwargs["files"]) == {"/src/main.py", "/src/utils.py"}
        assert "review_state_path" in result

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_returns_review_state_path(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-002: review_state_path is returned in output dict."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        result = scaffold_comments_node(_base_state())

        assert result["review_state_path"].endswith("review-state.json")
        assert result["errors"] == []

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_engine_langchain_set_on_new_sessions(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-002: New sessions have engine='langchain'."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        from agentic_devtools.cli.azure_devops.review_state import ReviewSession

        session = ReviewSession(
            sessionId="new-session-1",
            modelId="gpt-4o",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        rs = _make_review_state(sessions=[session])
        mock_scaffold.return_value = rs

        scaffold_comments_node(_base_state())

        saved = mock_save.call_args.args[0]
        assert saved.sessions[0].engine == "langchain"

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_zero_files_valid_state(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-002 edge case: Empty files list produces valid state."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        rs = _make_review_state(files={})
        mock_scaffold.return_value = rs

        result = scaffold_comments_node(_base_state(files=[]))

        assert "review_state_path" in result
        # Verify file_paths passed to scaffold_review_threads is empty
        assert mock_scaffold.call_args.kwargs["files"] == []

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    def test_model_id_from_model_config_raw(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-007: model_id sourced from model_config_raw with fallbacks."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        state = _base_state(model_config_raw={"default-model": "claude-opus-4.6"})

        with patch(_PATCH_GET_VALUE, return_value="fallback-model"):
            scaffold_comments_node(state)

        assert mock_scaffold.call_args.kwargs["model_id"] == "claude-opus-4.6"

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    def test_model_id_fallback_to_get_value(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-007: Falls back to get_value when model_config_raw absent."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        def get_value_side_effect(key):
            if key == "copilot.model_id":
                return "gpt-4o"
            return None

        with patch(_PATCH_GET_VALUE, side_effect=get_value_side_effect):
            scaffold_comments_node(_base_state())

        assert mock_scaffold.call_args.kwargs["model_id"] == "gpt-4o"

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_model_id_fallback_to_unknown(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-007: Defaults to 'unknown' when all sources empty."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        scaffold_comments_node(_base_state())

        assert mock_scaffold.call_args.kwargs["model_id"] == "unknown"


# ---------------------------------------------------------------------------
# US2: Idempotent Re-Scaffold on Retry
# ---------------------------------------------------------------------------


class TestIdempotentRetry:
    """US2: Idempotent re-scaffold on retry (FR-003, FR-005)."""

    @patch(_PATCH_SCAFFOLD, return_value=None)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_concurrent_session_returns_error(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-003, FR-005: None + not dry_run = concurrent session error."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        result = scaffold_comments_node(_base_state())

        assert "review_state_path" not in result
        assert any("concurrent session" in e for e in result["errors"])
        assert any("scaffold_comments:" in e for e in result["errors"])

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_existing_session_engine_preserved(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-002: Pre-existing sessions preserve their engine value."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        from agentic_devtools.cli.azure_devops.review_state import ReviewSession

        existing_session = ReviewSession(
            sessionId="existing-1",
            modelId="gpt-4o",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="completed",
            engine="default",
        )
        # Pre-load returns state with existing session
        existing_rs = _make_review_state(sessions=[existing_session])
        mock_load.return_value = existing_rs

        # scaffold_review_threads returns state with both old and new session
        new_session = ReviewSession(
            sessionId="new-2",
            modelId="gpt-4o",
            startedUtc="2026-01-02T00:00:00+00:00",
            status="in_progress",
        )
        result_rs = _make_review_state(sessions=[existing_session, new_session])
        mock_scaffold.return_value = result_rs

        scaffold_comments_node(_base_state())

        saved = mock_save.call_args.args[0]
        # Existing session keeps its original engine
        assert saved.sessions[0].engine == "default"
        # New session gets engine="langchain"
        assert saved.sessions[1].engine == "langchain"


# ---------------------------------------------------------------------------
# Error Handling & Dry-Run
# ---------------------------------------------------------------------------


class TestErrorHandling:
    """FR-005, NFR-002: Error handling and propagation."""

    def test_missing_pr_id_fatal_error(self) -> None:
        """FR-005: Missing pr_id produces scaffold_comments: error."""
        result = scaffold_comments_node({})
        assert any("pr_id is required" in e for e in result["errors"])
        assert any("scaffold_comments:" in e for e in result["errors"])
        assert "review_state_path" not in result

    def test_missing_pr_id_with_zero_value(self) -> None:
        """FR-005: pr_id=0 is rejected as non-positive."""
        result = scaffold_comments_node({"pr_id": 0})
        assert any("must be a positive integer" in e for e in result["errors"])
        assert any("scaffold_comments:" in e for e in result["errors"])
        assert "review_state_path" not in result

    def test_negative_pr_id_rejected(self) -> None:
        """FR-005: pr_id=-1 is rejected as non-positive."""
        result = scaffold_comments_node({"pr_id": -1})
        assert any("must be a positive integer" in e for e in result["errors"])
        assert any("scaffold_comments:" in e for e in result["errors"])
        assert "review_state_path" not in result

    def test_string_zero_pr_id_rejected(self) -> None:
        """FR-005: pr_id='0' (string) coerces to 0 and is rejected."""
        result = scaffold_comments_node({"pr_id": "0"})
        assert any("must be a positive integer" in e for e in result["errors"])
        assert "review_state_path" not in result

    def test_negative_string_pr_id_rejected(self) -> None:
        """FR-005: pr_id='-1' (string) coerces to -1 and is rejected."""
        result = scaffold_comments_node({"pr_id": "-1"})
        assert any("must be a positive integer" in e for e in result["errors"])
        assert "review_state_path" not in result

    def test_non_numeric_pr_id_rejected(self) -> None:
        """FR-005: Non-numeric pr_id string raises clear validation error."""
        result = scaffold_comments_node({"pr_id": "abc"})
        assert any("pr_id is required and must be a positive integer" in e for e in result["errors"])
        assert "review_state_path" not in result

    @patch(_PATCH_SCAFFOLD, side_effect=RuntimeError("API timeout"))
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_scaffold_exception_caught_and_reported(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-005: Exceptions from scaffold_review_threads produce errors."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        result = scaffold_comments_node(_base_state())

        assert "review_state_path" not in result
        assert len(result["errors"]) == 1
        error = result["errors"][0]
        assert "scaffold_comments:" in error
        assert "RuntimeError" in error
        assert "API timeout" in error
        assert "pr_id=123" in error

    @patch(_PATCH_SCAFFOLD, side_effect=OSError("disk error"))
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_unexpected_exception_caught(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-005: Unexpected exceptions caught without crash."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        result = scaffold_comments_node(_base_state())

        assert "review_state_path" not in result
        assert any("OSError" in e for e in result["errors"])

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE, side_effect=RuntimeError("disk full"))
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_save_failure_returns_error(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-005: Save failure is reported as fatal error."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        result = scaffold_comments_node(_base_state())

        assert "review_state_path" not in result
        assert any("failed to save review state" in e for e in result["errors"])

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=Exception("corrupted json"))
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_corrupted_state_triggers_fresh_scaffold(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-003, FR-005: Corrupted review-state.json triggers fresh scaffold."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        result = scaffold_comments_node(_base_state())

        # Should succeed — corrupted state treated as absent
        assert "review_state_path" in result
        mock_scaffold.assert_called_once()

    @patch(_PATCH_GET_AUTH, side_effect=RuntimeError("no PAT"))
    @patch(_PATCH_GET_PAT, side_effect=RuntimeError("auth failed"))
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_auth_failure_error_in_channel(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        tmp_path,
    ) -> None:
        """FR-005: Auth failure produces scaffold_comments: prefixed error."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        result = scaffold_comments_node(_base_state())

        assert "review_state_path" not in result
        assert any("scaffold_comments:" in e for e in result["errors"])


class TestDryRun:
    """NFR-003: Dry-run mode handling."""

    @patch(_PATCH_SCAFFOLD, return_value=None)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    def test_dry_run_placeholder_state(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """NFR-003: dry_run + None result produces placeholder ReviewState."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="my-repo")

        def get_value_side_effect(key):
            if key == "dry_run":
                return True
            return None

        with patch(_PATCH_GET_VALUE, side_effect=get_value_side_effect):
            result = scaffold_comments_node(_base_state())

        assert "review_state_path" in result
        assert result["errors"] == []
        saved = mock_save.call_args.args[0]
        assert saved.overallSummary.threadId == 0
        assert saved.overallSummary.commentId == 0
        assert saved.prId == 123
        assert saved.repoName == "my-repo"
        assert len(saved.sessions) == 1
        assert saved.sessions[0].engine == "langchain"

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    def test_dry_run_existing_state_returned(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """NFR-003: dry_run + existing ReviewState uses it directly."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        from agentic_devtools.cli.azure_devops.review_state import ReviewSession

        existing = _make_review_state(
            sessions=[
                ReviewSession(
                    sessionId="existing-1",
                    modelId="gpt-4o",
                    startedUtc="2026-01-01T00:00:00+00:00",
                    status="completed",
                )
            ],
        )
        mock_scaffold.return_value = existing

        def get_value_side_effect(key):
            if key == "dry_run":
                return True
            return None

        with patch(_PATCH_GET_VALUE, side_effect=get_value_side_effect):
            result = scaffold_comments_node(_base_state())

        assert "review_state_path" in result
        # Existing state returned — not the placeholder
        saved = mock_save.call_args.args[0]
        assert saved.overallSummary.threadId == 42

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    def test_dry_run_flag_from_state_key(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """NFR-003: dry_run read from get_value('dry_run'), not config."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = None

        # Config says dry_run=false, but state key says true
        state = _base_state(config={"dry_run": False})

        def get_value_side_effect(key):
            if key == "dry_run":
                return "true"
            return None

        with patch(_PATCH_GET_VALUE, side_effect=get_value_side_effect):
            result = scaffold_comments_node(state)

        # Should use state key, not config → dry_run=True → placeholder
        assert "review_state_path" in result
        assert mock_scaffold.call_args.kwargs["dry_run"] is True

    @patch(_PATCH_SCAFFOLD, return_value=None)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE, side_effect=RuntimeError("disk full"))
    @patch(_PATCH_GET_STATE_DIR)
    def test_dry_run_save_failure_returns_error(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """NFR-003: Save failure in dry-run produces error."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")

        def get_value_side_effect(key):
            if key == "dry_run":
                return True
            return None

        with patch(_PATCH_GET_VALUE, side_effect=get_value_side_effect):
            result = scaffold_comments_node(_base_state())

        assert "review_state_path" not in result
        assert any("failed to save dry-run review state" in e for e in result["errors"])

    @patch(_PATCH_SCAFFOLD, return_value=None)
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    def test_dry_run_skips_pat_lookup(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """NFR-003: dry_run skips get_pat() so it works without credentials."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="my-repo")

        def get_value_side_effect(key):
            if key == "dry_run":
                return True
            return None

        # get_pat / get_auth_headers are NOT patched — they must not be called
        with patch(_PATCH_GET_VALUE, side_effect=get_value_side_effect):
            result = scaffold_comments_node(_base_state())

        assert "review_state_path" in result
        assert result["errors"] == []
        # scaffold_review_threads received empty headers (dry_run path)
        call_kwargs = mock_scaffold.call_args.kwargs
        assert call_kwargs["dry_run"] is True
        assert call_kwargs.get("headers") == {}


class TestForceRereview:
    """US4, FR-006: Force re-review handling."""

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    def test_force_rereview_from_state_key(
        self,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-006: force_rereview read from get_value('review.force_rereview')."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        def get_value_side_effect(key):
            if key == "review.force_rereview":
                return True
            return None

        with patch(_PATCH_GET_VALUE, side_effect=get_value_side_effect):
            scaffold_comments_node(_base_state())

        assert mock_scaffold.call_args.kwargs["force_rereview"] is True

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_force_rereview_not_from_config(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """FR-006: config dict is never consulted for force_rereview."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        state = _base_state(config={"force_rereview": True})
        scaffold_comments_node(state)

        # force_rereview from get_value (None) → False, not from config
        assert mock_scaffold.call_args.kwargs["force_rereview"] is False


class TestRepoName:
    """Best-effort repo name resolution."""

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_populates_repo_name_from_config(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """repoName is populated from AzureDevOpsConfig.repository."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="my-repo")
        mock_scaffold.return_value = _make_review_state()

        scaffold_comments_node(_base_state())

        assert mock_scaffold.call_args.kwargs["repo_name"] == "my-repo"

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG, side_effect=RuntimeError("no config"))
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_repo_name_defaults_when_config_unavailable(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """Returns an error early when ADO config resolution fails."""
        mock_state_dir.return_value = tmp_path
        # ADO config fails both times (initial + fallback)
        mock_scaffold.side_effect = RuntimeError("no config")

        result = scaffold_comments_node(_base_state())

        # Should produce an error since scaffold can't proceed
        assert "review_state_path" not in result
        mock_scaffold.assert_not_called()

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_ado_config_fallback_on_second_attempt(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """When first ADO config attempt fails, retries before calling scaffold."""
        mock_state_dir.return_value = tmp_path
        mock_scaffold.return_value = _make_review_state()

        call_count = 0

        def from_state_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("first attempt fails")
            return SimpleNamespace(repository="fallback-repo")

        with patch(_PATCH_ADO_CONFIG, side_effect=from_state_side_effect):
            result = scaffold_comments_node(_base_state())

        assert "review_state_path" in result
        assert mock_scaffold.call_args.kwargs["repo_name"] == "fallback-repo"


class TestFilePathHandling:
    """File path extraction and handling."""

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_extracts_file_paths_from_dicts(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """File paths are extracted from file dicts as list[str]."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        state = _base_state(
            files=[
                {"path": "/src/main.py"},
                {"path": "/tests/test_main.py"},
            ]
        )
        scaffold_comments_node(state)

        passed_files = mock_scaffold.call_args.kwargs["files"]
        assert set(passed_files) == {"/src/main.py", "/tests/test_main.py"}

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_skips_files_without_path(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """Files without a 'path' key are excluded."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        state = _base_state(files=[{"path": "/src/main.py"}, {}, {"path": ""}])
        scaffold_comments_node(state)

        passed_files = mock_scaffold.call_args.kwargs["files"]
        assert passed_files == ["/src/main.py"]

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_skips_non_dict_and_blank_paths(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """Non-dict file entries and blank paths are ignored safely."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        state = _base_state(files=[{"path": "/src/main.py"}, None, "bad", {"path": "   "}])
        scaffold_comments_node(state)

        passed_files = mock_scaffold.call_args.kwargs["files"]
        assert passed_files == ["/src/main.py"]

    @patch(_PATCH_SCAFFOLD)
    @patch(_PATCH_GET_AUTH, return_value={})
    @patch(_PATCH_GET_PAT, return_value="pat")
    @patch(_PATCH_ADO_CONFIG)
    @patch(_PATCH_LOAD, side_effect=FileNotFoundError)
    @patch(_PATCH_SAVE)
    @patch(_PATCH_GET_STATE_DIR)
    @patch(_PATCH_GET_VALUE, return_value=None)
    def test_handles_non_list_files_payload(
        self,
        mock_get_value,
        mock_state_dir,
        mock_save,
        mock_load,
        mock_ado_config,
        mock_get_pat,
        mock_get_auth,
        mock_scaffold,
        tmp_path,
    ) -> None:
        """Non-list files payload is treated as an empty file set."""
        mock_state_dir.return_value = tmp_path
        mock_ado_config.return_value = SimpleNamespace(repository="")
        mock_scaffold.return_value = _make_review_state()

        scaffold_comments_node(_base_state(files=None))

        passed_files = mock_scaffold.call_args.kwargs["files"]
        assert passed_files == []
