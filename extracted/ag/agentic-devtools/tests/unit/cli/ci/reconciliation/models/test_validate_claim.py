"""Tests for validate_claim()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from agentic_devtools.cli.ci.reconciliation.models import Claim, validate_claim


def _make_claim(**kwargs: Any) -> Claim:
    now = datetime.now(UTC)
    defaults: dict[str, Any] = {
        "claim_id": "c1",
        "pr_number": 1,
        "repo": "owner/repo",
        "operation_id": "op1",
        "acquired_at": now,
        "expires_at": now + timedelta(seconds=300),
    }
    defaults.update(kwargs)
    return Claim(**defaults)


def test_rejects_expiry_before_acquired_at() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValueError, match="expires_at"):
        validate_claim(_make_claim(acquired_at=now, expires_at=now - timedelta(seconds=1)))


def test_rejects_expiry_equal_to_acquired_at() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValueError, match="expires_at"):
        validate_claim(_make_claim(acquired_at=now, expires_at=now))


def test_rejects_zero_pr_number() -> None:
    with pytest.raises(ValueError, match="pr_number"):
        validate_claim(_make_claim(pr_number=0))


def test_rejects_empty_repo() -> None:
    with pytest.raises(ValueError, match="repo"):
        validate_claim(_make_claim(repo=""))


def test_rejects_empty_operation_id() -> None:
    with pytest.raises(ValueError, match="operation_id"):
        validate_claim(_make_claim(operation_id=""))


def test_rejects_negative_revision() -> None:
    with pytest.raises(ValueError, match="revision"):
        validate_claim(_make_claim(revision=-1))


def test_rejects_naive_acquired_at() -> None:
    now = datetime(2024, 1, 1)
    with pytest.raises(ValueError, match="timezone"):
        validate_claim(_make_claim(acquired_at=now, expires_at=now + timedelta(seconds=300)))


def test_rejects_empty_claim_id() -> None:
    with pytest.raises(ValueError, match="claim_id"):
        validate_claim(_make_claim(claim_id=""))


def test_accepts_valid_claim() -> None:
    validate_claim(_make_claim())
