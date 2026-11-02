"""Project"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.knowledge_objective import KnowledgeObjective
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Project:
    """Project"""

    active_runs: int
    archived: bool
    dashboards: int
    datasets: int
    description: str
    environment_id: str
    id: str
    inserted_at: str
    last_run_at: str | None
    name: str
    objectives: list[KnowledgeObjective]
    runs: int
    sequence: int
    apps: list[JsonValue] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Project:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Project")
        return cls(
            active_runs=JsonDocument.expect_scalar(values["active_runs"], int),
            apps=list(JsonDocument.expect_list(values.get("apps", []))),
            archived=JsonDocument.expect_scalar(values["archived"], bool),
            dashboards=JsonDocument.expect_scalar(values["dashboards"], int),
            datasets=JsonDocument.expect_scalar(values["datasets"], int),
            description=JsonDocument.expect_scalar(values["description"], str),
            environment_id=JsonDocument.expect_scalar(values["environment_id"], str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            last_run_at=JsonDocument.expect_optional_scalar(values.get("last_run_at"), str),
            name=JsonDocument.expect_scalar(values["name"], str),
            objectives=[
                KnowledgeObjective.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("objectives", []))
            ],
            runs=JsonDocument.expect_scalar(values["runs"], int),
            sequence=JsonDocument.expect_scalar(values["sequence"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("active_runs", True, "int", ""),
                ("apps", False, "list[JsonValue]", "JsonValue"),
                ("archived", True, "bool", ""),
                ("dashboards", True, "int", ""),
                ("datasets", True, "int", ""),
                ("description", True, "str", ""),
                ("environment_id", True, "str", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("last_run_at", True, "str", ""),
                ("name", True, "str", ""),
                ("objectives", True, "list[KnowledgeObjective]", "KnowledgeObjective"),
                ("runs", True, "int", ""),
                ("sequence", True, "int", ""),
            ],
        )
