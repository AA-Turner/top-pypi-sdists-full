"""Tests for _apply_output_cap in retro_spec/synthesis.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec import synthesis
from agentic_devtools.cli.speckit.retro_spec.synthesis import _apply_output_cap


class TestApplyOutputCap:
    """Tests for the _apply_output_cap helper."""

    def test_returns_content_unchanged_when_within_body_budget(self) -> None:
        """Body content within the reserved budget passes through unchanged."""
        assert _apply_output_cap("hello") == "hello"

    def test_caps_content_to_reserved_body_budget(self) -> None:
        """Oversized body content is capped to the formatter's reserved budget."""
        content = "x\n" * 6000

        result = _apply_output_cap(content)

        assert len(result) <= synthesis._MAX_BODY_CHARS
        assert "summarized due to extensive artifacts" in result

    def test_preserves_required_sections_when_prefix_truncation_would_drop_them(self) -> None:
        """Required terminal sections are preserved when content must be summarized."""
        content = (
            ("x\n" * 6000)
            + "\n## Requirements\n### Functional Requirements\n- **FR-001**: Keep this section.\n"
            + "\n## Success Criteria\n### Measurable Outcomes\n- **SC-001**: Keep this section.\n"
        )

        result = _apply_output_cap(content)

        assert len(result) <= synthesis._MAX_BODY_CHARS
        assert "## Requirements" in result
        assert "## Success Criteria" in result
