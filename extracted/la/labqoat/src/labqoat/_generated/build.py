"""A build recipe with canonical state."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Build:
    """A build recipe with canonical state."""

    id: str
    links: Mapping[str, JsonValue]
    state: str
    status: str
    failure_detail: str | None = None
    family_name: str | None = None
    image_ref: str | None = None
    inserted_at: str | None = None
    kind: str | None = None
    phases: list[JsonValue] | None = field(default_factory=list)
    progress: Mapping[str, JsonValue] | None = None
    recipe: Mapping[str, JsonValue] | None = None
    recipe_digest: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Build:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Build")
        return cls(
            failure_detail=JsonDocument.expect_optional_scalar(values.get("failure_detail"), str),
            family_name=JsonDocument.expect_optional_scalar(values.get("family_name"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            image_ref=JsonDocument.expect_optional_scalar(values.get("image_ref"), str),
            inserted_at=JsonDocument.expect_optional_scalar(values.get("inserted_at"), str),
            kind=JsonDocument.expect_optional_scalar(values.get("kind"), str),
            links=JsonDocument.expect_dict(values["links"]),
            phases=list(JsonDocument.expect_list(values.get("phases", []))),
            progress=JsonDocument.expect_optional_dict(values.get("progress")),
            recipe=JsonDocument.expect_optional_dict(values.get("recipe")),
            recipe_digest=JsonDocument.expect_optional_scalar(values.get("recipe_digest"), str),
            state=JsonDocument.expect_scalar(values["state"], str),
            status=JsonDocument.expect_scalar(values["status"], str),
            updated_at=JsonDocument.expect_optional_scalar(values.get("updated_at"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("failure_detail", False, "str", ""),
                ("family_name", False, "str", ""),
                ("id", True, "str", ""),
                ("image_ref", False, "str", ""),
                ("inserted_at", False, "str", ""),
                ("kind", False, "str", ""),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("phases", False, "list[JsonValue]", "JsonValue"),
                ("progress", False, "Mapping[str, JsonValue]", ""),
                ("recipe", False, "Mapping[str, JsonValue]", ""),
                ("recipe_digest", False, "str", ""),
                ("state", True, "str", ""),
                ("status", True, "str", ""),
                ("updated_at", False, "str", ""),
            ],
        )
