"""Typed dataset arguments resolved before worker execution."""

import re
from dataclasses import dataclass, field
from typing import Generic, Self, TypeVar

from labqoat.json_document import JsonValue
from labqoat.references.named_reference import NamedReference
from labqoat.schemas.schema_record import SchemaRecord

RowT = TypeVar("RowT", covariant=True)
RecordT = TypeVar("RecordT", bound=SchemaRecord)


@dataclass(frozen=True, slots=True)
class DatasetRef(Generic[RowT]):
    """A dataset selection whose generated binding carries an exact expected schema."""

    repository: str
    revision: str = "latest"
    schema_digest: str | None = None
    _record_type: type[RowT] | None = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        """Validate the family and revision."""
        NamedReference.validate(self.repository, self.revision)
        if self.schema_digest is not None and re.fullmatch(r"sha256:[0-9a-f]{64}", self.schema_digest) is None:
            raise ValueError("Expected an algorithm-qualified dataset schema digest")
        if self._record_type is not None and (
            not issubclass(self._record_type, SchemaRecord) or self._record_type.schema_digest != self.schema_digest
        ):
            raise ValueError("Dataset reference requires a matching generated schema binding")

    def bind(self, record_type: type[RecordT]) -> "DatasetRef[RecordT]":
        """Attach the generated row model while preserving any serialized schema requirement."""
        if self.schema_digest is not None and self.schema_digest != record_type.schema_digest:
            raise ValueError("Dataset reference schema does not match the generated row model")
        return DatasetRef(self.repository, self.revision, record_type.schema_digest, _record_type=record_type)

    @property
    def record_type(self) -> type[RowT]:
        """Require a generated binding before typed row consumption."""
        if self._record_type is None:
            raise ValueError("Dataset rows require a generated schema binding")
        return self._record_type

    def document(self) -> dict[str, JsonValue]:
        """Serialize selection and expected schema identity without Python class objects."""
        value: dict[str, JsonValue] = {"repository": self.repository, "revision": self.revision}
        if self.schema_digest is not None:
            value["schema_digest"] = self.schema_digest
        return value

    @classmethod
    def parse(cls, value: str) -> Self:
        """Parse a dataset argument such as top/fixture@v1."""
        return cls(*NamedReference.parse(value))

    def __str__(self) -> str:
        """Return the canonical selector."""
        return f"{self.repository}@{self.revision}"
