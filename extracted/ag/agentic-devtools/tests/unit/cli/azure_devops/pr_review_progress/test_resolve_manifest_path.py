"""Tests for resolve_manifest_path."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_progress import resolve_manifest_path

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_progress"


class TestResolveManifestPath:
    def test_manifest_sits_next_to_answers_dir(self, tmp_path):
        answers = tmp_path / "pull-request-review" / "abc123" / "answers"
        with patch(f"{_MODULE}.resolve_answers_dir", return_value=answers):
            result = resolve_manifest_path(42)
        assert result == tmp_path / "pull-request-review" / "abc123" / "manifest.json"
        assert isinstance(result, Path)
