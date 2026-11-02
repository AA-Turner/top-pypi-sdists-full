"""Tests for looks_like_path in rederive_deferral_variants."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.ccr_review_format import UNKNOWN_FILE
from tests.scripts.rederive_deferral_variants import rederive


@pytest.mark.parametrize(
    "raw",
    [
        "specs/3672-defer/spec.md",
        "agentic_devtools/cli/ci/pipeline/gate_verdict.py",
        ".github/workflows/ai-pr-loop.yml",
        "README.md",
        "`specs/3672/plan.md`",
        "specs/3672/plan.md:42",
        "specs/3672/plan.md:42-58",
        "./docs/setup.md",
        "specs/3672/design notes.md",
    ],
)
def test_accepts_path_shaped_strings(raw: str) -> None:
    """Path-shaped strings, with or without decoration, are accepted."""
    assert rederive.looks_like_path(raw) is True


@pytest.mark.parametrize(
    "raw",
    [
        "get_issue_types()",
        "_is_copilot_review_actionable()",
        "--dry-run",
        "Acceptance Scenarios",
        UNKNOWN_FILE,
        "",
        "   ",
        "specs/3672/spec",
        "specs/3672/",
        "../agentic_devtools/state.py",
        "specs/../agentic_devtools/state.py",
        "././agentic_devtools/state.py",
        ".\\agentic_devtools\\state.py",
        "..\\agentic_devtools\\state.py",
        "specs\\..\\agentic_devtools\\state.py",
    ],
)
def test_rejects_non_path_artefacts(raw: str) -> None:
    """The artefact strings measured in #3672 are rejected, as is UNKNOWN_FILE."""
    assert rederive.looks_like_path(raw) is False


def test_rejects_extension_longer_than_ten_characters() -> None:
    """A trailing dot-run too long to be an extension is not a path."""
    assert rederive.looks_like_path("thing.averylongextension") is False
