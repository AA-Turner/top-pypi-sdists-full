"""Tests for WriterOutcome."""

from agentic_devtools.cli.ci.pipeline.writer_outcome import WriterOutcome


def test_exposes_exact_uppercase_string_outcomes() -> None:
    """The enum exposes exactly its four documented uppercase string outcomes."""
    assert {member.name: member.value for member in WriterOutcome} == {
        "PUSHED_WITH_EVIDENCE": "PUSHED_WITH_EVIDENCE",
        "PUSHED_WITHOUT_EVIDENCE": "PUSHED_WITHOUT_EVIDENCE",
        "NO_PUSH": "NO_PUSH",
        "UNKNOWN": "UNKNOWN",
    }
    assert str(WriterOutcome.PUSHED_WITH_EVIDENCE) == "PUSHED_WITH_EVIDENCE"
