"""ProjectMoveResult"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ProjectMoveResult:
    """ProjectMoveResult"""

    dashboards: int
    datasets: int
    project: str
    runs: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ProjectMoveResult:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ProjectMoveResult")
        return cls(
            dashboards=JsonDocument.expect_scalar(values["dashboards"], int),
            datasets=JsonDocument.expect_scalar(values["datasets"], int),
            project=JsonDocument.expect_scalar(values["project"], str),
            runs=JsonDocument.expect_scalar(values["runs"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("dashboards", True, "int", ""),
                ("datasets", True, "int", ""),
                ("project", True, "str", ""),
                ("runs", True, "int", ""),
            ],
        )
