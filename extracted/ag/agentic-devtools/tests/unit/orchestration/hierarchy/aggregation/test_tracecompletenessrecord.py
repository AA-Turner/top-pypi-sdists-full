"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from agentic_devtools.orchestration.hierarchy.aggregation import (
    TraceCompletenessRecord,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


@pytest.mark.parametrize(
    ("payload", "match"),
    [
        ({"run_id": 1, "timestamp": "t", "complete": True}, "run_id"),
        ({"run_id": "r", "timestamp": 1, "complete": True}, "timestamp"),
        ({"run_id": "r", "timestamp": "t", "complete": "yes"}, "complete"),
        ({"run_id": "r", "timestamp": "t", "complete": True, "explicitly_cancelled": "no"}, "explicitly_cancelled"),
    ],
)
def test_trace_completeness_from_dict_rejects_invalid_types(payload: dict[str, object], match: str) -> None:
    with pytest.raises(ValueError, match=match):
        TraceCompletenessRecord.from_dict(payload)
