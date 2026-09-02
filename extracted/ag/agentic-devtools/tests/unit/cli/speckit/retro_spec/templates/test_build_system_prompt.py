"""Tests for build_system_prompt in retro_spec/templates.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.templates import build_system_prompt


class TestBuildSystemPrompt:
    """Tests for the build_system_prompt function."""

    def test_enforces_factual_tone(self) -> None:
        """Test that the prompt enforces a factual, descriptive tone."""
        prompt = build_system_prompt()
        assert "FACTUAL" in prompt
        assert "DESCRIPTIVE" in prompt
        assert "shall" in prompt.lower()  # References to avoid prescriptive

    def test_requires_output_structure(self) -> None:
        """Test that required output sections are specified."""
        prompt = build_system_prompt()
        assert "User Story N - ... (Priority: PN)" in prompt
        assert "**Why this priority**" in prompt
        assert "**Independent Test**" in prompt
        assert "**Acceptance Scenarios**" in prompt

    def test_content_rules(self) -> None:
        """Test that content rules are included."""
        prompt = build_system_prompt()
        assert "10,000 characters" in prompt
        assert "artifacts" in prompt.lower()

    def test_forbids_frontmatter_in_generated_content(self) -> None:
        """Test that the prompt forbids duplicate frontmatter in model output."""
        prompt = build_system_prompt()
        assert "Do NOT include YAML frontmatter" in prompt
        assert "The tool adds the retroactive metadata header" in prompt

    def test_requires_implementation_evidence_subsections(self) -> None:
        """Test that mandatory implementation-evidence subsections are required."""
        prompt = build_system_prompt()
        assert "**Summary**" in prompt
        assert "**PR References**" in prompt
        assert "**Key Changes**" in prompt
