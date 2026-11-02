"""Tests for generate_v2_review_artifacts (best-effort wrapper)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_artifacts import generate_v2_review_artifacts

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_artifacts"


class TestGenerateV2ReviewArtifacts:
    def test_delegates_on_success(self):
        with patch(f"{_MODULE}._generate_v2_review_artifacts") as inner:
            generate_v2_review_artifacts(1, {"files": []}, Path("/tmp/x"))
        inner.assert_called_once()

    def test_catches_exception(self, capsys):
        with patch(f"{_MODULE}._generate_v2_review_artifacts", side_effect=RuntimeError("boom")):
            generate_v2_review_artifacts(1, {"files": []}, Path("/tmp/x"))
        captured = capsys.readouterr().err
        assert "v2 review artifact generation failed" in captured
        assert "setup unaffected" in captured
