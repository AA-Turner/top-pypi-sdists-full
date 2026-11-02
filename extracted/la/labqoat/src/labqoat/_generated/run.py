"""A submitted execution with canonical lifecycle state."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Run:
    """A submitted execution with canonical lifecycle state."""

    id: str
    links: Mapping[str, JsonValue]
    name: str
    status: str
    app: str | None = None
    build_id: str | None = None
    child_operation_key: str | None = None
    cleanup: Mapping[str, JsonValue] | None = None
    coordination: Mapping[str, JsonValue] | None = None
    creator: str | None = None
    ended_at: str | None = None
    failure_detail: Mapping[str, JsonValue] | None = None
    inserted_at: str | None = None
    kind: str | None = None
    manifest: Mapping[str, JsonValue] | None = None
    owner_run_id: str | None = None
    project: str | None = None
    shards: list[JsonValue] | None = field(default_factory=list)
    started_at: str | None = None
    state: str | None = None
    state_version: int | None = None
    tags: list[JsonValue] | None = field(default_factory=list)
    terminal: bool | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Run:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Run")
        return cls(
            app=JsonDocument.expect_optional_scalar(values.get("app"), str),
            build_id=JsonDocument.expect_optional_scalar(values.get("build_id"), str),
            child_operation_key=JsonDocument.expect_optional_scalar(values.get("child_operation_key"), str),
            cleanup=JsonDocument.expect_optional_dict(values.get("cleanup")),
            coordination=JsonDocument.expect_optional_dict(values.get("coordination")),
            creator=JsonDocument.expect_optional_scalar(values.get("creator"), str),
            ended_at=JsonDocument.expect_optional_scalar(values.get("ended_at"), str),
            failure_detail=JsonDocument.expect_optional_dict(values.get("failure_detail")),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_optional_scalar(values.get("inserted_at"), str),
            kind=JsonDocument.expect_optional_scalar(values.get("kind"), str),
            links=JsonDocument.expect_dict(values["links"]),
            manifest=JsonDocument.expect_optional_dict(values.get("manifest")),
            name=JsonDocument.expect_scalar(values["name"], str),
            owner_run_id=JsonDocument.expect_optional_scalar(values.get("owner_run_id"), str),
            project=JsonDocument.expect_optional_scalar(values.get("project"), str),
            shards=list(JsonDocument.expect_list(values.get("shards", []))),
            started_at=JsonDocument.expect_optional_scalar(values.get("started_at"), str),
            state=JsonDocument.expect_optional_scalar(values.get("state"), str),
            state_version=JsonDocument.expect_optional_scalar(values.get("state_version"), int),
            status=JsonDocument.expect_scalar(values["status"], str),
            tags=list(JsonDocument.expect_list(values.get("tags", []))),
            terminal=JsonDocument.expect_optional_scalar(values.get("terminal"), bool),
            updated_at=JsonDocument.expect_optional_scalar(values.get("updated_at"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("app", False, "str", ""),
                ("build_id", False, "str", ""),
                ("child_operation_key", False, "str", ""),
                ("cleanup", False, "Mapping[str, JsonValue]", ""),
                ("coordination", False, "Mapping[str, JsonValue]", ""),
                ("creator", False, "str", ""),
                ("ended_at", False, "str", ""),
                ("failure_detail", False, "Mapping[str, JsonValue]", ""),
                ("id", True, "str", ""),
                ("inserted_at", False, "str", ""),
                ("kind", False, "str", ""),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("manifest", False, "Mapping[str, JsonValue]", ""),
                ("name", True, "str", ""),
                ("owner_run_id", False, "str", ""),
                ("project", False, "str", ""),
                ("shards", False, "list[JsonValue]", "JsonValue"),
                ("started_at", False, "str", ""),
                ("state", False, "str", ""),
                ("state_version", False, "int", ""),
                ("status", True, "str", ""),
                ("tags", False, "list[JsonValue]", "JsonValue"),
                ("terminal", False, "bool", ""),
                ("updated_at", False, "str", ""),
            ],
        )
