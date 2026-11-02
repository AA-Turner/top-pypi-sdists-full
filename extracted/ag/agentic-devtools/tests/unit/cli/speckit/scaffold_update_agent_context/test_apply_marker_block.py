"""Tests for ``apply_marker_block``."""

import pytest

from agentic_devtools.cli.speckit.scaffold_update_agent_context import (
    SPECKIT_END_MARKER,
    SPECKIT_START_MARKER,
    apply_marker_block,
)

_BLOCK = f"{SPECKIT_START_MARKER}\n\nnew content\n\n{SPECKIT_END_MARKER}"


class TestApplyMarkerBlock:
    """apply_marker_block inserts or replaces the SpecKit-managed block."""

    def test_empty_existing_text_returns_block_with_trailing_newline(self) -> None:
        result = apply_marker_block("", _BLOCK)

        assert result == _BLOCK + "\n"

    def test_appends_block_when_markers_absent_and_text_ends_with_newline(self) -> None:
        existing = "# My Agent Instructions\n"

        result = apply_marker_block(existing, _BLOCK)

        assert result == existing + "\n" + _BLOCK + "\n"

    def test_appends_block_when_markers_absent_and_text_has_no_trailing_newline(self) -> None:
        existing = "# My Agent Instructions"

        result = apply_marker_block(existing, _BLOCK)

        assert result == existing + "\n" + "\n" + _BLOCK + "\n"

    def test_replaces_existing_block_in_place(self) -> None:
        old_block = f"{SPECKIT_START_MARKER}\n\nold content\n\n{SPECKIT_END_MARKER}"
        existing = f"# Header\n\n{old_block}\n\n# Footer"

        result = apply_marker_block(existing, _BLOCK)

        assert result == f"# Header\n\n{_BLOCK}\n\n# Footer"
        assert "old content" not in result

    def test_replace_is_idempotent(self) -> None:
        existing = f"# Header\n\n{_BLOCK}\n\n# Footer"

        result = apply_marker_block(existing, _BLOCK)

        assert result == existing

    def test_raises_when_only_one_marker_exists(self) -> None:
        existing = f"# Header\n\n{SPECKIT_START_MARKER}\n\n# Footer"

        with pytest.raises(ValueError, match="Malformed SpecKit marker block"):
            apply_marker_block(existing, _BLOCK)

    def test_raises_when_marker_text_is_not_on_a_standalone_line(self) -> None:
        existing = f"# Header\n\nPrefix {SPECKIT_START_MARKER}\n\n# Footer"

        with pytest.raises(ValueError, match="Malformed SpecKit marker block"):
            apply_marker_block(existing, _BLOCK)

    def test_raises_when_end_marker_text_is_not_on_a_standalone_line(self) -> None:
        existing = f"# Header\n\nSuffix {SPECKIT_END_MARKER}\n\n# Footer"

        with pytest.raises(ValueError, match="Malformed SpecKit marker block"):
            apply_marker_block(existing, _BLOCK)

    def test_raises_when_multiple_marker_pairs_exist(self) -> None:
        existing = "\n".join(
            [
                SPECKIT_START_MARKER,
                SPECKIT_END_MARKER,
                SPECKIT_START_MARKER,
                SPECKIT_END_MARKER,
            ]
        )

        with pytest.raises(ValueError, match="Malformed SpecKit marker block"):
            apply_marker_block(existing, _BLOCK)
