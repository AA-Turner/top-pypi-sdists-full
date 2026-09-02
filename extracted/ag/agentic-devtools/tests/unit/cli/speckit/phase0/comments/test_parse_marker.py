"""Tests for parse_marker in speckit/phase0/comments.py (FR-004, FR-006)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.comments import parse_marker


class TestParseMarker:
    """Tests for the parse_marker function."""

    def test_parses_rendered_marker(self) -> None:
        marker = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        body = f"{marker}\n## Phase 0 Status\n\n- Repository: owner/repo"

        parsed = parse_marker(body)

        assert parsed is not None
        assert parsed.chain_operation_id == "gh-event:abc"
        assert parsed.operation_id == "gh-event:abc"
        assert parsed.run_id == "gh:owner/repo:1:1"
        assert parsed.issue_id == "owner/repo#1"
        assert parsed.attempt_started_at == "2026-01-01T00:00:00Z"
        assert parsed.schema_version == "1.0"

    def test_returns_none_when_no_marker_present(self) -> None:
        assert parse_marker("just a regular comment") is None

    def test_returns_none_for_unrelated_html_comment(self) -> None:
        assert parse_marker("<!-- some other marker -->") is None

    def test_returns_none_for_unsupported_schema_version(self) -> None:
        comment = (
            "<!-- agdt:phase0-status schemaVersion=2.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        assert parse_marker(comment) is None

    def test_returns_none_when_marker_is_not_at_start(self) -> None:
        # FR-004 requires the status comment to begin with the marker; an
        # embedded marker (e.g. quoted or followed by text before it) must
        # not be treated as the mutable status comment.
        marker = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        body = f"Some preceding text\n\n{marker}"
        assert parse_marker(body) is None

    def test_returns_none_for_invalid_attempt_timestamp(self) -> None:
        comment = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=not-a-date -->"
        )
        assert parse_marker(comment) is None

    def test_returns_none_for_nonexistent_calendar_timestamp(self) -> None:
        comment = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-02-30T00:00:00Z -->"
        )
        assert parse_marker(comment) is None

    def test_returns_none_for_invalid_run_id(self) -> None:
        comment = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:0:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        assert parse_marker(comment) is None

    def test_returns_none_for_invalid_operation_id(self) -> None:
        comment = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh/event:abc runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        assert parse_marker(comment) is None

    def test_returns_none_for_noncanonical_operation_id_shape(self) -> None:
        comment = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event: runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        assert parse_marker(comment) is None

    def test_returns_none_for_invalid_issue_id(self) -> None:
        comment = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:1:1 issueId=%ZZ "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        assert parse_marker(comment) is None

    def test_returns_none_for_inconsistent_delivery_chain_operation_ids(self) -> None:
        # Both IDs are individually valid but the declared chainOperationId
        # does not match the operationId, which would allow a legacy or crafted
        # comment to be coalesced into the wrong mutable comment chain.
        comment = (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:a "
            "operationId=gh-event:b runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        assert parse_marker(comment) is None

    def test_parses_valid_retry_marker(self) -> None:
        # A retry operation ID must embed the declared chainOperationId.
        retry_op_id = "gh-retry:gh-event:abc:20260101T000000Z:1:1"
        comment = (
            f"<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            f"operationId={retry_op_id} runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            f"attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        parsed = parse_marker(comment)
        assert parsed is not None
        assert parsed.chain_operation_id == "gh-event:abc"
        assert parsed.operation_id == retry_op_id

    def test_returns_none_when_retry_embeds_wrong_chain(self) -> None:
        # operationId embeds chain "gh-event:abc" but chainOperationId says "gh-event:other".
        retry_op_id = "gh-retry:gh-event:abc:20260101T000000Z:1:1"
        comment = (
            f"<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:other "
            f"operationId={retry_op_id} runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            f"attemptStartedAt=2026-01-01T00:00:00Z -->"
        )
        assert parse_marker(comment) is None
