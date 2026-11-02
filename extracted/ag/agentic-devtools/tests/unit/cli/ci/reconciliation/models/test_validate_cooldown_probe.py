"""Tests for validate_cooldown_probe()."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.reconciliation.models import CooldownProbe, ProbeStatus, validate_cooldown_probe


def _make_probe(**kwargs: Any) -> CooldownProbe:
    defaults: dict[str, object] = {
        "probe_id": "probe-1",
        "provider_identity": "gh",
        "credential_identity": "cred",
        "cooldown_generation_id": "gen-1",
        "status": ProbeStatus.PENDING,
        "scheduled_at": datetime.now(UTC),
    }
    defaults.update(kwargs)
    return CooldownProbe(**cast(Any, defaults))


def test_rejects_negative_retry_count() -> None:
    with pytest.raises(ValueError, match="retry_count"):
        validate_cooldown_probe(_make_probe(status=ProbeStatus.FAILED, retry_count=-1))


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"probe_id": ""}, "probe_id"),
        ({"provider_identity": ""}, "provider_identity"),
        ({"credential_identity": ""}, "credential_identity"),
        ({"cooldown_generation_id": ""}, "cooldown_generation_id"),
    ],
)
def test_rejects_blank_required_fields(kwargs: dict[str, str], match: str) -> None:
    with pytest.raises(ValueError, match=match):
        validate_cooldown_probe(_make_probe(**kwargs))


def test_accepts_optional_timestamps() -> None:
    validate_cooldown_probe(
        _make_probe(
            status=ProbeStatus.FAILED,
            attempted_at=datetime.now(UTC),
            resume_at=datetime.now(UTC),
            next_probe_at=datetime.now(UTC),
        )
    )
