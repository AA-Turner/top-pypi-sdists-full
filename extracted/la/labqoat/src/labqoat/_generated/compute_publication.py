"""ComputePublication"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.compute_function import ComputeFunction
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputePublication:
    """ComputePublication"""

    app_name: str
    bindings: Mapping[str, JsonValue]
    function: ComputeFunction
    image: str
    images: Mapping[str, JsonValue]
    runtime_version: str
    source_asset_sha: str
    app: Mapping[str, JsonValue] | None = None
    distributed_recovery_protocol: int | None = None
    recovery_protocol: int | None = None
    workflow_replay_protocol: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputePublication:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputePublication")
        return cls(
            app=JsonDocument.expect_optional_dict(values.get("app")),
            app_name=JsonDocument.expect_scalar(values["app_name"], str),
            bindings=JsonDocument.expect_dict(values["bindings"]),
            distributed_recovery_protocol=JsonDocument.expect_optional_scalar(
                values.get("distributed_recovery_protocol"), int
            ),
            function=ComputeFunction.from_dict(JsonDocument.expect_dict(values["function"])),
            image=JsonDocument.expect_scalar(values["image"], str),
            images=JsonDocument.expect_dict(values["images"]),
            recovery_protocol=JsonDocument.expect_optional_scalar(values.get("recovery_protocol"), int),
            runtime_version=JsonDocument.expect_scalar(values["runtime_version"], str),
            source_asset_sha=JsonDocument.expect_scalar(values["source_asset_sha"], str),
            workflow_replay_protocol=JsonDocument.expect_optional_scalar(values.get("workflow_replay_protocol"), int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("app", False, "Mapping[str, JsonValue]", ""),
                ("app_name", True, "str", ""),
                ("bindings", True, "Mapping[str, JsonValue]", ""),
                ("distributed_recovery_protocol", False, "int", ""),
                ("function", True, "ComputeFunction", ""),
                ("image", True, "str", ""),
                ("images", True, "Mapping[str, JsonValue]", ""),
                ("recovery_protocol", False, "int", ""),
                ("runtime_version", True, "str", ""),
                ("source_asset_sha", True, "str", ""),
                ("workflow_replay_protocol", False, "int", ""),
            ],
        )
