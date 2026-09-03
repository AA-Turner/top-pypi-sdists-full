"""Tests for deserialize_queue_document()."""

from __future__ import annotations

import pytest

from agentic_devtools.state import deserialize_queue_document


class TestDeserializeQueueDocument:
    """Tests for queue document deserialization."""

    def test_deserializes_utf8_json_object(self) -> None:
        result = deserialize_queue_document(b'{"a":1,"b":"two"}')
        assert result == {"a": 1, "b": "two"}

    def test_raises_for_invalid_utf8_or_json(self) -> None:
        with pytest.raises(ValueError, match="Invalid queue document bytes"):
            deserialize_queue_document(b"\xff")

    def test_raises_for_non_object_json(self) -> None:
        with pytest.raises(ValueError, match="Queue document must be a JSON object"):
            deserialize_queue_document(b'["not","an","object"]')

    @pytest.mark.parametrize("payload", [b'{"value":NaN}', b'{"value":Infinity}', b'{"value":-Infinity}'])
    def test_raises_for_non_finite_number_literals(self, payload: bytes) -> None:
        with pytest.raises(ValueError, match="must not contain non-finite numbers"):
            deserialize_queue_document(payload)
