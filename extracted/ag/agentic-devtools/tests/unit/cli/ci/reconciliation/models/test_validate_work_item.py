"""Tests for validate_work_item()."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from agentic_devtools.cli.ci.reconciliation.models import WorkItem, WorkItemStatus, validate_work_item


def _make_work_item(**kwargs: Any) -> WorkItem:
    defaults: dict[str, Any] = {
        "pr_number": 1,
        "repo": "owner/repo",
        "change_id": "abc",
        "eligibility": "eligible",
        "due_at": None,
        "status": WorkItemStatus.QUEUED,
    }
    defaults.update(kwargs)
    return WorkItem(**defaults)


def test_rejects_zero_pr_number() -> None:
    with pytest.raises(ValueError, match="pr_number"):
        validate_work_item(_make_work_item(pr_number=0))


def test_rejects_negative_pr_number() -> None:
    with pytest.raises(ValueError, match="pr_number"):
        validate_work_item(_make_work_item(pr_number=-1))


def test_rejects_empty_repo() -> None:
    with pytest.raises(ValueError, match="repo"):
        validate_work_item(_make_work_item(repo=""))


def test_rejects_naive_datetime() -> None:
    with pytest.raises(ValueError, match="timezone"):
        validate_work_item(_make_work_item(due_at=datetime(2024, 1, 1)))


def test_rejects_negative_retry_count() -> None:
    with pytest.raises(ValueError, match="retry_count"):
        validate_work_item(_make_work_item(retry_count=-1))


def test_rejects_claimed_item_without_claim_id() -> None:
    with pytest.raises(ValueError, match="claim_id"):
        validate_work_item(_make_work_item(status=WorkItemStatus.CLAIMED, claim_id=""))


def test_rejects_claimed_item_without_operation_id() -> None:
    with pytest.raises(ValueError, match="operation_id"):
        validate_work_item(
            _make_work_item(
                status=WorkItemStatus.CLAIMED,
                claim_id="c1",
                operation_id="",
                claim_expires_at=datetime.now(UTC),
            )
        )


def test_rejects_claimed_item_without_claim_expiry() -> None:
    with pytest.raises(ValueError, match="claim_expires_at"):
        validate_work_item(
            _make_work_item(
                status=WorkItemStatus.CLAIMED,
                claim_id="c1",
                operation_id="op1",
                claim_expires_at=None,
            )
        )


def test_accepts_claimed_item_with_required_fields() -> None:
    validate_work_item(
        _make_work_item(
            status=WorkItemStatus.CLAIMED,
            claim_id="c1",
            operation_id="op1",
            claim_expires_at=datetime.now(UTC),
        )
    )


def test_rejects_leased_item_without_claim_id() -> None:
    with pytest.raises(ValueError, match="claim_id"):
        validate_work_item(_make_work_item(status=WorkItemStatus.LEASED, claim_id=""))


def test_rejects_leased_item_without_lease_id() -> None:
    with pytest.raises(ValueError, match="lease_id"):
        validate_work_item(
            _make_work_item(
                status=WorkItemStatus.LEASED,
                claim_id="c1",
                lease_id="",
                operation_id="op1",
            )
        )


def test_rejects_leased_item_without_operation_id() -> None:
    with pytest.raises(ValueError, match="operation_id"):
        validate_work_item(
            _make_work_item(
                status=WorkItemStatus.LEASED,
                claim_id="c1",
                lease_id="l1",
                operation_id="",
            )
        )


def test_rejects_leased_item_without_lease_expiry() -> None:
    with pytest.raises(ValueError, match="lease_expires_at"):
        validate_work_item(
            _make_work_item(
                status=WorkItemStatus.LEASED,
                claim_id="c1",
                lease_id="l1",
                operation_id="op1",
                lease_expires_at=None,
            )
        )


def test_accepts_leased_item_with_required_fields() -> None:
    validate_work_item(
        _make_work_item(
            status=WorkItemStatus.LEASED,
            claim_id="c1",
            lease_id="l1",
            operation_id="op1",
            lease_expires_at=datetime.now(UTC),
        )
    )


def test_accepts_valid_item() -> None:
    validate_work_item(_make_work_item())
