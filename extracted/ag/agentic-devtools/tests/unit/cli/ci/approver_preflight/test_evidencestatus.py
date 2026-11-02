"""Stable evidence states."""

from agentic_devtools.cli.ci.approver_preflight import EvidenceStatus


def test_unknown_value_is_stable() -> None:
    assert EvidenceStatus.UNKNOWN.value == "unknown"
