"""MaterializedDatasetFile"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.publication_input import PublicationInput
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class MaterializedDatasetFile:
    """MaterializedDatasetFile"""

    asset_id: str
    byte_size: int
    evidence_digest: str
    format: str
    input: PublicationInput
    rows: int
    sha256: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> MaterializedDatasetFile:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for MaterializedDatasetFile")
        return cls(
            asset_id=JsonDocument.expect_scalar(values["asset_id"], str),
            byte_size=JsonDocument.expect_scalar(values["byte_size"], int),
            evidence_digest=JsonDocument.expect_scalar(values["evidence_digest"], str),
            format=JsonDocument.expect_scalar(values["format"], str),
            input=PublicationInput.from_dict(JsonDocument.expect_dict(values["input"])),
            rows=JsonDocument.expect_scalar(values["rows"], int),
            sha256=JsonDocument.expect_scalar(values["sha256"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("asset_id", True, "str", ""),
                ("byte_size", True, "int", ""),
                ("evidence_digest", True, "str", ""),
                ("format", True, "str", ""),
                ("input", True, "PublicationInput", ""),
                ("rows", True, "int", ""),
                ("sha256", True, "str", ""),
            ],
        )
