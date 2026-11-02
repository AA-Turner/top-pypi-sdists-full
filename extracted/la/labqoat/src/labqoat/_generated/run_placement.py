"""Admission, waiting blockers and GPU constraints with candidate fit and outcome."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class RunPlacement:
    """Admission, waiting blockers and GPU constraints with candidate fit and outcome."""

    candidates: list[JsonValue]
    selected_family: str | None
    acquisition: Mapping[str, JsonValue] | None = None
    admission: Mapping[str, JsonValue] | None = None
    container_preparation: Mapping[str, JsonValue] | None = None
    expected_family: str | None = None
    gpu_constraints: Mapping[str, JsonValue] | None = None
    location_policy: Mapping[str, JsonValue] | None = None
    observed: Mapping[str, JsonValue] | None = None
    placement_note: str | None = None
    runtime_handle: str | None = None
    selected_pricing: Mapping[str, JsonValue] | None = None
    waiting: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> RunPlacement:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for RunPlacement")
        return cls(
            acquisition=JsonDocument.expect_optional_dict(values.get("acquisition")),
            admission=JsonDocument.expect_optional_dict(values.get("admission")),
            candidates=list(JsonDocument.expect_list(values.get("candidates", []))),
            container_preparation=JsonDocument.expect_optional_dict(values.get("container_preparation")),
            expected_family=JsonDocument.expect_optional_scalar(values.get("expected_family"), str),
            gpu_constraints=JsonDocument.expect_optional_dict(values.get("gpu_constraints")),
            location_policy=JsonDocument.expect_optional_dict(values.get("location_policy")),
            observed=JsonDocument.expect_optional_dict(values.get("observed")),
            placement_note=JsonDocument.expect_optional_scalar(values.get("placement_note"), str),
            runtime_handle=JsonDocument.expect_optional_scalar(values.get("runtime_handle"), str),
            selected_family=JsonDocument.expect_optional_scalar(values.get("selected_family"), str),
            selected_pricing=JsonDocument.expect_optional_dict(values.get("selected_pricing")),
            waiting=JsonDocument.expect_optional_dict(values.get("waiting")),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("acquisition", False, "Mapping[str, JsonValue]", ""),
                ("admission", False, "Mapping[str, JsonValue]", ""),
                ("candidates", True, "list[JsonValue]", "JsonValue"),
                ("container_preparation", False, "Mapping[str, JsonValue]", ""),
                ("expected_family", False, "str", ""),
                ("gpu_constraints", False, "Mapping[str, JsonValue]", ""),
                ("location_policy", False, "Mapping[str, JsonValue]", ""),
                ("observed", False, "Mapping[str, JsonValue]", ""),
                ("placement_note", False, "str", ""),
                ("runtime_handle", False, "str", ""),
                ("selected_family", True, "str", ""),
                ("selected_pricing", False, "Mapping[str, JsonValue]", ""),
                ("waiting", False, "Mapping[str, JsonValue]", ""),
            ],
        )
