"""Tests for unrecovered_suppression_signal() in the CCR review-format parser."""

from agentic_devtools.cli.github.ccr_review_format import unrecovered_suppression_signal


class TestUnrecoveredSuppressionSignal:
    """Tests for unrecovered_suppression_signal()."""

    def test_empty_body_returns_false(self) -> None:
        assert unrecovered_suppression_signal("") is False

    def test_unanchored_count_with_entry_shaped_lines_fires(self) -> None:
        """An unrecognised wrapper that still names findings must fail closed."""
        body = "Copilot suppressed comments (2) in an unrecognised wrapper.\n\n**a.py:1**\n\n**b.py:2**\n"
        assert unrecovered_suppression_signal(body) is True

    def test_anchored_count_returns_false(self) -> None:
        """An anchored count is parsed normally, so the sentinel stays quiet."""
        body = "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        assert unrecovered_suppression_signal(body) is False

    def test_recovered_entries_without_count_returns_false(self) -> None:
        """Entries recovered by the structured parser mean nothing was lost."""
        body = "<details>\n<summary>Suppressed comments</summary>\n\n**a.py**: A finding\n\n</details>"
        assert unrecovered_suppression_signal(body) is False

    def test_no_count_returns_false(self) -> None:
        body = "A review body with **a.py:1** mentioned but no suppressed count."
        assert unrecovered_suppression_signal(body) is False

    def test_count_inside_fenced_block_returns_false(self) -> None:
        body = "Docs update.\n\n```\nSuppressed comments (2)\n**a.py:1**\n```\n"
        assert unrecovered_suppression_signal(body) is False

    def test_unanchored_count_without_entry_shaped_lines_returns_false(self) -> None:
        """Prose alone is the false positive this fix removes — do not re-block it."""
        body = "This PR renames the `Suppressed comment (1)` helper used by the parser."
        assert unrecovered_suppression_signal(body) is False

    def test_quoted_count_with_unrelated_bold_line_returns_false(self) -> None:
        """A narrated count plus an unrelated bold line must not block a clean review."""
        body = (
            "### ✅ Ready to approve\n\n"
            "The earlier `Suppressed comments (3)` note no longer applies.\n\n"
            "**Key changes**\n\n"
            "- **Comments generated:** 0 new\n"
        )
        assert unrecovered_suppression_signal(body) is False

    def test_entry_shaped_line_before_the_count_returns_false(self) -> None:
        """Real suppressed entries follow their count; an earlier bold line is unrelated."""
        body = "### ✅ Ready to approve\n\n**Key changes**\n\nSuppressed comments (3) were reviewed earlier.\n"
        assert unrecovered_suppression_signal(body) is False

    def test_zero_count_with_unrelated_bold_line_returns_false(self) -> None:
        """A zero declaration must not trigger the sentinel."""
        body = "Suppressed comments (0)\n\n**Key changes**\n\n- docs only\n"
        assert unrecovered_suppression_signal(body) is False

    def test_backticked_entry_after_count_still_fires(self) -> None:
        """Inline-code masking must not hide legacy backticked entry headers."""
        body = "Copilot suppressed comments (2) in an unrecognised wrapper.\n\n`a.py`\n\n`b.py`\n"
        assert unrecovered_suppression_signal(body) is True

    def test_inline_legacy_entry_after_nonzero_count_fires(self) -> None:
        """Legacy ``**path**: body`` entries after a nonzero count still fail closed."""
        body = "Suppressed comments (2) in an unrecognised wrapper.\n\n**a.py**: Fix this\n"
        assert unrecovered_suppression_signal(body) is True

    def test_low_confidence_nonzero_after_suppressed_zero_fires(self) -> None:
        """A later nonzero low-confidence declaration must not be masked by earlier zero."""
        body = "Suppressed comments (0)\n\nLow confidence (1)\n\n**a.py**: Fix this\n"
        assert unrecovered_suppression_signal(body) is True

    def test_count_and_parenthesised_number_on_separate_lines_returns_false(self) -> None:
        """The probe is line-scoped, so a stray number further down is not a count."""
        body = "Nothing was suppressed here.\n\nSee note (2) below.\n\n**a.py:1**\n"
        assert unrecovered_suppression_signal(body) is False

    def test_look_alike_unsuppressed_label_with_entries_does_not_stall_gate(self) -> None:
        """``Unsuppressed comments (2)`` is not a suppressed-comment block.

        The count parser already rejects it (no ``\\bsuppressed\\b`` word boundary
        before ``s``), so the gate fires no repair dispatch.  The sentinel must
        also reject it so the look-alike cannot stall the merge by tripping
        fail-closed handling.
        """
        body = "Unsuppressed comments (2)\n\n**a.py:1**\n\n**b.py:2**\n"
        assert unrecovered_suppression_signal(body) is False

    def test_look_alike_suppressed_commentary_with_entries_does_not_stall_gate(self) -> None:
        """``Suppressed commentary (2)`` is not a suppressed-comment block.

        ``commentary`` is not a word-bounded match for ``comments?``, so the
        structured parser ignores it.  The sentinel must also ignore it to keep
        the gate consistent: the look-alike must not produce a stall (fail-closed
        blocks merge without dispatching any repair findings).
        """
        body = "Suppressed commentary (2) in the narrative.\n\n**a.py:1**\n\n**b.py:2**\n"
        assert unrecovered_suppression_signal(body) is False
