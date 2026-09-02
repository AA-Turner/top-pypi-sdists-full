"""Tests for count_non_blank in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_counts_fence_delimiters() -> None:
    """The canonical wrapper shape is four non-blank lines, fences included."""
    actions = "\n1. Run the command:\n\n   ```bash\n   agdt-set key value\n   ```\n"
    assert derive.count_non_blank(actions) == derive.T0_MAX_ACTION_LINES


def test_blank_lines_are_ignored() -> None:
    """Whitespace-only lines do not count."""
    assert derive.count_non_blank("\n \n\ta\n") == 1
