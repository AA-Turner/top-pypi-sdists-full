"""JSON record construction does not discard unknown fields."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import ReconciliationFileVerdict, _record_from_json


def test_record_construction():
    payload = {"path": "a", "content_sha256": "a" * 64, "verdict": "accepted", "behavior": "Preserved"}
    assert _record_from_json(ReconciliationFileVerdict, payload) == ReconciliationFileVerdict(**payload)
