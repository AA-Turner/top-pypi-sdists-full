"""Tests for _sanitize_attribute_value()."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum, StrEnum

import pytest

from agentic_devtools.cli.ci.reconciliation.metric_attributes import _sanitize_attribute_value


class _TextValue(StrEnum):
    READY = "ready"


class _NumericValue(Enum):
    COUNT = 3


def test_sanitizes_supported_values() -> None:
    aware_datetime = datetime(2024, 1, 2, 3, 4, 5, tzinfo=UTC)

    assert _sanitize_attribute_value("text") == "text"
    assert _sanitize_attribute_value(3) == 3
    assert _sanitize_attribute_value(2.5) == 2.5
    assert _sanitize_attribute_value(True) is True
    assert _sanitize_attribute_value(None) is None
    assert _sanitize_attribute_value(aware_datetime) == "2024-01-02T03:04:05+00:00"
    assert _sanitize_attribute_value(_TextValue.READY) == "ready"
    assert _sanitize_attribute_value(_NumericValue.COUNT) == 3
    assert _sanitize_attribute_value([1, 2]) == (1, 2)
    assert _sanitize_attribute_value((1, 2)) == (1, 2)
    assert _sanitize_attribute_value({2, 1}) == (1, 2)
    assert _sanitize_attribute_value(frozenset({2, 1})) == (1, 2)


def test_rejects_naive_datetime() -> None:
    with pytest.raises(TypeError, match="timezone-aware"):
        _sanitize_attribute_value(datetime(2024, 1, 2, 3, 4, 5))


def test_redacts_unsupported_object() -> None:
    assert _sanitize_attribute_value(object()) == "<redacted:object>"
