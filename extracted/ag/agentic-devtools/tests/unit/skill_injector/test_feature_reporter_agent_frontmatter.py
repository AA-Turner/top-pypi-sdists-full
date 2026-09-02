"""Tests for agdt.report-setup-feature.agent.md frontmatter and content validation."""

from __future__ import annotations

from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AGENT_FILE = _REPO_ROOT / ".github" / "agents" / "agdt.report-setup-feature.agent.md"


def _load_frontmatter() -> dict:
    """Parse YAML frontmatter from the agent file."""
    content = _AGENT_FILE.read_text(encoding="utf-8")
    assert content.startswith("---"), "File must start with YAML frontmatter delimiter"
    lines = content.splitlines()
    close_idx = next(i for i, line in enumerate(lines) if i > 0 and line == "---")
    fm_text = "\n".join(lines[1:close_idx])
    return yaml.safe_load(fm_text)


class TestFeatureReporterAgentFrontmatter:
    """Validate agdt.report-setup-feature.agent.md frontmatter."""

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


class TestFeatureReporterAgentContent:
    """Validate agdt.report-setup-feature.agent.md required sections and content."""

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

    def test_references_timeout_constant(self) -> None:
        """Feature reporter references FEATURE_REPORTER_INPUT_TIMEOUT_SECONDS = 120 (FR-007)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "FEATURE_REPORTER_INPUT_TIMEOUT_SECONDS" in content
        assert "120" in content

    def test_references_auto_submit_on_timeout(self) -> None:
        """Feature reporter references auto-submit on timeout (FR-007)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "auto-submit" in content.lower() or "Auto-submit" in content

    def test_references_dedupe_flag(self) -> None:
        """Feature reporter references agdt-create-agdt-feature-issue --dedupe (FR-007)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "agdt-create-agdt-feature-issue --dedupe" in content

    def test_references_tty_requirement(self) -> None:
        """Feature reporter references TTY requirement."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "TTY" in content

    def test_references_satisfaction_gating(self) -> None:
        """Feature reporter references satisfaction gating."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "satisf" in content.lower()
