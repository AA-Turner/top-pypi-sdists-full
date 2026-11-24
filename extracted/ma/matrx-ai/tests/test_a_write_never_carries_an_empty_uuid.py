"""P8-RUNS guard: no queued write carries "" in a uuid column (chat.tool_call id '' crashed turns)."""

import pytest

from matrx_ai.persistence.queue_helpers import EmptyIdWriteError, normalize_empty_uuid_fields


def test_empty_row_id_is_refused_by_name():
    with pytest.raises(EmptyIdWriteError):
        normalize_empty_uuid_fields("chat.tool_call", {"id": "", "tool_name": "x"})


def test_empty_primary_key_is_refused_by_name():
    with pytest.raises(EmptyIdWriteError):
        normalize_empty_uuid_fields("chat.tool_call", {"status": "completed"}, primary_key=("id", ""))


def test_empty_uuid_column_becomes_null_never_a_blank_uuid():
    out = normalize_empty_uuid_fields(
        "chat.tool_call", {"id": "11111111-1111-1111-1111-111111111111", "message_id": "", "call_id": ""}
    )
    assert out["message_id"] is None
    assert out["call_id"] == ""  # call_id is provider text, not a uuid column


def test_a_real_payload_is_untouched():
    payload = {"id": "11111111-1111-1111-1111-111111111111", "message_id": None}
    assert normalize_empty_uuid_fields("chat.tool_call", payload) is payload
