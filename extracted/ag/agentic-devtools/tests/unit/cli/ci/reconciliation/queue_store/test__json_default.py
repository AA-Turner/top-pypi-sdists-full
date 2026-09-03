"""Tests for _json_default()."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.reconciliation.models import WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import _json_default


def test_serializes_datetime() -> None:
    assert isinstance(_json_default(datetime.now(UTC)), str)


def test_serializes_enum() -> None:
    assert _json_default(WorkItemStatus.QUEUED) == "queued"


def test_raises_for_unsupported_values() -> None:
    with pytest.raises(TypeError):
        _json_default(object())
