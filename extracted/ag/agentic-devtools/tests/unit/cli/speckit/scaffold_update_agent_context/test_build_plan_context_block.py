"""Tests for ``build_plan_context_block``."""

from agentic_devtools.cli.speckit.scaffold_update_agent_context import (
    SPECKIT_END_MARKER,
    SPECKIT_START_MARKER,
    build_plan_context_block,
)


class TestBuildPlanContextBlock:
    """build_plan_context_block renders the marker-delimited plan summary."""

    def test_includes_markers_and_branch(self) -> None:
        block = build_plan_context_block("042-my-feature", "specs/042-my-feature", {})

        assert block.startswith(SPECKIT_START_MARKER)
        assert block.endswith(SPECKIT_END_MARKER)
        assert "042-my-feature" in block
        assert "specs/042-my-feature/plan.md" in block

    def test_includes_only_provided_fields_in_declared_order(self) -> None:
        fields = {"Storage": "N/A", "Language/Version": "Python 3.11"}

        block = build_plan_context_block("042-x", "specs/042-x", fields)

        lang_index = block.index("Language/Version")
        storage_index = block.index("Storage")
        assert lang_index < storage_index

    def test_omits_fields_not_present(self) -> None:
        block = build_plan_context_block("042-x", "specs/042-x", {"Storage": "N/A"})

        assert "Language/Version" not in block
        assert "Storage" in block

    def test_escapes_marker_tokens_in_rendered_values(self) -> None:
        block = build_plan_context_block(
            SPECKIT_START_MARKER,
            "specs/042-x",
            {"Storage": SPECKIT_END_MARKER},
        )

        assert f"- **Storage**: {SPECKIT_END_MARKER}" not in block
        assert "- **Storage**: &lt;!-- SPECKIT END --&gt;" in block
        assert "&lt;!-- SPECKIT START --&gt;" in block
