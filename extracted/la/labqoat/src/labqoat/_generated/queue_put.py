"""QueuePut"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.encoded_value import EncodedValue
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class QueuePut:
    """QueuePut"""

    values: list[EncodedValue]
    partition: str | None = None
    partition_ttl: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> QueuePut:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for QueuePut")
        return cls(
            partition=JsonDocument.expect_optional_scalar(values.get("partition"), str),
            partition_ttl=JsonDocument.expect_optional_scalar(values.get("partition_ttl"), int),
            values=[
                EncodedValue.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("values", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("partition", False, "str", ""),
                ("partition_ttl", False, "int", ""),
                ("values", True, "list[EncodedValue]", "EncodedValue"),
            ],
        )
