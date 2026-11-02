"""Tests for offset-preserving text masking."""

from agentic_devtools.cli.github.ccr_finding_recovery import _mask_spans


def test_masks_span_content_and_preserves_newlines() -> None:
    text = "before\nlegacy entry\nstatus"

    result = _mask_spans(text, ((7, 20),))

    assert len(result) == len(text)
    assert result == "before\n            \nstatus"


def test_empty_spans_preserve_text() -> None:
    assert _mask_spans("status", ()) == "status"
