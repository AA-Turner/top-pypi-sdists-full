"""Tests for discover_skill_files function."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.checks.skill_classification import discover_skill_files


class TestDiscoverSkillFiles:
    """Verifies glob patterns, exclusion, and path normalization."""

    def test_discovers_agent_files(self, tmp_path: Path) -> None:
        agents = tmp_path / ".github" / "agents"
        agents.mkdir(parents=True)
        (agents / "agdt.foo.agent.md").write_text("# Skill\n")
        (agents / "agdt.bar.agent.md").write_text("# Skill\n")
        result = discover_skill_files(tmp_path)
        assert ".github/agents/agdt.foo.agent.md" in result
        assert ".github/agents/agdt.bar.agent.md" in result

    def test_discovers_prompt_files(self, tmp_path: Path) -> None:
        prompts = tmp_path / ".github" / "prompts"
        prompts.mkdir(parents=True)
        (prompts / "agdt.baz.prompt.md").write_text("# Skill\n")
        result = discover_skill_files(tmp_path)
        assert ".github/prompts/agdt.baz.prompt.md" in result

    def test_excludes_non_agdt_files(self, tmp_path: Path) -> None:
        agents = tmp_path / ".github" / "agents"
        agents.mkdir(parents=True)
        (agents / "agdt.foo.agent.md").write_text("# Skill\n")
        (agents / "some-other-file.md").write_text("# Not a skill\n")
        (agents / "agdt.README.md").write_text("# README\n")
        result = discover_skill_files(tmp_path)
        assert ".github/agents/agdt.foo.agent.md" in result
        assert ".github/agents/some-other-file.md" not in result
        assert ".github/agents/agdt.README.md" not in result

    def test_forward_slash_separators(self, tmp_path: Path) -> None:
        agents = tmp_path / ".github" / "agents"
        agents.mkdir(parents=True)
        (agents / "agdt.x.agent.md").write_text("# Skill\n")
        result = discover_skill_files(tmp_path)
        paths = list(result)
        for p in paths:
            assert "\\" not in p, f"Backslash found in path: {p}"

    def test_empty_repo_returns_empty_set(self, tmp_path: Path) -> None:
        result = discover_skill_files(tmp_path)
        assert result == set()

    def test_empty_dirs_returns_empty_set(self, tmp_path: Path) -> None:
        (tmp_path / ".github" / "agents").mkdir(parents=True)
        (tmp_path / ".github" / "prompts").mkdir(parents=True)
        result = discover_skill_files(tmp_path)
        assert result == set()
