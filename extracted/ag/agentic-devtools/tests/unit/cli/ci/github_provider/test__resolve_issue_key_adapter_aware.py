"""Tests for GitHubActionsProvider._resolve_issue_key_adapter_aware."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_LOAD_PLATFORM_CONFIG = "agentic_devtools.cli.ci.github_provider.load_platform_config"


def _provider() -> GitHubActionsProvider:
    return GitHubActionsProvider(repo="owner/repo")


class TestResolveIssueKeyAdapterAware:
    """Tests for adapter-aware issue key resolution from head branch."""

    # ── Numeric keys are always valid ────────────────────────────────────────

    def test_numeric_key_returned_without_adapter_check(self) -> None:
        """Numeric keys bypass the adapter check and are returned directly."""
        with patch(_LOAD_PLATFORM_CONFIG) as mock_config:
            result = _provider()._resolve_issue_key_adapter_aware(
                "fix/2249/squash", ["fix(#2249): thing"], Path("/repo")
            )
        assert result == "2249"
        mock_config.assert_not_called()

    def test_no_key_in_branch_checks_adapter_and_returns_none_for_non_github(self) -> None:
        """``None`` from branch parsing checks the adapter and returns None for non-github adapters."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "jira"}):
            result = _provider()._resolve_issue_key_adapter_aware("main", [], Path("/repo"))
        assert result is None

    def test_no_key_in_branch_github_adapter_falls_back_to_subjects(self) -> None:
        """For github adapter, ``None`` branch key falls back to subject extraction."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "github"}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "fix/non-numeric-segment/description",
                ["fix(#2262): make coding-agent assignment reliable"],
                Path("/repo"),
            )
        assert result == "2262"

    def test_no_key_in_branch_github_adapter_no_subjects_returns_none(self) -> None:
        """For github adapter, ``None`` branch key with no numeric subjects returns None."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "github"}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "fix/non-numeric-segment/description",
                [],
                Path("/repo"),
            )
        assert result is None

    # ── Jira key on a GitHub-adapter repo ────────────────────────────────────

    def test_jira_key_on_github_adapter_falls_back_to_subjects(self) -> None:
        """Jira key is discarded for github adapter; numeric key extracted from subjects."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "github"}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "feature/PROJECT-1234/add-webhook",
                ["fix(#42): implement webhook"],
                Path("/repo"),
            )
        assert result == "42"

    def test_jira_key_on_github_adapter_no_subjects_returns_none(self) -> None:
        """Jira key discarded; no numeric key in subjects → None."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "github"}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "feature/PROJECT-1234/add-webhook",
                ["feat: add webhook without issue ref"],
                Path("/repo"),
            )
        assert result is None

    def test_jira_key_on_github_adapter_empty_subjects_returns_none(self) -> None:
        """Jira key discarded; empty subjects list → None."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "github"}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "feature/PROJECT-1234/add-webhook",
                [],
                Path("/repo"),
            )
        assert result is None

    # ── Jira key on a Jira-adapter repo ──────────────────────────────────────

    def test_jira_key_on_jira_adapter_returned_unchanged(self) -> None:
        """Jira key is kept when issue_adapter is ``"jira"``."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "jira"}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "feature/PROJECT-1234/add-webhook",
                ["feat(PROJECT-1234): add webhook"],
                Path("/repo"),
            )
        assert result == "PROJECT-1234"

    def test_jira_key_on_markdown_adapter_returned_unchanged(self) -> None:
        """Jira key is kept when issue_adapter is ``"markdown"``."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": "markdown"}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "feature/PROJECT-1234/add-webhook",
                [],
                Path("/repo"),
            )
        assert result == "PROJECT-1234"

    # ── Config load failure ───────────────────────────────────────────────────

    def test_config_load_failure_keeps_jira_key(self) -> None:
        """When platform config cannot be read, the conservative default keeps the Jira key."""
        with patch(_LOAD_PLATFORM_CONFIG, side_effect=OSError("file not found")):
            result = _provider()._resolve_issue_key_adapter_aware(
                "feature/PROJECT-1234/add-webhook",
                [],
                Path("/repo"),
            )
        assert result == "PROJECT-1234"

    # ── Adapter key missing from config ──────────────────────────────────────

    def test_missing_adapter_key_defaults_to_jira(self) -> None:
        """When ``issue_adapter`` is absent, defaults to ``"jira"`` → Jira key kept."""
        with patch(_LOAD_PLATFORM_CONFIG, return_value={}):
            result = _provider()._resolve_issue_key_adapter_aware(
                "feature/PROJECT-1234/add-webhook",
                [],
                Path("/repo"),
            )
        assert result == "PROJECT-1234"

    # ── Parametrized cross-adapter matrix ────────────────────────────────────

    @pytest.mark.parametrize(
        ("adapter", "branch", "subjects", "expected"),
        [
            ("github", "fix/ABC-99/x", ["fix(#55): stuff"], "55"),
            ("github", "fix/ABC-99/x", [], None),
            ("jira", "fix/ABC-99/x", [], "ABC-99"),
            ("markdown", "chore/XYZ-7/y", [], "XYZ-7"),
            # None branch key on github adapter → falls back to subject extraction
            ("github", "fix/no-key/description", ["fix(#2262): something"], "2262"),
            ("github", "fix/no-key/description", [], None),
            # None branch key on non-github adapters → None (no subject fallback)
            ("jira", "fix/no-key/description", ["fix(#2262): something"], None),
            ("markdown", "fix/no-key/description", ["fix(#2262): something"], None),
        ],
    )
    def test_parametrized(self, adapter: str, branch: str, subjects: list[str], expected: str | None) -> None:
        with patch(_LOAD_PLATFORM_CONFIG, return_value={"issue_adapter": adapter}):
            result = _provider()._resolve_issue_key_adapter_aware(branch, subjects, Path("/repo"))
        assert result == expected
