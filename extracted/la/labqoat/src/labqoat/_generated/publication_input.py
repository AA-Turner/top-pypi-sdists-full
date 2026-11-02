"""PublicationInput"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class PublicationInput:
    """PublicationInput"""

    byte_size: int
    format: str
    path: str
    sha256: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> PublicationInput:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for PublicationInput")
        return cls(
            byte_size=JsonDocument.expect_scalar(values["byte_size"], int),
            format=JsonDocument.expect_scalar(values["format"], str),
            path=JsonDocument.expect_scalar(values["path"], str),
            sha256=JsonDocument.expect_scalar(values["sha256"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("byte_size", True, "int", ""),
                ("format", True, "str", ""),
                ("path", True, "str", ""),
                ("sha256", True, "str", ""),
            ],
        )
