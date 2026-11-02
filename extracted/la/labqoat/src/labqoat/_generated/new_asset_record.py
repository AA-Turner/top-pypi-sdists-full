"""Content identity to register as pending."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewAssetRecord:
    """Content identity to register as pending."""

    byte_size: int
    media_type: str
    sha256: str
    audio_metadata: Mapping[str, JsonValue] | None = None
    filename: str | None = None
    license: str | None = None
    pcm_identity: str | None = None
    provenance: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewAssetRecord:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewAssetRecord")
        return cls(
            audio_metadata=JsonDocument.expect_optional_dict(values.get("audio_metadata")),
            byte_size=JsonDocument.expect_scalar(values["byte_size"], int),
            filename=JsonDocument.expect_optional_scalar(values.get("filename"), str),
            license=JsonDocument.expect_optional_scalar(values.get("license"), str),
            media_type=JsonDocument.expect_scalar(values["media_type"], str),
            pcm_identity=JsonDocument.expect_optional_scalar(values.get("pcm_identity"), str),
            provenance=JsonDocument.expect_optional_dict(values.get("provenance")),
            sha256=JsonDocument.expect_scalar(values["sha256"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("audio_metadata", False, "Mapping[str, JsonValue]", ""),
                ("byte_size", True, "int", ""),
                ("filename", False, "str", ""),
                ("license", False, "str", ""),
                ("media_type", True, "str", ""),
                ("pcm_identity", False, "str", ""),
                ("provenance", False, "Mapping[str, JsonValue]", ""),
                ("sha256", True, "str", ""),
            ],
        )
