"""Tests for is_executable_path in the gate_verdict module."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.pipeline.gate_verdict import is_executable_path


class TestIsExecutablePath:
    """Tests for is_executable_path."""

    @pytest.mark.parametrize(
        "path",
        [
            "agentic_devtools/cli/ci/pipeline/gate_verdict.py",
            "scripts/targeted-checks.sh",
            ".github/workflows/ai-pr-loop.yml",
            "./agentic_devtools/state.py",
            "/scripts/run-pr-checks.sh",
            "  agentic_devtools/state.py  ",
        ],
    )
    def test_executable_paths_return_true(self, path: str) -> None:
        assert is_executable_path(path) is True

    @pytest.mark.parametrize(
        "path",
        [
            "specs/3672-deferral/spec.md",
            "docs/suppressed-comment-triage-contract.md",
            "tests/unit/cli/ci/pipeline/gate_verdict/test_is_review_clean.py",
            "README.md",
            "",
        ],
    )
    def test_non_executable_paths_return_false(self, path: str) -> None:
        assert is_executable_path(path) is False
