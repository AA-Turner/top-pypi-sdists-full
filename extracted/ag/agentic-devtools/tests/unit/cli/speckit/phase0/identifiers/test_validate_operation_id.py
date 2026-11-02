"""Tests for validate_operation_id in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.identifiers import validate_operation_id


class TestValidateOperationId:
    """Tests for the validate_operation_id function."""

    def test_accepts_gh_event_form(self) -> None:
        assert validate_operation_id("gh-event:abc-123") is True

    def test_accepts_gh_retry_form(self) -> None:
        assert validate_operation_id("gh-retry:gh-event:abc:20260102T030405Z:1:1") is True

    def test_accepts_gh_event_fallback_form(self) -> None:
        assert validate_operation_id(f"gh-event-fallback:{'a' * 64}") is True

    def test_rejects_empty_string(self) -> None:
        assert validate_operation_id("") is False

    def test_rejects_whitespace(self) -> None:
        assert validate_operation_id("has space") is False

    def test_rejects_disallowed_characters(self) -> None:
        for bad in ('has"quote', "has=equals", "has<lt", "has>gt", "has#hash"):
            assert validate_operation_id(bad) is False

    def test_rejects_trailing_newline(self) -> None:
        assert validate_operation_id("gh-event:abc\n") is False

    def test_rejects_unknown_prefix(self) -> None:
        assert validate_operation_id("arbitrary") is False

    def test_rejects_empty_delivery_suffix(self) -> None:
        assert validate_operation_id("gh-event:") is False

    def test_rejects_short_fallback_digest(self) -> None:
        assert validate_operation_id("gh-event-fallback:abc123") is False

    def test_rejects_retry_with_retry_chain_operation_id(self) -> None:
        assert validate_operation_id("gh-retry:gh-retry:gh-event:abc:20260102T000000Z:1:1:2:1") is False

    def test_rejects_retry_with_invalid_timestamp(self) -> None:
        assert validate_operation_id("gh-retry:gh-event:abc:20261301T000000Z:1:1") is False

    def test_rejects_retry_with_non_positive_run_coordinate(self) -> None:
        assert validate_operation_id("gh-retry:gh-event:abc:20260102T030405Z:0:1") is False

    def test_rejects_non_string(self) -> None:
        assert validate_operation_id(123) is False  # type: ignore[arg-type]
