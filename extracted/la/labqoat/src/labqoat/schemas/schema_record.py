"""Runtime validation boundary shared by statically generated schema records."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import TYPE_CHECKING, ClassVar, Self

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.identity import Identity

if TYPE_CHECKING:
    from labqoat.schemas.schema_document import SchemaDocument


class SchemaRecord(ABC):
    """Validate captured schemas while generated declarations own fields and structural decoding."""

    _schema: ClassVar[SchemaDocument]
    schema_digest: ClassVar[str]
    field_names: ClassVar[Mapping[str, str]]

    def __post_init__(self) -> None:
        """Validate every generated dataclass constructor without coercion or authored hooks."""
        self.to_dict()

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Self:
        """Validate full schema semantics before generated structural decoding of a private copy."""
        copied = JsonDocument.expect_dict(Identity.decode(Identity.bytes(dict(values)).decode("utf-8")))
        cls._schema.validate(copied)
        return cls._decode(copied)

    def to_dict(self) -> dict[str, JsonValue]:
        """Return independent JSON values, enforcing constraints even after nested-value mutation."""
        from labqoat.schemas.record_values import RecordValues

        if self.schema_digest != self._schema.digest:
            raise ValueError("Generated record schema identity mismatch")
        values = RecordValues.encode(dict(self._encode()))
        self._schema.validate(values)
        return JsonDocument.expect_dict(Identity.decode(Identity.bytes(values).decode("utf-8")))

    @abstractmethod
    def _encode(self) -> Mapping[str, object]:
        """Serialize only the schema properties declared by the generated record."""

    @classmethod
    @abstractmethod
    def _decode(cls, values: JsonDocument) -> Self:
        """Construct typed fields using generated schema-owned decoding."""
