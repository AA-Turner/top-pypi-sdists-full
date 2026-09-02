"""Tests for ``extract_technical_context``."""

from agentic_devtools.cli.speckit.scaffold_update_agent_context import extract_technical_context


class TestExtractTechnicalContext:
    """extract_technical_context parses filled-in fields from plan.md."""

    def test_extracts_known_filled_fields(self) -> None:
        plan_text = "\n".join(
            [
                "## Technical Context",
                "**Language/Version**: Python 3.11",
                "**Primary Dependencies**: click, pydantic",
                "**Storage**: N/A",
            ]
        )

        fields = extract_technical_context(plan_text)

        assert fields == {
            "Language/Version": "Python 3.11",
            "Primary Dependencies": "click, pydantic",
            "Storage": "N/A",
        }

    def test_ignores_unresolved_placeholder_values(self) -> None:
        plan_text = "**Language/Version**: [NEEDS CLARIFICATION]"

        fields = extract_technical_context(plan_text)

        assert fields == {}

    def test_ignores_empty_values(self) -> None:
        plan_text = "**Language/Version**:"

        fields = extract_technical_context(plan_text)

        assert fields == {}

    def test_ignores_needs_clarification_sentinel_anywhere_in_value(self) -> None:
        plan_text = "**Primary Dependencies**: Python 3.11 tooling (NEEDS CLARIFICATION)"

        fields = extract_technical_context(plan_text)

        assert fields == {}

    def test_ignores_unknown_field_names(self) -> None:
        plan_text = "**Some Random Field**: value"

        fields = extract_technical_context(plan_text)

        assert fields == {}

    def test_ignores_non_matching_lines(self) -> None:
        plan_text = "\n".join(
            [
                "# Plan",
                "Just a regular line",
                "**Language/Version**: Python 3.11",
            ]
        )

        fields = extract_technical_context(plan_text)

        assert fields == {"Language/Version": "Python 3.11"}

    def test_empty_plan_text_returns_empty_mapping(self) -> None:
        assert extract_technical_context("") == {}

    def test_extracts_wrapped_and_bulleted_multiline_values(self) -> None:
        plan_text = "\n".join(
            [
                "## Technical Context",
                "**Language/Version**: Markdown (YAML frontmatter) for agents/prompts; Python",
                "3.11 for optional coverage script",
                "**Primary Dependencies**:",
                "",
                "- Existing: pytest, requests",
                "- New: specify-cli",
                "## Constitution Check",
            ]
        )

        fields = extract_technical_context(plan_text)

        assert fields == {
            "Language/Version": (
                "Markdown (YAML frontmatter) for agents/prompts; Python 3.11 for optional coverage script"
            ),
            "Primary Dependencies": "Existing: pytest, requests; New: specify-cli",
        }

    def test_does_not_treat_single_hash_comment_line_as_heading(self) -> None:
        plan_text = "\n".join(
            [
                "## Technical Context",
                "**Testing**: pytest",
                "# keep inline shell comment text",
                "## Constitution Check",
            ]
        )

        fields = extract_technical_context(plan_text)

        assert fields == {"Testing": "pytest # keep inline shell comment text"}

    def test_mixed_inline_value_and_bullets_keep_prefix_separate(self) -> None:
        plan_text = "\n".join(
            [
                "## Technical Context",
                "**Primary Dependencies**: Core runtime",
                "- dep-a",
                "- dep-b",
            ]
        )

        fields = extract_technical_context(plan_text)

        assert fields == {"Primary Dependencies": "Core runtime dep-a; dep-b"}

    def test_bullet_value_can_include_continuation_lines(self) -> None:
        plan_text = "\n".join(
            [
                "## Technical Context",
                "**Primary Dependencies**:",
                "- dep-a",
                "continued details",
                "- dep-b",
            ]
        )

        fields = extract_technical_context(plan_text)

        assert fields == {"Primary Dependencies": "dep-a continued details; dep-b"}
