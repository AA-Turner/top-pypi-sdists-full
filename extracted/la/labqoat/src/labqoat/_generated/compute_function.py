"""ComputeFunction"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.automatic_recovery_policy import AutomaticRecoveryPolicy
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeFunction:
    """ComputeFunction"""

    context_parameter: str
    input_schema: Mapping[str, JsonValue]
    module: str
    name: str
    output_schema: Mapping[str, JsonValue]
    resources: Mapping[str, JsonValue]
    timeout_seconds: int
    automatic_recovery: AutomaticRecoveryPolicy | None = None
    class_name: str | None = None
    fit_budget_ms: int | None = None
    initializer: str | None = None
    location: str | None = None
    memory_snapshot: int | None = None
    queue_timeout_seconds: int | None = None
    recovery: Mapping[str, JsonValue] | None = None
    resume: Mapping[str, JsonValue] | None = None
    retries: int | None = None
    reuse: int | None = None
    sandboxes: Mapping[str, JsonValue] | None = None
    secrets: list[JsonValue] | None = None
    snapshot_initializer: str | None = None
    volumes: Mapping[str, JsonValue] | None = None
    workers: Mapping[str, JsonValue] | None = None
    workflow_replay: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeFunction:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeFunction")
        return cls(
            automatic_recovery=AutomaticRecoveryPolicy.from_dict(
                JsonDocument.expect_dict(values.get("automatic_recovery"))
            )
            if values.get("automatic_recovery") is not None
            else None,
            class_name=JsonDocument.expect_optional_scalar(values.get("class_name"), str),
            context_parameter=JsonDocument.expect_scalar(values["context_parameter"], str),
            fit_budget_ms=JsonDocument.expect_optional_scalar(values.get("fit_budget_ms"), int),
            initializer=JsonDocument.expect_optional_scalar(values.get("initializer"), str),
            input_schema=JsonDocument.expect_dict(values["input_schema"]),
            location=JsonDocument.expect_optional_scalar(values.get("location"), str),
            memory_snapshot=JsonDocument.expect_optional_scalar(values.get("memory_snapshot"), int),
            module=JsonDocument.expect_scalar(values["module"], str),
            name=JsonDocument.expect_scalar(values["name"], str),
            output_schema=JsonDocument.expect_dict(values["output_schema"]),
            queue_timeout_seconds=JsonDocument.expect_optional_scalar(values.get("queue_timeout_seconds"), int),
            recovery=JsonDocument.expect_optional_dict(values.get("recovery")),
            resources=JsonDocument.expect_dict(values["resources"]),
            resume=JsonDocument.expect_optional_dict(values.get("resume")),
            retries=JsonDocument.expect_optional_scalar(values.get("retries"), int),
            reuse=JsonDocument.expect_optional_scalar(values.get("reuse"), int),
            sandboxes=JsonDocument.expect_optional_dict(values.get("sandboxes")),
            secrets=list(JsonDocument.expect_list(values["secrets"])) if "secrets" in values else None,
            snapshot_initializer=JsonDocument.expect_optional_scalar(values.get("snapshot_initializer"), str),
            timeout_seconds=JsonDocument.expect_scalar(values["timeout_seconds"], int),
            volumes=JsonDocument.expect_optional_dict(values.get("volumes")),
            workers=JsonDocument.expect_optional_dict(values.get("workers")),
            workflow_replay=JsonDocument.expect_optional_scalar(values.get("workflow_replay"), int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("automatic_recovery", False, "AutomaticRecoveryPolicy", ""),
                ("class_name", False, "str", ""),
                ("context_parameter", True, "str", ""),
                ("fit_budget_ms", False, "int", ""),
                ("initializer", False, "str", ""),
                ("input_schema", True, "Mapping[str, JsonValue]", ""),
                ("location", False, "str", ""),
                ("memory_snapshot", False, "int", ""),
                ("module", True, "str", ""),
                ("name", True, "str", ""),
                ("output_schema", True, "Mapping[str, JsonValue]", ""),
                ("queue_timeout_seconds", False, "int", ""),
                ("recovery", False, "Mapping[str, JsonValue]", ""),
                ("resources", True, "Mapping[str, JsonValue]", ""),
                ("resume", False, "Mapping[str, JsonValue]", ""),
                ("retries", False, "int", ""),
                ("reuse", False, "int", ""),
                ("sandboxes", False, "Mapping[str, JsonValue]", ""),
                ("secrets", False, "list[JsonValue]", "JsonValue"),
                ("snapshot_initializer", False, "str", ""),
                ("timeout_seconds", True, "int", ""),
                ("volumes", False, "Mapping[str, JsonValue]", ""),
                ("workers", False, "Mapping[str, JsonValue]", ""),
                ("workflow_replay", False, "int", ""),
            ],
        )
