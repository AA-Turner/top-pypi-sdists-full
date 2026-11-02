"""Tests for discover_units in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline, build_repo


def test_units_are_sorted_by_surface_then_invocation(tmp_path):
    """All three surfaces are merged into one deterministically sorted list."""
    repo = build_repo(
        tmp_path,
        prompts=["agdt.set.prompt.md"],
        agents=["agdt.get.agent.md"],
        skills=["write-commit-message"],
    )
    units = baseline.discover_units(repo)
    assert [(unit.surface, unit.invocation) for unit in units] == [
        ("agent", "agdt.get"),
        ("prompt", "/agdt.set"),
        ("skill", "write-commit-message"),
    ]


def test_repository_baseline_matches_committed_file():
    """The committed baseline still lists exactly the units on disk."""
    from tests.scripts.record_discovery_baseline import REPO_ROOT

    units = baseline.discover_units(REPO_ROOT)
    committed = (REPO_ROOT / baseline.OUTPUT_PATH).read_text(encoding="utf-8")
    for unit in units:
        assert f"| {unit.surface} | `{unit.invocation}` | `{unit.backing_file}` |" in committed
    unit_rows = [line for line in committed.splitlines() if line.endswith(".md` |")]
    assert len(unit_rows) == len(units)
