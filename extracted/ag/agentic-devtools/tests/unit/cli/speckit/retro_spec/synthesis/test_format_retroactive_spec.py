"""Tests for format_retroactive_spec in retro_spec/synthesis.py."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec import synthesis
from agentic_devtools.cli.speckit.retro_spec.synthesis import format_retroactive_spec


class TestFormatRetroactiveSpec:
    """Tests for formatting retroactive specs with metadata and caps."""

    def test_includes_issue_title_and_source_metadata(self) -> None:
        """Metadata is included when issue details are available."""
        content = format_retroactive_spec(
            "body",
            issue_number=42,
            title="Implemented feature",
            labels=["done"],
            milestone="v1",
        )

        assert "# Feature Specification: Implemented feature" in content
        assert "**Source Issue**: #42" in content
        assert "**Labels**: done" in content
        assert "**Milestone**: v1" in content

    def test_marks_feature_branch_as_unavailable(self) -> None:
        """Generated metadata does not invent branch information."""
        content = format_retroactive_spec("body")

        assert "**Feature Branch**: `unavailable`" in content

    def test_uses_availability_agnostic_retroactive_warning(self) -> None:
        """The fixed header does not claim unavailable artifact classes."""
        content = format_retroactive_spec("body")

        assert "delivery evidence" in content
        assert "implementation artifacts" in content
        assert "when available" in content
        assert "PR diffs, commit messages, issue body" not in content

    def test_caps_content_to_output_limit(self) -> None:
        """The complete document stays within the 10,000-character contract."""
        content = format_retroactive_spec("x" * 100_000)

        assert len(content) <= 10_000

    def test_dynamic_header_cap_preserves_truncation_note(self) -> None:
        """Long metadata headers still use boundary-aware body truncation."""
        content = format_retroactive_spec(
            "line\n" * 5_000,
            issue_number=42,
            title="Very long title " * 60,
            labels=[f"label-{i}" for i in range(50)],
            milestone="milestone " * 80,
        )

        assert len(content) <= 10_000
        assert "This spec was summarized due to extensive artifacts." in content

    def test_extreme_title_is_capped_and_required_markers_preserved(self) -> None:
        """A 12,000-character title is capped so the retroactive warning block is never truncated."""
        content = format_retroactive_spec(
            "body content",
            issue_number=42,
            title="x" * 12_000,
        )

        assert len(content) <= 10_000
        # Required retroactive markers must survive regardless of title length.
        assert "**Generated**: retroactive" in content
        assert "⚠️ **Retroactive Spec**" in content
        # Body should also be present because the header no longer consumes the budget.
        assert "body content" in content

    def test_header_overflow_via_excessive_labels_preserves_retroactive_markers(self) -> None:
        """Excessive metadata is capped so required retroactive markers remain intact."""
        # 2,000 labels of "x"*6 each → "**Labels**: x, x, ... " ≫ 10,000 chars
        content = format_retroactive_spec(
            "body",
            labels=["x" * 6] * 2000,
        )

        assert len(content) <= synthesis._MAX_OUTPUT_CHARS
        assert "**Generated**: retroactive" in content
        assert "⚠️ **Retroactive Spec**" in content

    def test_truncates_milestone_line_when_metadata_budget_is_tight(self) -> None:
        """Milestone metadata is ellipsized when the remaining header budget is narrow."""
        base_header = synthesis._RETROACTIVE_HEADER.format(
            created="0000-00-00",
            source_issue="",
            labels="",
            milestone="",
        )
        capped_budget = len(base_header) + len("**Milestone**: …\n") + 5 + synthesis._MIN_BODY_CHARS
        with patch.object(synthesis, "_MAX_OUTPUT_CHARS", capped_budget):
            content = format_retroactive_spec("body", milestone="m" * 200)

        assert "**Milestone**: mmmmm…\n" in content

    def test_hard_caps_when_base_header_alone_exceeds_limit(self) -> None:
        """If the fixed header exceeds the cap, output is safely hard-capped."""
        with patch.object(synthesis, "_MAX_OUTPUT_CHARS", 120):
            content = format_retroactive_spec("body")

        assert len(content) == 120

    def test_body_survives_extreme_label_count(self) -> None:
        """Body content always receives at least _MIN_BODY_CHARS even with huge label metadata."""
        content = format_retroactive_spec(
            "body content here",
            labels=["x" * 6] * 2000,
        )

        assert len(content) <= synthesis._MAX_OUTPUT_CHARS
        assert "body content here" in content

    def test_total_output_does_not_exceed_max_chars_for_long_body(self) -> None:
        """Formatting an oversized body still honors the 10,000-character cap."""
        oversized_body = "x\n" * 6000

        result = format_retroactive_spec(oversized_body)
        assert len(result) <= synthesis._MAX_OUTPUT_CHARS

    def test_required_sections_preserved_when_dynamic_header_reduces_available_budget(self) -> None:
        """Required sections are retained even when header metadata shrinks the body budget."""
        # Force a small cap so the available budget after the header is tight enough
        # that a plain prefix truncation would discard the required sections.
        preamble = "x\n" * 300  # 600 chars > available budget with a patched limit
        body = preamble + "\n## Requirements\n- FR-001: Keep this.\n\n## Success Criteria\n- SC-001: Keep this.\n"
        with patch.object(synthesis, "_MAX_OUTPUT_CHARS", 800):
            content = format_retroactive_spec(body)

        assert len(content) <= 800
        assert "## Requirements" in content
        assert "## Success Criteria" in content

    def test_invokes_section_preserving_cap_when_sub_markers_are_missing(self) -> None:
        """format_retroactive_spec uses _cap_with_required_sections when sub-markers are absent.

        When _cap_content preserves the three top-level headings but drops a
        mandatory sub-marker such as ``### Functional Requirements``, the call
        site must escalate to the section-preserving cap, not silently emit a
        heading-only Requirements section.
        """
        # Build content where top-level headings appear early (within the cap)
        # but ### Functional Requirements appears past the truncation boundary.
        # With _MAX_OUTPUT_CHARS=700 and a ~395-char header, budget ≈ 305.
        # _cap_content truncates at (305 - 67) = 238 chars.
        # prefix=66 chars; filler fills up to 238+; sub_marker at ~276 is cut.
        prefix = "## User Scenarios & Testing\n## Requirements\n## Success Criteria\n"
        sub_marker = "\n### Functional Requirements\n"
        filler = "y\n" * 107  # 214 chars: places sub_marker past truncation boundary
        body = prefix + filler + sub_marker

        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._cap_with_required_sections",
                wraps=synthesis._cap_with_required_sections,
            ) as mock_capped,
            patch.object(synthesis, "_MAX_OUTPUT_CHARS", 700),
        ):
            format_retroactive_spec(body)

        assert mock_capped.called, (
            "_cap_with_required_sections must be invoked when a plain cap drops required sub-markers"
        )

    def test_post_validation_fallback_preserves_sub_markers_within_total_cap(self) -> None:
        """Last-resort fallback keeps the total cap while retaining compact required markers.

        When both ``_cap_content`` and ``_cap_with_required_sections`` would drop
        sub-markers, ``format_retroactive_spec`` falls back to a compact
        marker-bearing excerpt instead of allowing the document to exceed the
        10,000-character contract.
        """
        # Build content where required sub-markers exist but would be lost at a tiny budget
        content = (
            "## User Scenarios & Testing\n" + "z\n" * 500 + "### User Story Title\n"
            "**Why this priority**: x\n"
            "**Independent Test**: y\n"
            "**Acceptance Scenarios**: z\n"
            "### Edge Cases\n"
            "## Requirements\n"
            "### Functional Requirements\n"
            "### Non-Functional Requirements\n"
            "## Success Criteria\n"
        )

        # A cap tight enough that the prefix-preserving fallback would previously
        # exceed the total output limit, but large enough to fit a compact marker excerpt.
        with patch.object(synthesis, "_MAX_OUTPUT_CHARS", 800):
            result = format_retroactive_spec(content)

        assert len(result) <= 800
        # All required top-level markers must be present in the output
        assert "## Requirements" in result
        assert "## Success Criteria" in result
        # Required sub-markers must also be present via the fallback path
        assert "### Functional Requirements" in result
        assert "### Non-Functional Requirements" in result

    def test_preserves_artifact_availability_section_under_tight_budget(self) -> None:
        """Artifact Availability is not dropped when the body budget is tight.

        The section is prepended by the tool layer (not the LLM), so the
        format_retroactive_spec capping logic must treat it as required when
        present, even though it is not a marker expected from raw LLM output.
        """
        availability_notice = "No PR diffs were available for this issue."
        content = (
            f"## Artifact Availability\n\n{availability_notice}\n\n"
            "## User Scenarios & Testing\n"
            "### User Story 1 - Test (Priority: P1)\n"
            "**Why this priority**: reason\n"
            "**Independent Test**: test\n"
            "**Acceptance Scenarios**: scenario\n"
            "### Edge Cases\n"
            "none\n"
            "## Requirements\n"
            "### Functional Requirements\n"
            "- FR1\n"
            "### Non-Functional Requirements\n"
            "- NFR1\n"
            "## Success Criteria\n"
            "- SC1\n" + "x" * 8000
        )

        result = format_retroactive_spec(content)

        assert availability_notice in result
