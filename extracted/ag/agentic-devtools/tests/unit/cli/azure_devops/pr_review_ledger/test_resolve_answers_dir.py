"""Tests for resolve_answers_dir."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_ledger import resolve_answers_dir

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_ledger"


class TestResolveAnswersDir:
    def test_builds_answers_path_from_state(self, tmp_path):
        def _get(key, default=None):
            return {"review.commit_hash_short": "abc123"}.get(key, default)

        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_get),
            patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value="dir1") as resolver,
        ):
            result = resolve_answers_dir(42)

        assert result == tmp_path / "pull-request-review" / "dir1" / "answers"
        resolver.assert_called_once_with(42, "abc123", backfill=True)

    def test_missing_commit_hash_short_defaults_to_empty(self, tmp_path):
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", return_value=None),
            patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value="PR7") as resolver,
        ):
            result = resolve_answers_dir(7)

        assert isinstance(result, Path)
        resolver.assert_called_once_with(7, None, backfill=True)

    def test_delegates_state_missing_fallback_to_resolver(self, tmp_path):
        """When review.commit_hash_short is absent, delegate fallback to the unified resolver (#1182)."""
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", return_value=None),
            patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value="2fea8cdf46c8") as resolver,
        ):
            result = resolve_answers_dir(25553)

        assert result == tmp_path / "pull-request-review" / "2fea8cdf46c8" / "answers"
        resolver.assert_called_once_with(25553, None, backfill=True)

    def test_uses_state_value_when_present(self, tmp_path):
        """When state has review.commit_hash_short, pass it straight to resolver."""

        def _get(key, default=None):
            return {"review.commit_hash_short": "abc123"}.get(key, default)

        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_get),
            patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value="dir1") as resolver,
        ):
            resolve_answers_dir(42)
        resolver.assert_called_once_with(42, "abc123", backfill=True)

    def test_backfill_false_is_forwarded_to_resolver(self, tmp_path):
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", return_value=None),
            patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value="PR42") as resolver,
        ):
            resolve_answers_dir(42, backfill=False)

        resolver.assert_called_once_with(42, None, backfill=False)
