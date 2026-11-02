"""Tests for agdt.report-setup-feature.prompt.md frontmatter validation."""

from __future__ import annotations

from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PROMPT_FILE = _REPO_ROOT / ".github" / "prompts" / "agdt.report-setup-feature.prompt.md"


def _load_frontmatter() -> dict:
    """Parse YAML frontmatter from the prompt file."""
    content = _PROMPT_FILE.read_text(encoding="utf-8")
    assert content.startswith("---"), "File must start with YAML frontmatter delimiter"
    lines = content.splitlines()
    close_idx = next(i for i, line in enumerate(lines) if i > 0 and line == "---")
    fm_text = "\n".join(lines[1:close_idx])
    return yaml.safe_load(fm_text)


class TestFeatureReporterPromptFrontmatter:
    """Validate agdt.report-setup-feature.prompt.md frontmatter."""

    def test_frontmatter_is_parseable(self) -> None:
        """YAML frontmatter parses without error."""
        fm = _load_frontmatter()
        assert isinstance(fm, dict)

    def test_has_agent_field(self) -> None:
        """Frontmatter includes the agent field pointing to the feature reporter."""
        fm = _load_frontmatter()
        assert fm.get("agent") == "agdt.report-setup-feature"

    def test_agdt_always_is_true(self) -> None:
        """Frontmatter has agdt.always set to true (FR-009)."""
        fm = _load_frontmatter()
        assert "agdt" in fm
        assert isinstance(fm["agdt"], dict)
        assert fm["agdt"].get("always") is True
