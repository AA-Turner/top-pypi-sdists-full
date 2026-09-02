"""Tests for agdt.address-copilot-review.evaluate-and-respond.agent.md content."""

from __future__ import annotations

from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AGENT_FILE = _REPO_ROOT / ".github" / "agents" / "agdt.address-copilot-review.evaluate-and-respond.agent.md"


def _load_frontmatter() -> dict:
    """Parse YAML frontmatter from the agent file."""
    content = _AGENT_FILE.read_text(encoding="utf-8")
    assert content.startswith("---"), "File must start with YAML frontmatter delimiter"
    lines = content.splitlines()
    close_idx = next(i for i, line in enumerate(lines) if i > 0 and line == "---")
    fm_text = "\n".join(lines[1:close_idx])
    return yaml.safe_load(fm_text)


class TestEvaluateAndRespondAgentFrontmatter:
    """Validate agdt.address-copilot-review.evaluate-and-respond.agent.md frontmatter."""

    def test_frontmatter_is_parseable(self) -> None:
        """YAML frontmatter parses without error."""
        fm = _load_frontmatter()
        assert isinstance(fm, dict)

    def test_has_description(self) -> None:
        """Frontmatter includes a description field."""
        fm = _load_frontmatter()
        assert "description" in fm
        assert isinstance(fm["description"], str)
        assert len(fm["description"]) > 0

    def test_is_scoped_to_github(self) -> None:
        """Frontmatter keeps the GitHub-only classification."""
        fm = _load_frontmatter()
        assert fm["agdt"]["requires"]["code_hosting"] == "github"


class TestEvaluateAndRespondAgentContent:
    """Validate the companion agent file stays aligned with the flat dispatch format."""

    def test_describes_flat_comment_headings(self) -> None:
        """User Input describes the visible flat headings the dispatch now emits."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "## Comments from the PR author" in content
        assert "## Comments from the Code Review Agent" in content
        assert "`### Comment {N} - {file}[:{line}]` heading" in content

    def test_names_follow_on_sections(self) -> None:
        """User Input documents the CI, instructions, and review-thread sections."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "Optional `## CI failures`, `## Instructions`, and" in content
        assert "`## Original Code Review Thread` sections follow." in content

    def test_no_longer_describes_details_blocks(self) -> None:
        """The agent file must not contradict the flattened dispatch format."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "<details>" not in content
        assert "<summary>" not in content
