"""Known wake schemas share count and serialized-byte limits across all writers."""

import pytest

from agentic_devtools.cli.ci.cooldown_document import (
    MAX_WAKE_DOCUMENT_BYTES,
    MAX_WAKE_ENTRIES,
    _validate_wake_document,
)


class TestValidateWakeDocument:
    def test_known_schema_rejects_oversized_union(self):
        payload = {"dispatcher_wakes": {"version": 1, "entries": dict.fromkeys(range(MAX_WAKE_ENTRIES + 1))}}
        with pytest.raises(ValueError, match="capacity"):
            _validate_wake_document(payload, "{}")

    def test_known_schema_accepts_capacity_and_rejects_encoded_byte_overflow(self):
        payload = {"dispatcher_wakes": {"version": 1, "entries": dict.fromkeys(range(MAX_WAKE_ENTRIES))}}
        _validate_wake_document(payload, "x" * MAX_WAKE_DOCUMENT_BYTES)
        with pytest.raises(ValueError, match="size"):
            _validate_wake_document(payload, "é" * (MAX_WAKE_DOCUMENT_BYTES // 2 + 1))

    @pytest.mark.parametrize(
        "extension",
        [None, [], {"version": 9, "entries": {}}, {"version": True, "entries": {}}, {"version": 1, "entries": []}],
    )
    def test_unknown_schemas_remain_tolerated(self, extension):
        _validate_wake_document({"dispatcher_wakes": extension}, "x" * (MAX_WAKE_DOCUMENT_BYTES + 1))
