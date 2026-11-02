"""Defensive read-only payload handling."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.approver_preflight import EvidenceStatus, _read_evidence


@pytest.mark.parametrize("payload", ["[]", "null", '"not a mapping"', "invalid json"])
def test_non_mapping_or_invalid_response_is_unknown(payload: str) -> None:
    data, evidence = _read_evidence(Mock(return_value=payload), "/user", "credential")
    assert data == {}
    assert evidence.status is EvidenceStatus.UNKNOWN
