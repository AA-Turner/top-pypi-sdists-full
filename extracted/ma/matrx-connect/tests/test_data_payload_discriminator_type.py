"""Typed payload specialization keeps the runtime stream discriminator exact."""

from typing import Literal

import pytest
from pydantic import ValidationError

from matrx_connect.context.data_types import ConversationIdData, DataPayload


class NamedPayload(DataPayload[Literal["named"]]):
    type: Literal["named"] = "named"
    message: str


def test_specialized_payload_keeps_its_literal_and_native_values() -> None:
    payload = NamedPayload(message="hello")
    assert payload.model_dump() == {"type": "named", "message": "hello"}
    assert NamedPayload.model_json_schema()["properties"]["type"] == {
        "const": "named", "default": "named", "title": "Type", "type": "string",
    }
    with pytest.raises(ValidationError):
        NamedPayload.model_validate({"type": "wrong", "message": "hello"})
    with pytest.raises(ValidationError):
        NamedPayload.model_validate({"message": "hello", "extra": True})


def test_bare_payload_and_existing_subclass_keep_their_contracts() -> None:
    assert DataPayload(type="custom").model_dump() == {"type": "custom"}
    assert DataPayload.model_json_schema() == {
        "additionalProperties": False,
        "properties": {"type": {"title": "Type", "type": "string"}},
        "required": ["type"], "title": "DataPayload", "type": "object",
    }
    with pytest.raises(ValidationError):
        DataPayload.model_validate({"type": 4})
    assert ConversationIdData(conversation_id="id").model_dump() == {
        "type": "conversation_id", "conversation_id": "id",
    }
