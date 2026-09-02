"""Tests for derive_retry_operation_id in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.speckit.phase0.identifiers import derive_retry_operation_id


class TestDeriveRetryOperationId:
    """Tests for the derive_retry_operation_id function."""

    def test_valid_retry(self) -> None:
        decision_time = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
        result = derive_retry_operation_id("gh-event:abc", decision_time, 99, 2)
        assert result == "gh-retry:gh-event:abc:20260102T030405Z:99:2"

    def test_rejects_invalid_chain_operation_id(self) -> None:
        decision_time = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(ValueError):
            derive_retry_operation_id("has space", decision_time, 1, 1)

    def test_rejects_non_positive_workflow_run_id(self) -> None:
        decision_time = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(ValueError):
            derive_retry_operation_id("gh-event:abc", decision_time, 0, 1)

    def test_rejects_non_positive_workflow_run_attempt(self) -> None:
        decision_time = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(ValueError):
            derive_retry_operation_id("gh-event:abc", decision_time, 1, 0)

    def test_rejects_retry_prefix_as_chain_operation_id(self) -> None:
        decision_time = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(ValueError, match="initial-delivery"):
            derive_retry_operation_id("gh-retry:gh-event:abc:20260101T000000Z:1:1", decision_time, 2, 1)
