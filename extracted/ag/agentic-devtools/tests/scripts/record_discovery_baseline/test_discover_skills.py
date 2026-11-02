"""Tests for discover_skills in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline, build_repo


def test_skill_directories_become_rows(tmp_path):
    """Each SKILL.md yields one row invoked by its parent directory name."""
    repo = build_repo(tmp_path, skills=["run-targeted-checks"])
    units = baseline.discover_skills(repo)
    assert units == [baseline.Unit("skill", "run-targeted-checks", ".agents/skills/run-targeted-checks/SKILL.md")]


def test_missing_skills_directory_yields_no_rows(tmp_path):
    """A repository without .agents/skills contributes no skill rows."""
    repo = build_repo(tmp_path)
    assert baseline.discover_skills(repo) == []
