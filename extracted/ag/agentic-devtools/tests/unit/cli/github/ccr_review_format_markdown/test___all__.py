"""Tests for the Markdown helpers exported to CCR parser modules."""

import agentic_devtools.cli.github.ccr_review_format_markdown as ccr_review_format_markdown


def test_markdown_helpers_are_explicit_exports() -> None:
    assert set(ccr_review_format_markdown.__all__) == {
        "_FENCE_DELIM_RE",
        "_INLINE_CODE_COMPARISON_RE",
        "_INLINE_CODE_RE",
        "_mask_fenced_blocks",
        "_mask_inline_code",
    }
