"""Tests for CCRFindingRecovery."""

from agentic_devtools.cli.github.ccr_review_format import CCRFinding, CCRFindingRecovery


def test_stores_findings_and_defaults_shortfalls_to_empty() -> None:
    finding = CCRFinding(
        section="previously_missed",
        ordinal=1,
        severity="P1",
        title="Guard the response",
        body="The response may be missing.",
        path="src/client.py",
        line=42,
    )

    recovery = CCRFindingRecovery(findings=(finding,))

    assert recovery.findings == (finding,)
    assert recovery.shortfalls == ()


def test_stores_declared_count_shortfalls() -> None:
    recovery = CCRFindingRecovery(findings=(), shortfalls=(("previously_missed", 2, 1),))

    assert recovery.findings == ()
    assert recovery.shortfalls == (("previously_missed", 2, 1),)
