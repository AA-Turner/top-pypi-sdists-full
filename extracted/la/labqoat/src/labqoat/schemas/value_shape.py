"""Generated structural numeric decoding after complete captured-schema validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.references import AssetRef, ResourceId, Sha256
from labqoat.schemas.value_decoder import ValueDecoder

if TYPE_CHECKING:
    from labqoat.schemas.schema_record import SchemaRecord


@dataclass(frozen=True)
class ValueShape:
    """Describe finite scalar/array shapes without reflecting on Python author declarations."""

    kinds: tuple[str, ...]
    item: ValueDecoder | None = None
    record: type[SchemaRecord] | None = None

    def decode(self, value: JsonValue) -> object:
        """Preserve JSON values while restoring Python integer/float types losslessly."""
        if self.item is not None and isinstance(value, list):
            return [self.item.decode(item) for item in value]
        if "asset" in self.kinds and value is not None:
            return self._asset(JsonDocument.expect_dict(value))
        if self.record is not None and isinstance(value, dict):
            return self.record.from_dict(value)
        if type(value) in (int, float):
            number = cast(int | float, value)
            if "number" in self.kinds:
                return float(number)
            return int(number)
        return value

    @staticmethod
    def _asset(value: JsonDocument) -> AssetRef:
        """Hydrate schema-annotated identities without downloads or authored contract discovery."""
        return AssetRef(
            id=ResourceId.parse(JsonDocument.expect_scalar(value["id"], str)),
            blob_sha256=Sha256.parse(JsonDocument.expect_scalar(value["blob_sha256"], str)),
            byte_size=JsonDocument.expect_scalar(value["byte_size"], int),
            media_type=JsonDocument.expect_scalar(value["media_type"], str),
        )
