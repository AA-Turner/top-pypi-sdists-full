"""Tests for is_well_formed_path in the gate_verdict module."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.pipeline.gate_verdict import is_well_formed_path
from agentic_devtools.cli.github.ccr_review_format import UNKNOWN_FILE


class TestIsWellFormedPath:
    """Tests for is_well_formed_path."""

    @pytest.mark.parametrize(
        "path",
        [
            "specs/3672-deferral/spec.md",
            "README.md",
            "docs/a-b_c.d@e+f/notes.md",
            "specs/3672/tasks.md:42",
            "specs/3672/tasks.md:42-58",
            "./specs/3672/spec.md",
            "/specs/3672/spec.md",
        ],
    )
    def test_well_formed_paths_return_true(self, path: str) -> None:
        assert is_well_formed_path(path) is True

    @pytest.mark.parametrize(
        "path",
        [
            UNKNOWN_FILE,
            "get_issue_types()",
            "_is_copilot_review_actionable()",
            "--dry-run",
            "Acceptance Scenarios",
            "specs/3672",
            "../etc/passwd.txt",
            "",
            "   ",
            "specs/3672/spec.md:notanumber",
        ],
    )
    def test_non_path_strings_return_false(self, path: str) -> None:
        assert is_well_formed_path(path) is False
