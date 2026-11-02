"""Immutable static manifest declarations, independent of authored Python imports."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.manifests.manifest_formats import ManifestFormats
from labqoat.manifests.manifest_schemas import ManifestSchemas
from labqoat.schemas.identity import Identity
from labqoat.schemas.schema_validator import SchemaValidator


@dataclass(frozen=True)
class Manifest:
    """Own one versioned manifest as canonical bytes rather than a mutable mapping."""

    kind: str
    canonical: bytes

    @classmethod
    def capture(cls, kind: str, value: JsonValue) -> "Manifest":
        """Check declaration shape, captured schemas, and immutable requirements."""
        canonical = Identity.bytes(value)
        SchemaValidator.compile(ManifestFormats.schema(kind)).validate(value)
        ManifestSchemas.validate(kind, JsonDocument.expect_dict(value))
        return cls(kind, canonical)

    @classmethod
    def decode(cls, kind: str, text: str) -> "Manifest":
        """Reject ambiguous JSON before manifest validation or identity creation."""
        return cls.capture(kind, Identity.decode(text))

    @property
    def digest(self) -> str:
        """Return the exact immutable declaration identity."""
        return "sha256:" + Identity.hash(self.canonical)

    @property
    def document(self) -> JsonDocument:
        """Decode a fresh copy so edits cannot mutate the captured identity."""
        return JsonDocument.expect_dict(Identity.decode(self.canonical.decode("utf-8")))
