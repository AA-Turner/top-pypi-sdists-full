"""Validated immutable ownership boundary for captured schema declarations."""

from dataclasses import dataclass, field

from labqoat.json_document import JsonValue
from labqoat.schemas.identity import Identity
from labqoat.schemas.schema_policy import SchemaPolicy
from labqoat.schemas.schema_validator import SchemaValidator


@dataclass(frozen=True)
class SchemaDocument:
    """Capture exact schema bytes and their full validator without authored imports."""

    canonical: bytes
    _validator: SchemaValidator = field(compare=False, repr=False)

    @property
    def digest(self) -> str:
        """Identify the immutable canonical schema document."""
        return "sha256:" + Identity.hash(self.canonical)

    @classmethod
    def capture(cls, schema: dict[str, JsonValue] | bool) -> "SchemaDocument":
        """Enforce the shared static protocol before compiling any schema behavior."""
        canonical = Identity.bytes(schema)
        SchemaPolicy.check(schema)
        return cls(canonical, SchemaValidator.compile(schema))

    def validate(self, value: JsonValue) -> None:
        """Validate JSON-domain values against the captured immutable schema."""
        Identity.check(value)
        self._validator.validate(value)
