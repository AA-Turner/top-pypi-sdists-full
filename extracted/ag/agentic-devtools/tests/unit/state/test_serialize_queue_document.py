"""Tests for serialize_queue_document()."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum, StrEnum

import pytest

from agentic_devtools.state import serialize_queue_document


class _SampleEnum(StrEnum):
    READY = "ready"


class _NumericEnum(Enum):
    COUNT = 3


class _BadEnum(Enum):
    BAD = object()


class TestSerializeQueueDocument:
    """Tests for queue document serialization."""

    def test_serializes_canonical_utf8_json_bytes(self) -> None:
        payload = {"b": 2, "a": 1}
        result = serialize_queue_document(payload)
        assert result == b'{"a":1,"b":2}'

    def test_serializes_aware_datetime_isoformat(self) -> None:
        timestamp = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
        result = serialize_queue_document({"when": timestamp})
        assert result == b'{"when":"2026-01-02T03:04:05+00:00"}'

    def test_serializes_string_enum_value(self) -> None:
        result = serialize_queue_document({"status": _SampleEnum.READY})
        assert result == b'{"status":"ready"}'

    def test_serializes_non_string_enum_value(self) -> None:
        result = serialize_queue_document({"count": _NumericEnum.COUNT})
        assert result == b'{"count":3}'

    def test_rejects_naive_datetime(self) -> None:
        with pytest.raises(TypeError, match="timezone-aware"):
            serialize_queue_document({"when": datetime(2026, 1, 2, 3, 4, 5)})

    def test_rejects_unsupported_enum_value_type(self) -> None:
        with pytest.raises(TypeError, match="Unsupported enum value type"):
            serialize_queue_document({"bad": _BadEnum.BAD})

    @pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
    def test_rejects_non_finite_floats(self, value: float) -> None:
        with pytest.raises(ValueError, match="Out of range float values"):
            serialize_queue_document({"bad": value})

    def test_rejects_unsupported_value_types(self) -> None:
        with pytest.raises(TypeError, match="not JSON serializable"):
            serialize_queue_document({"bad": {"set_value": {1, 2}}})
