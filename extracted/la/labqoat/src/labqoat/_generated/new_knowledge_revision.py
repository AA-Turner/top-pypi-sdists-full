"""NewKnowledgeRevision"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewKnowledgeRevision:
    """NewKnowledgeRevision"""

    expected_revision_id: str
    idempotency_key: str
    title: str
    attachments: list[JsonValue] | None = field(default_factory=list)
    attempt_id: str | None = None
    body: str | None = None
    client_label: str | None = None
    properties: Mapping[str, JsonValue] | None = None
    run_id: str | None = None
    schema_version: int | None = None
    summary: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewKnowledgeRevision:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewKnowledgeRevision")
        return cls(
            attachments=list(JsonDocument.expect_list(values.get("attachments", []))),
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            body=JsonDocument.expect_optional_scalar(values.get("body"), str),
            client_label=JsonDocument.expect_optional_scalar(values.get("client_label"), str),
            expected_revision_id=JsonDocument.expect_scalar(values["expected_revision_id"], str),
            idempotency_key=JsonDocument.expect_scalar(values["idempotency_key"], str),
            properties=JsonDocument.expect_optional_dict(values.get("properties")),
            run_id=JsonDocument.expect_optional_scalar(values.get("run_id"), str),
            schema_version=JsonDocument.expect_optional_scalar(values.get("schema_version"), int),
            summary=JsonDocument.expect_optional_scalar(values.get("summary"), str),
            title=JsonDocument.expect_scalar(values["title"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attachments", False, "list[JsonValue]", "JsonValue"),
                ("attempt_id", False, "str", ""),
                ("body", False, "str", ""),
                ("client_label", False, "str", ""),
                ("expected_revision_id", True, "str", ""),
                ("idempotency_key", True, "str", ""),
                ("properties", False, "Mapping[str, JsonValue]", ""),
                ("run_id", False, "str", ""),
                ("schema_version", False, "int", ""),
                ("summary", False, "str", ""),
                ("title", True, "str", ""),
            ],
        )
