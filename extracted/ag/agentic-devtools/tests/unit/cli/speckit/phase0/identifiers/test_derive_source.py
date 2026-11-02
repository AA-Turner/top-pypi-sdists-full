"""Tests for derive_source in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.identifiers import derive_source


class TestDeriveSource:
    """Tests for the derive_source function."""

    def test_retry_takes_precedence(self) -> None:
        result = derive_source(
            "issues",
            retry_of_run_id="gh:owner/repo:1:1",
            operation_id="gh-retry:gh-event:abc:20260101T000000Z:2:1",
        )
        assert result == "retry"

    def test_manual_dispatch(self) -> None:
        result = derive_source("workflow_dispatch", retry_of_run_id=None, operation_id="gh-event:abc")
        assert result == "manual-dispatch"

    def test_repository_dispatch(self) -> None:
        result = derive_source("repository_dispatch", retry_of_run_id=None, operation_id="gh-event:abc")
        assert result == "repository-dispatch"

    def test_provider_event_from_delivery(self) -> None:
        result = derive_source("issues", retry_of_run_id=None, operation_id="gh-event:abc")
        assert result == "provider-event"

    def test_provider_event_from_fallback(self) -> None:
        result = derive_source("issue_comment", retry_of_run_id=None, operation_id="gh-event-fallback:deadbeef")
        assert result == "provider-event"

    def test_raises_when_no_rule_matches(self) -> None:
        with pytest.raises(ValueError):
            derive_source("push", retry_of_run_id=None, operation_id="gh-retry:chain:20260101T000000Z:1:1")
