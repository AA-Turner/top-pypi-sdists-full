"""Tests for dedupe_or_create."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.github.issue_dedup_integration import dedupe_or_create

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestDedupeOrCreateCreatePath:
    """Tests for dedupe_or_create — create path."""

    @patch(f"{_MOD}.record_in_ledger")
    @patch(f"{_MOD}.run_safe")
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}._get_ledger_path")
    def test_no_match_creates_issue(
        self, mock_path, mock_lookup, mock_search, mock_run, mock_record, tmp_path, capsys
    ) -> None:
        """No ledger match + no search match creates a new issue."""
        mock_path.return_value = tmp_path / "ledger.json"
        mock_run.return_value = MagicMock(returncode=0, stdout="https://github.com/owner/repo/issues/123\n", stderr="")

        dedupe_or_create(
            title="Test Issue",
            body="Test body",
            labels=["bug"],
            issue_type="Bug",
            assignees=None,
            milestone=None,
            error_class="ssl_error",
            dry_run=False,
        )

        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[1]["shell"] is False
        mock_record.assert_called_once()
        captured = capsys.readouterr()
        assert "Issue created:" in captured.out

    @patch(f"{_MOD}.record_in_ledger")
    @patch(f"{_MOD}.run_safe")
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}._get_ledger_path")
    def test_marker_present_in_body(self, mock_path, mock_lookup, mock_search, mock_run, mock_record, tmp_path) -> None:
        """Created issue body contains the dedup marker."""
        mock_path.return_value = tmp_path / "ledger.json"
        mock_run.return_value = MagicMock(returncode=0, stdout="https://github.com/owner/repo/issues/1\n", stderr="")

        dedupe_or_create(
            title="Test",
            body="body text",
            labels=None,
            issue_type=None,
            assignees=None,
            milestone=None,
            error_class="test_error",
            dry_run=False,
        )

        # Check the body passed to gh includes the marker
        call_args = mock_run.call_args[0][0]  # first positional = args list
        body_idx = call_args.index("--body") + 1
        body_arg = call_args[body_idx]
        assert "<!-- agdt-dedup-sig:" in body_arg

    @patch(f"{_MOD}.record_in_ledger")
    @patch(f"{_MOD}.run_safe")
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}._get_ledger_path")
    def test_create_path_uses_repo_override(
        self, mock_path, mock_lookup, mock_search, mock_run, mock_record, tmp_path
    ) -> None:
        """Create path uses the requested repo for gh issue create."""
        mock_path.return_value = tmp_path / "ledger.json"
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="https://github.com/owner/custom-repo/issues/123\n",
            stderr="",
        )

        dedupe_or_create(
            title="Test Issue",
            body="Test body",
            labels=["bug"],
            issue_type="Bug",
            assignees=None,
            milestone=None,
            error_class="ssl_error",
            dry_run=False,
            repo="owner/custom-repo",
        )

        gh_args = mock_run.call_args[0][0]
        repo_idx = gh_args.index("--repo")
        assert gh_args[repo_idx + 1] == "owner/custom-repo"


class TestDedupeOrCreateAugmentPath:
    """Tests for dedupe_or_create — augment path."""

    @patch(f"{_MOD}.record_in_ledger")
    @patch(f"{_MOD}.add_augment_comment")
    @patch(f"{_MOD}.add_thumbs_up")
    @patch(f"{_MOD}.lookup_ledger", return_value=42)
    def test_ledger_hit_augments_without_search(
        self, mock_lookup, mock_thumbs, mock_augment, mock_record, capsys
    ) -> None:
        """Ledger hit augments existing issue without GitHub search."""
        dedupe_or_create(
            title="Test",
            body="body",
            labels=None,
            issue_type=None,
            assignees=None,
            milestone=None,
            error_class="test_error",
            dry_run=False,
        )

        mock_thumbs.assert_called_once_with(42, repo="swai-factory/agentic-devtools")
        mock_augment.assert_called_once()
        mock_record.assert_called_once()
        captured = capsys.readouterr()
        assert "via ledger" in captured.out

    @patch(f"{_MOD}.record_in_ledger")
    @patch(f"{_MOD}.add_augment_comment")
    @patch(f"{_MOD}.add_thumbs_up")
    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}.search_by_marker")
    def test_search_hit_augments(
        self, mock_search, mock_lookup, mock_thumbs, mock_augment, mock_record, capsys
    ) -> None:
        """Search hit with open issue augments it."""
        mock_search.return_value = [
            {"number": 10, "state": "open", "body": "<!-- agdt-dedup-sig:a1b2c3d4e5f67890 -->"},
        ]

        from agentic_devtools.cli.github.issue_dedup import build_signature

        sig = build_signature("test_error")

        # Create an open match with the correct marker
        mock_search.return_value = [
            {"number": 10, "state": "open", "body": f"<!-- agdt-dedup-sig:{sig} -->"},
        ]

        dedupe_or_create(
            title="Test",
            body="body",
            labels=None,
            issue_type=None,
            assignees=None,
            milestone=None,
            error_class="test_error",
            dry_run=False,
        )

        mock_thumbs.assert_called_once_with(10, repo="swai-factory/agentic-devtools")
        mock_augment.assert_called_once()
        captured = capsys.readouterr()
        assert "via search" in captured.out


class TestDedupeOrCreateErrorPaths:
    """Tests for dedupe_or_create — error paths."""

    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}.search_by_marker", side_effect=RuntimeError("API error"))
    def test_search_runtime_error_propagates(self, mock_search, mock_lookup) -> None:
        """RuntimeError from search_by_marker propagates (fail-fast)."""
        with pytest.raises(RuntimeError, match="API error"):
            dedupe_or_create(
                title="Test",
                body="body",
                labels=None,
                issue_type=None,
                assignees=None,
                milestone=None,
                error_class="test_error",
                dry_run=False,
            )

    def test_invalid_error_class_raises(self) -> None:
        """Blank error_class raises ValueError."""
        with pytest.raises(ValueError, match="must not be blank"):
            dedupe_or_create(
                title="Test",
                body="body",
                labels=None,
                issue_type=None,
                assignees=None,
                milestone=None,
                error_class="  ",
                dry_run=False,
            )

    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    def test_closed_issues_filtered(self, mock_search, mock_lookup, capsys) -> None:
        """Closed issues are filtered out before decide()."""
        from agentic_devtools.cli.github.issue_dedup import build_signature

        sig = build_signature("test_error")

        mock_search.return_value = [
            {"number": 5, "state": "closed", "body": f"<!-- agdt-dedup-sig:{sig} -->"},
        ]

        with patch(f"{_MOD}.run_safe") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="https://github.com/o/r/issues/99\n", stderr="")
            with patch(f"{_MOD}.record_in_ledger"):
                dedupe_or_create(
                    title="Test",
                    body="body",
                    labels=None,
                    issue_type=None,
                    assignees=None,
                    milestone=None,
                    error_class="test_error",
                    dry_run=False,
                )
            # Should create because closed issue is filtered out
            mock_run.assert_called_once()


class TestDedupeOrCreateDryRun:
    """Tests for dedupe_or_create — dry-run paths."""

    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    def test_dry_run_create_preview(self, mock_search, mock_lookup, capsys) -> None:
        """Dry-run with no match shows create preview."""
        dedupe_or_create(
            title="Test Issue",
            body="Test body",
            labels=None,
            issue_type=None,
            assignees=None,
            milestone=None,
            error_class="test_error",
            dry_run=True,
        )

        captured = capsys.readouterr()
        assert "PREVIEW (not submitted)" in captured.out
        assert "would create issue" in captured.out
        assert "<!-- agdt-dedup-sig:" in captured.out

    @patch(f"{_MOD}.lookup_ledger", return_value=42)
    def test_dry_run_augment_preview(self, mock_lookup, capsys) -> None:
        """Dry-run with ledger hit shows augment preview."""
        dedupe_or_create(
            title="Test",
            body="body",
            labels=None,
            issue_type=None,
            assignees=None,
            milestone=None,
            error_class="test_error",
            dry_run=True,
        )

        captured = capsys.readouterr()
        assert "PREVIEW (not submitted)" in captured.out
        assert "would upvote and augment #42" in captured.out

    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    def test_dry_run_makes_no_mutations(self, mock_search, mock_lookup) -> None:
        """Dry-run performs no write operations."""
        with patch(f"{_MOD}.run_safe") as mock_run:
            with patch(f"{_MOD}.record_in_ledger") as mock_record:
                with patch(f"{_MOD}.add_thumbs_up") as mock_thumbs:
                    dedupe_or_create(
                        title="Test",
                        body="body",
                        labels=None,
                        issue_type=None,
                        assignees=None,
                        milestone=None,
                        error_class="test_error",
                        dry_run=True,
                    )
                    mock_run.assert_not_called()
                    mock_record.assert_not_called()
                    mock_thumbs.assert_not_called()

    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}.search_by_marker")
    def test_dry_run_search_hit_shows_augment_preview(self, mock_search, mock_lookup, capsys) -> None:
        """Dry-run with search hit shows augment preview."""
        from agentic_devtools.cli.github.issue_dedup import build_signature

        sig = build_signature("test_error")
        mock_search.return_value = [
            {"number": 77, "state": "open", "body": f"<!-- agdt-dedup-sig:{sig} -->"},
        ]

        dedupe_or_create(
            title="Test",
            body="body",
            labels=None,
            issue_type=None,
            assignees=None,
            milestone=None,
            error_class="test_error",
            dry_run=True,
        )

        captured = capsys.readouterr()
        assert "PREVIEW (not submitted)" in captured.out
        assert "would upvote and augment #77" in captured.out


class TestDedupeOrCreateGhErrors:
    """Tests for dedupe_or_create — gh CLI error paths."""

    @patch(f"{_MOD}.record_in_ledger")
    @patch(f"{_MOD}.run_safe")
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}._get_ledger_path")
    def test_gh_failure_exits(self, mock_path, mock_lookup, mock_search, mock_run, mock_record, tmp_path) -> None:
        """Non-zero returncode from gh causes sys.exit."""
        mock_path.return_value = tmp_path / "ledger.json"
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="auth error")

        with pytest.raises(SystemExit) as exc_info:
            dedupe_or_create(
                title="Test",
                body="body",
                labels=None,
                issue_type=None,
                assignees=None,
                milestone=None,
                error_class="test_error",
                dry_run=False,
            )
        assert exc_info.value.code == 1
        mock_record.assert_not_called()

    @patch(f"{_MOD}.run_safe")
    @patch(f"{_MOD}.search_by_marker", return_value=[])
    @patch(f"{_MOD}.lookup_ledger", return_value=None)
    @patch(f"{_MOD}._get_ledger_path")
    def test_unparseable_url_warns_but_succeeds(
        self, mock_path, mock_lookup, mock_search, mock_run, tmp_path, capsys
    ) -> None:
        """Unparseable issue URL warns but does not crash."""
        mock_path.return_value = tmp_path / "ledger.json"
        mock_run.return_value = MagicMock(returncode=0, stdout="not-a-url\n", stderr="")

        with pytest.warns(UserWarning, match="Could not extract issue number"):
            dedupe_or_create(
                title="Test",
                body="body",
                labels=None,
                issue_type=None,
                assignees=None,
                milestone=None,
                error_class="test_error",
                dry_run=False,
            )

        captured = capsys.readouterr()
        assert "Issue created:" in captured.out
