"""Tests for discrepancy serialization."""

from agentic_devtools.cli.phase0_review.report import discrepancy


def test_discrepancy_contains_three_json_string_tokens():
    finding = discrepancy('field"x', "a\\b", "é\nx")
    assert finding.serialize() == ('- [ ] Field "field\\"x": expected "a\\\\b", found "é\\nx"')
