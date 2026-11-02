"""Tests for reconciliation CLI error outcomes."""

import json
import logging
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError
from agentic_devtools.cli.ci.reconciliation.command_errors import handle_reconciliation_error
from agentic_devtools.cli.ci.reconciliation.models import Lease


@pytest.mark.parametrize("json_output", [False, True])
@pytest.mark.parametrize(
    ("reset_timestamp", "retry_after_seconds", "timing"),
    [
        (0, 30, "1970-01-01T00:00:00+00:00"),
        (1792684800, 30, "2026-10-22T16:00:00+00:00"),
        (1792684800000, 30, "retry after 30 seconds"),
        (1792684800000, None, "timing unknown"),
        (None, 2.5, "2.5 seconds"),
        (None, 0, "0 seconds"),
        (None, None, "timing unknown"),
    ],
)
def test_classified_rate_limit_is_deferred(
    json_output, reset_timestamp, retry_after_seconds, timing, capsys, caplog
) -> None:
    """Classified exhaustion gets neutral output with truthful reset timing."""
    fence = MagicMock()
    with caplog.at_level(logging.INFO):
        assert (
            handle_reconciliation_error(
                ProviderRateLimitError(retry_after_seconds, reset_timestamp=reset_timestamp),
                json_output=json_output,
                repo="owner/repo",
                dispatch_context=None,
                fence_unknown_dispatch_outcome=fence,
            )
            == 0
        )
    fence.assert_not_called()
    output = capsys.readouterr().out
    if json_output:
        payload = json.loads(output)
        assert payload["action"] == "deferred"
        assert payload["lease_id"] is None
        assert payload["operation_id"] is None
        assert payload["pr_number"] is None
        message = payload["message"]
    else:
        message = output
    assert "provider rate-limit" in message.lower()
    assert "not completed in this run" in message
    assert "will not be automatically resumed" in message
    assert timing in message
    if timing.startswith("reset at "):
        assert "30 seconds" not in message
    assert "Dispatched reconciliation" not in output
    assert "Unexpected reconciliation error" not in caplog.text
    assert message.strip() in caplog.text
    assert all(record.levelno < logging.ERROR for record in caplog.records)


@pytest.mark.parametrize("error", [ProviderRateLimitError(is_rate_limit=False), ValueError("provider rate limit")])
@pytest.mark.parametrize("dispatch_started", [False, True])
def test_genuine_errors_retain_failure_and_fencing(error, dispatch_started, capsys, caplog) -> None:
    """Typed false classifications and message lookalikes keep the unexpected-error path."""
    fence = MagicMock()
    store = MagicMock()
    assert (
        handle_reconciliation_error(
            error,
            json_output=True,
            repo="owner/repo",
            dispatch_context=(store, 42, None) if dispatch_started else None,
            fence_unknown_dispatch_outcome=fence,
        )
        == 1
    )
    assert capsys.readouterr().out == ""
    assert "Unexpected reconciliation error" in caplog.text
    assert any(record.levelno == logging.ERROR for record in caplog.records)
    if dispatch_started:
        fence.assert_called_once_with(
            store,
            "owner/repo",
            42,
            f"unexpected reconciliation error after provider dispatch for pr_number=42: {error}",
            lease=None,
        )
    else:
        fence.assert_not_called()


@pytest.mark.parametrize("fence_result", [True, False, ValueError("fence failed")])
@pytest.mark.parametrize("with_lease", [True, False])
def test_deferred_success_requires_fencing(fence_result, with_lease, capsys, caplog) -> None:
    """A dispatch attempt stays unknown; failed fencing cannot emit deferred success."""
    now = datetime.now(UTC)
    lease = (
        Lease(
            lease_id="lease-1",
            claim_id="claim-1",
            pr_number=42,
            repo="owner/repo",
            operation_id="operation-1",
            acquired_at=now,
            expires_at=now + timedelta(minutes=5),
        )
        if with_lease
        else None
    )
    store = MagicMock()
    fence = MagicMock()

    def fence_before_output(*args, **kwargs):
        assert capsys.readouterr().out == ""
        if isinstance(fence_result, Exception):
            raise fence_result
        return fence_result

    fence.side_effect = fence_before_output
    with caplog.at_level(logging.INFO):
        status = handle_reconciliation_error(
            ProviderRateLimitError(),
            json_output=True,
            repo="owner/repo",
            dispatch_context=(store, 42, lease),
            fence_unknown_dispatch_outcome=fence,
        )
    assert status == (0 if fence_result is True else 1)
    assert fence.call_count == 1
    assert fence.call_args.args[:3] == (store, "owner/repo", 42)
    assert fence.call_args.kwargs["lease"] is lease
    output = capsys.readouterr().out
    if fence_result is True:
        payload = json.loads(output)
        assert payload["action"] == "deferred"
        assert payload["pr_number"] == 42
        assert payload["lease_id"] == ("lease-1" if with_lease else None)
        assert payload["operation_id"] == ("operation-1" if with_lease else None)
        assert "dispatch outcome remains unknown" in payload["message"]
        assert all(record.levelno < logging.ERROR for record in caplog.records)
    else:
        assert output == ""
        assert any(record.levelno == logging.ERROR for record in caplog.records)
