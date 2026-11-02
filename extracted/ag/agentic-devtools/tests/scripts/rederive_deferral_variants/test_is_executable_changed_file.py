"""Tests for is_executable_changed_file in rederive_deferral_variants."""

from __future__ import annotations

import pytest

from tests.scripts.rederive_deferral_variants import rederive


@pytest.mark.parametrize(
    "raw",
    [
        "agentic_devtools/state.py",
        "agentic_devtools/cli/ci/pipeline/gate_verdict.py",
        "scripts/targeted-checks.sh",
        ".github/workflows/ai-pr-loop.yml",
    ],
)
def test_executable_union_members_are_executable(raw: str) -> None:
    """The three executable patterns classify as executable."""
    assert rederive.is_executable_changed_file(raw) is True


@pytest.mark.parametrize(
    "raw",
    [
        "LICENSE",
        "Dockerfile",
        "agentic_devtools/cli/setup/templates/commit-template",
        "specs/3672-defer/spec.md",
        "README.md",
        "tests/unit/state/test_get_value.py",
        "agentic_devtools/cli/setup/templates/commit-template.j2",
    ],
)
def test_files_outside_the_executable_union_are_not_executable(raw: str) -> None:
    """Extensionless real files and non-.py agentic_devtools files are not executable."""
    assert rederive.is_executable_changed_file(raw) is False


@pytest.mark.parametrize("raw", ["LICENSE", "Dockerfile"])
def test_does_not_fail_closed_the_way_is_executable_path_does(raw: str) -> None:
    """Extensionless API paths diverge from the fail-closed parsed-finding classifier."""
    assert rederive.is_executable_path(raw) is True
    assert rederive.is_executable_changed_file(raw) is False
