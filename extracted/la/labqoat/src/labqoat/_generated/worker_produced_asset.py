"""Content digest of one verified available asset."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerProducedAsset:
    """Content digest of one verified available asset."""

    asset_sha: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerProducedAsset:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerProducedAsset")
        return cls(
            asset_sha=JsonDocument.expect_scalar(values["asset_sha"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("asset_sha", True, "str", "")])
