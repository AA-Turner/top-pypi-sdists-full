"""Tests for discover_agents in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline, build_repo


def test_agent_files_become_agent_name_rows(tmp_path):
    """Each agdt.* agent file yields one row invoked by its agent name."""
    repo = build_repo(tmp_path, agents=["agdt.set.agent.md"])
    units = baseline.discover_agents(repo)
    assert units == [baseline.Unit("agent", "agdt.set", ".github/agents/agdt.set.agent.md")]


def test_agent_name_comes_from_frontmatter_name_field(tmp_path):
    """Frontmatter name is preferred over filename when present."""
    repo = build_repo(tmp_path, agents=["agdt.pr-merge-execute.agent.md"])
    agent_file = repo / ".github/agents/agdt.pr-merge-execute.agent.md"
    agent_file.write_text(
        "---\nname: PR Merge Execute\ndescription: test\n---\n\n# Test\n",
        encoding="utf-8",
    )
    units = baseline.discover_agents(repo)
    assert units == [baseline.Unit("agent", "PR Merge Execute", ".github/agents/agdt.pr-merge-execute.agent.md")]


def test_readme_manifest_is_not_a_unit(tmp_path):
    """The agdt.README.md manifest is excluded because it backs no agent."""
    repo = build_repo(tmp_path, agents=["agdt.README.md"])
    assert baseline.discover_agents(repo) == []
