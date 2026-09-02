"""Tests for parse_suppressed_count() in the CCR review-format parser."""

from agentic_devtools.cli.github.ccr_review_format import parse_suppressed_count


class TestParseSuppressedCount:
    """Tests for parse_suppressed_count()."""

    def test_empty_body_returns_zero(self) -> None:
        assert parse_suppressed_count("") == 0

    def test_legacy_summary_suppressed_count(self) -> None:
        body = "<summary>Comments suppressed due to low confidence (5)</summary>"
        assert parse_suppressed_count(body) == 5

    def test_new_format_heading_suppressed_count(self) -> None:
        body = "### Comments suppressed due to low confidence (8)"
        assert parse_suppressed_count(body) == 8

    def test_new_summary_suppressed_comments_count(self) -> None:
        """The bare ``<summary>Suppressed comments (N)</summary>`` summary yields N."""
        body = "<details>\n<summary>Suppressed comments (2)</summary>\n</details>"
        assert parse_suppressed_count(body) == 2

    def test_legacy_summary_bare_suppressed_count(self) -> None:
        """The legacy bare ``<summary>Suppressed (N)</summary>`` summary yields N."""
        body = "<details>\n<summary>Suppressed (2)</summary>\n</details>"
        assert parse_suppressed_count(body) == 2

    def test_heading_suppressed_comments_count(self) -> None:
        """The ``### Suppressed comments (N)`` heading spelling yields N.

        Regression for the stall class in swai-factory/agentic-devtools#3638: this
        heading is nested inside a generic ``<summary>Review details</summary>``
        block, so the ``<summary>``-anchored spelling never sees it.
        """
        body = "<details>\n<summary>Review details</summary>\n\n### Suppressed comments (3)\n\n**a.py:1**\n* finding\n"
        assert parse_suppressed_count(body) == 3

    def test_h1_heading_suppressed_comments_count(self) -> None:
        """An h1 ``# Suppressed comments (N)`` heading yields N (h1–h6 all accepted)."""
        assert parse_suppressed_count("# Suppressed comments (3)\n") == 3

    def test_suppressed_zero(self) -> None:
        body = "### Comments suppressed due to low confidence (0)"
        assert parse_suppressed_count(body) == 0

    def test_low_confidence_fallback_without_suppressed_word(self) -> None:
        """When 'suppressed' is absent, the 'low confidence (N)' fallback applies."""
        assert parse_suppressed_count("### Low confidence (3) findings hidden") == 3

    def test_no_pattern_returns_zero(self) -> None:
        assert parse_suppressed_count("This review has no suppressed section.") == 0

    def test_prose_count_is_not_anchored_and_returns_zero(self) -> None:
        """A count in ordinary prose is not a declared suppressed count.

        Regression for swai-factory/agentic-devtools#3638 root cause C: a PR
        overview mentioning ``Suppressed comment (1)`` used to block the merge
        gate even though the review had no suppressed block at all.
        """
        body = "This PR renames the `Suppressed comment (1)` helper used by the parser."
        assert parse_suppressed_count(body) == 0

    def test_count_inside_fenced_block_returns_zero(self) -> None:
        """A heading inside a fenced code excerpt is documentation, not a count."""
        body = "Review details:\n\n```\n### Suppressed comments (7)\n```\n"
        assert parse_suppressed_count(body) == 0

    def test_suppressed_takes_priority_over_low_confidence(self) -> None:
        body = "<summary>Suppressed comments (2)</summary>\n\n### Low confidence (9)"
        assert parse_suppressed_count(body) == 2

    def test_case_insensitive_suppressed(self) -> None:
        assert parse_suppressed_count("### suppressed comments (4)") == 4

    def test_crlf_heading_count(self) -> None:
        """GitHub returns review bodies with CRLF line endings."""
        assert parse_suppressed_count("### Suppressed comments (2)\r\n\r\n**a.py:1**\r\n") == 2

    def test_heading_with_trailing_text_after_the_count(self) -> None:
        """The count tolerates a heading tail, so the block regex must too."""
        assert parse_suppressed_count("### Suppressed comments (2) — low confidence") == 2

    def test_multiple_zero_declarations_return_zero(self) -> None:
        """Two zero declarations for the same pattern both return 0 without error."""
        body = "### Suppressed comments (0)\n\n### Suppressed comments (0)\n"
        assert parse_suppressed_count(body) == 0

    def test_nonzero_after_zero_returns_nonzero(self) -> None:
        """When a zero declaration precedes a nonzero one, the nonzero count wins."""
        body = "### Suppressed comments (0)\n\n### Suppressed comments (3)\n"
        assert parse_suppressed_count(body) == 3

    def test_zero_suppressed_nonzero_low_confidence_returns_nonzero(self) -> None:
        """A zero declaration in the first family must not suppress a nonzero in the second.

        A body containing ``### Suppressed comments (0)`` followed by
        ``### Low confidence (1)`` must return 1 so that extraction and the
        sentinel are not disabled by the earlier zero.
        """
        body = "### Suppressed comments (0)\n\n### Low confidence (1)\n\n**a.py:5**\n* finding\n"
        assert parse_suppressed_count(body) == 1

    def test_both_families_zero_returns_zero(self) -> None:
        """When both pattern families declare zero, return 0."""
        body = "### Suppressed comments (0)\n\n### Low confidence (0)\n"
        assert parse_suppressed_count(body) == 0
