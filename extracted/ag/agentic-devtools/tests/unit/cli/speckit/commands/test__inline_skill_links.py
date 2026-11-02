"""Tests for _inline_skill_links."""

import pytest

from agentic_devtools.cli.speckit.commands import _inline_skill_links


def test_inline_skill_links_inlines_linked_skill(tmp_path):
    """Inline linked skill content so it survives when the prompt is saved elsewhere."""
    agents_dir = tmp_path / ".github" / "agents"
    agents_dir.mkdir(parents=True)
    agent_file = agents_dir / "speckit.specify.agent.md"
    skill_file = tmp_path / ".agents" / "skills" / "speckit-specify" / "SKILL.md"
    skill_file.parent.mkdir(parents=True)
    skill_file.write_text(
        "---\nname: speckit-specify\n---\n# Specify procedure\n\nStep one.",
        encoding="utf-8",
    )

    result = _inline_skill_links(
        "Read and follow the [speckit-specify skill]"
        "(../../.agents/skills/speckit-specify/SKILL.md) as the authoritative procedure.",
        agent_file,
        tmp_path,
    )

    assert result == (
        "Read and follow the speckit-specify skill as the authoritative procedure.\n\n# Specify procedure\n\nStep one."
    )


def test_inline_skill_links_rejects_link_outside_skills_directory(tmp_path):
    """Reject skill links that resolve outside the repository skill directory."""
    agents_dir = tmp_path / ".github" / "agents"
    agents_dir.mkdir(parents=True)
    agent_file = agents_dir / "speckit.specify.agent.md"

    with pytest.raises(ValueError, match="must resolve within .agents/skills"):
        _inline_skill_links(
            "[external skill](../../.agents/skills/../../../../outside/SKILL.md)",
            agent_file,
            tmp_path,
        )
