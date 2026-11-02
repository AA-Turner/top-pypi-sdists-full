"""Canonical JSON is ASCII, compact, and sorted."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import _canonical_json


def test_canonical_bytes():
    assert _canonical_json({"z": "é", "a": 1}) == b'{"a":1,"z":"\\u00e9"}'
