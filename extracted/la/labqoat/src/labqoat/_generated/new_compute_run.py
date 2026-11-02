"""NewComputeRun"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.compute_publication import ComputePublication
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewComputeRun:
    """NewComputeRun"""

    arguments: Mapping[str, JsonValue]
    input_schema_digest: str
    name: str
    publication: ComputePublication
    location: str | None = None
    resources: Mapping[str, JsonValue] | None = None
    seed: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewComputeRun:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewComputeRun")
        return cls(
            arguments=JsonDocument.expect_dict(values["arguments"]),
            input_schema_digest=JsonDocument.expect_scalar(values["input_schema_digest"], str),
            location=JsonDocument.expect_optional_scalar(values.get("location"), str),
            name=JsonDocument.expect_scalar(values["name"], str),
            publication=ComputePublication.from_dict(JsonDocument.expect_dict(values["publication"])),
            resources=JsonDocument.expect_optional_dict(values.get("resources")),
            seed=JsonDocument.expect_optional_scalar(values.get("seed"), int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("arguments", True, "Mapping[str, JsonValue]", ""),
                ("input_schema_digest", True, "str", ""),
                ("location", False, "str", ""),
                ("name", True, "str", ""),
                ("publication", True, "ComputePublication", ""),
                ("resources", False, "Mapping[str, JsonValue]", ""),
                ("seed", False, "int", ""),
            ],
        )
