"""Tests for discover_prompts in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline, build_repo


def test_prompt_files_become_slash_command_rows(tmp_path):
    """Each agdt.* prompt file yields one row invoked as a slash command."""
    repo = build_repo(tmp_path, prompts=["agdt.set.prompt.md", "agdt.get.prompt.md"])
    units = baseline.discover_prompts(repo)
    assert units == [
        baseline.Unit("prompt", "/agdt.get", ".github/prompts/agdt.get.prompt.md"),
        baseline.Unit("prompt", "/agdt.set", ".github/prompts/agdt.set.prompt.md"),
    ]


def test_readme_manifest_is_not_a_unit(tmp_path):
    """The agdt.README.md manifest is excluded because it backs no command."""
    repo = build_repo(tmp_path, prompts=["agdt.README.md", "agdt.set.prompt.md"])
    units = baseline.discover_prompts(repo)
    assert [unit.invocation for unit in units] == ["/agdt.set"]
