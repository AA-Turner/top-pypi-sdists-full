"""Tests for PRDiffEvidence."""

from agentic_devtools.cli.ci.pipeline.delivery import PRDiffEvidence


def test_pr_diff_evidence_values() -> None:
    assert [evidence.value for evidence in PRDiffEvidence] == ["ZERO_DIFF", "NON_ZERO_DIFF", "UNKNOWN"]
