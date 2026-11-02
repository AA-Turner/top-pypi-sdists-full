"""Tests for CCRFinding."""

from agentic_devtools.cli.github.ccr_review_format import CCRFinding


def test_stores_finding_details_and_defaults_optional_provenance() -> None:
    finding = CCRFinding(
        section="previously_missed",
        ordinal=1,
        severity="P1",
        title="Guard the response",
        body="The response may be missing.",
        path="src/client.py",
        line=42,
    )

    assert finding.section == "previously_missed"
    assert finding.ordinal == 1
    assert finding.severity == "P1"
    assert finding.title == "Guard the response"
    assert finding.body == "The response may be missing."
    assert finding.path == "src/client.py"
    assert finding.line == 42
    assert finding.source_review_id == 0
    assert finding.source_review_url == ""
    assert finding.explicitly_resolved is False
