"""Tests for agdt.report-setup-bug.agent.md frontmatter and content validation."""

from __future__ import annotations

from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AGENT_FILE = _REPO_ROOT / ".github" / "agents" / "agdt.report-setup-bug.agent.md"


def _load_frontmatter() -> dict:
    """Parse YAML frontmatter from the agent file."""
    content = _AGENT_FILE.read_text(encoding="utf-8")
    assert content.startswith("---"), "File must start with YAML frontmatter delimiter"
    lines = content.splitlines()
    close_idx = next(i for i, line in enumerate(lines) if i > 0 and line == "---")
    fm_text = "\n".join(lines[1:close_idx])
    return yaml.safe_load(fm_text)


class TestBugReporterAgentFrontmatter:
    """Validate agdt.report-setup-bug.agent.md frontmatter."""

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

    def test_agdt_always_is_true(self) -> None:
        """Frontmatter has agdt.always set to true (FR-009)."""
        fm = _load_frontmatter()
        assert "agdt" in fm
        assert isinstance(fm["agdt"], dict)
        assert fm["agdt"].get("always") is True


class TestBugReporterAgentContent:
    """Validate agdt.report-setup-bug.agent.md required sections and content."""

    def test_has_user_input_section(self) -> None:
        """File contains a User Input section."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "## User Input" in content

    def test_has_purpose_section(self) -> None:
        """File contains a Purpose section."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "## Purpose" in content

    def test_has_actions_section(self) -> None:
        """File contains an Actions section."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "## Actions" in content

    def test_no_input_references(self) -> None:
        """Bug reporter must not contain input() as an action to perform (NFR-001).

        The constraint section may reference input() to forbid it — that's fine.
        We check that no Actions section contains input() usage.
        """
        content = _AGENT_FILE.read_text(encoding="utf-8")
        # Split at Actions section and check only the actions don't call input()
        actions_idx = content.find("## Actions")
        if actions_idx >= 0:
            remaining = content[actions_idx:]
            next_heading_idx = remaining.find("\n## ")
            actions_section = remaining[:next_heading_idx] if next_heading_idx >= 0 else remaining
        else:
            actions_section = ""
        assert "input()" not in actions_section

    def test_references_sanitize(self) -> None:
        """Bug reporter references sanitization (FR-004)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "sanitize" in content.lower() or "Sanitize" in content

    def test_references_truncation(self) -> None:
        """Bug reporter references 2000 char truncation (FR-004)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "2000" in content
        assert "truncat" in content.lower()

    def test_references_decision_log_table(self) -> None:
        """Bug reporter references decision-log summary table (FR-004)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "decision" in content.lower()
        assert "table" in content.lower() or "|" in content
        assert "| Iteration | Error class | Remedy applied | Rationale |" in content
        assert "- `Rationale` ← `--rationale` value" in content

    def test_references_dedupe_flag(self) -> None:
        """Bug reporter references agdt-create-agdt-bug-issue --dedupe (FR-004)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "agdt-create-agdt-bug-issue --dedupe" in content

    def test_references_exit_code_behavior(self) -> None:
        """Bug reporter references exit code 0 on success (FR-005)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "exit code" in content.lower() or "Exit" in content
