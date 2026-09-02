"""Tests for is_executable_path in rederive_deferral_variants."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.ccr_review_format import UNKNOWN_FILE
from tests.scripts.rederive_deferral_variants import rederive


@pytest.mark.parametrize(
    "raw",
    [
        "agentic_devtools/cli/ci/pipeline/gate_verdict.py",
        "agentic_devtools/state.py",
        "scripts/targeted-checks.sh",
        "scripts/run-pr-checks.sh",
        ".github/workflows/ai-pr-loop.yml",
        ".github/prompts/agdt.pr-merge-manager.prompt.md",
    ],
)
def test_executable_prefixes_are_executable(raw: str) -> None:
    """agentic_devtools/**.py, scripts/** and .github/** are executable."""
    assert rederive.is_executable_path(raw) is True


@pytest.mark.parametrize(
    "raw",
    [
        "specs/3672-defer/spec.md",
        "docs/phase-0-configuration.md",
        "README.md",
        ".gitignore.md",
        "tests/unit/state/test_get_value.py",
        "agentic_devtools/cli/setup/templates/commit-template.j2",
    ],
)
def test_non_executable_paths(raw: str) -> None:
    """Specs, docs and tests are non-executable; so is a non-.py agentic_devtools file."""
    assert rederive.is_executable_path(raw) is False


@pytest.mark.parametrize(
    "raw",
    [
        "get_issue_types()",
        "--dry-run",
        "Acceptance Scenarios",
        UNKNOWN_FILE,
        "",
        "../agentic_devtools/state.py",
        "specs/../agentic_devtools/state.py",
        "././agentic_devtools/state.py",
        ".\\agentic_devtools\\state.py",
        "..\\agentic_devtools\\state.py",
        "specs\\..\\agentic_devtools\\state.py",
    ],
)
def test_non_path_artefacts_fail_closed(raw: str) -> None:
    """A string that is not a path cannot be shown safe, so it counts as executable."""
    assert rederive.is_executable_path(raw) is True


def test_line_anchor_does_not_defeat_classification() -> None:
    """A trailing :line anchor is stripped before the prefix test."""
    assert rederive.is_executable_path("agentic_devtools/state.py:120") is True
