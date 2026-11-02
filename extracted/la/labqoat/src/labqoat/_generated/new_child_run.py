"""NewChildRun"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.new_compute_run import NewComputeRun
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewChildRun:
    """NewChildRun"""

    key: str
    request: NewComputeRun

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewChildRun:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewChildRun")
        return cls(
            key=JsonDocument.expect_scalar(values["key"], str),
            request=NewComputeRun.from_dict(JsonDocument.expect_dict(values["request"])),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("key", True, "str", ""), ("request", True, "NewComputeRun", "")])
