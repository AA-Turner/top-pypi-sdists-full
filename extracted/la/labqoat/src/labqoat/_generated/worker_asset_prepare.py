"""Content identity with transfer purpose for one staged upload."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerAssetPrepare:
    """Content identity with transfer purpose for one staged upload."""

    byte_size: int
    media_type: str
    purpose: str
    sha256: str
    filename: str | None = None
    license: str | None = None
    provenance: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerAssetPrepare:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerAssetPrepare")
        return cls(
            byte_size=JsonDocument.expect_scalar(values["byte_size"], int),
            filename=JsonDocument.expect_optional_scalar(values.get("filename"), str),
            license=JsonDocument.expect_optional_scalar(values.get("license"), str),
            media_type=JsonDocument.expect_scalar(values["media_type"], str),
            provenance=JsonDocument.expect_optional_dict(values.get("provenance")),
            purpose=JsonDocument.expect_scalar(values["purpose"], str),
            sha256=JsonDocument.expect_scalar(values["sha256"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("byte_size", True, "int", ""),
                ("filename", False, "str", ""),
                ("license", False, "str", ""),
                ("media_type", True, "str", ""),
                ("provenance", False, "Mapping[str, JsonValue]", ""),
                ("purpose", True, "str", ""),
                ("sha256", True, "str", ""),
            ],
        )
