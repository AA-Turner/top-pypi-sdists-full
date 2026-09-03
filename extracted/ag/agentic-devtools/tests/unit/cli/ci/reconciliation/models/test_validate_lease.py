"""Tests for validate_lease()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from agentic_devtools.cli.ci.reconciliation.models import Lease, validate_lease


def _make_lease(**kwargs: Any) -> Lease:
    now = datetime.now(UTC)
    defaults: dict[str, Any] = {
        "lease_id": "l1",
        "claim_id": "c1",
        "pr_number": 1,
        "repo": "owner/repo",
        "operation_id": "op1",
        "acquired_at": now,
        "expires_at": now + timedelta(seconds=600),
    }
    defaults.update(kwargs)
    return Lease(**defaults)


def test_rejects_zero_pr_number() -> None:
    with pytest.raises(ValueError, match="pr_number"):
        validate_lease(_make_lease(pr_number=0))


def test_rejects_empty_repo() -> None:
    with pytest.raises(ValueError, match="repo"):
        validate_lease(_make_lease(repo=""))


def test_rejects_empty_operation_id() -> None:
    with pytest.raises(ValueError, match="operation_id"):
        validate_lease(_make_lease(operation_id=""))


def test_rejects_expiry_before_acquired_at() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValueError, match="expires_at"):
        validate_lease(_make_lease(acquired_at=now, expires_at=now - timedelta(seconds=1)))


def test_rejects_negative_revision() -> None:
    with pytest.raises(ValueError, match="revision"):
        validate_lease(_make_lease(revision=-1))


def test_rejects_empty_lease_id() -> None:
    with pytest.raises(ValueError, match="lease_id"):
        validate_lease(_make_lease(lease_id=""))


def test_rejects_empty_claim_id() -> None:
    with pytest.raises(ValueError, match="claim_id"):
        validate_lease(_make_lease(claim_id=""))


def test_accepts_valid_lease() -> None:
    validate_lease(_make_lease())
