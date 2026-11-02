"""Endpoint"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Endpoint:
    """Endpoint"""

    active_at: str | None
    buffer_containers: int
    created_at: str
    failures: int
    function: str
    last_failure: str | None
    max_containers: int
    min_containers: int
    name: str
    path: str
    public: bool
    replicas: Mapping[str, JsonValue]
    retry_at: str | None
    revision: int
    scaledown_window: int
    target_inputs: int
    updated_at: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Endpoint:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Endpoint")
        return cls(
            active_at=JsonDocument.expect_optional_scalar(values.get("active_at"), str),
            buffer_containers=JsonDocument.expect_scalar(values["buffer_containers"], int),
            created_at=JsonDocument.expect_scalar(values["created_at"], str),
            failures=JsonDocument.expect_scalar(values["failures"], int),
            function=JsonDocument.expect_scalar(values["function"], str),
            last_failure=JsonDocument.expect_optional_scalar(values.get("last_failure"), str),
            max_containers=JsonDocument.expect_scalar(values["max_containers"], int),
            min_containers=JsonDocument.expect_scalar(values["min_containers"], int),
            name=JsonDocument.expect_scalar(values["name"], str),
            path=JsonDocument.expect_scalar(values["path"], str),
            public=JsonDocument.expect_scalar(values["public"], bool),
            replicas=JsonDocument.expect_dict(values["replicas"]),
            retry_at=JsonDocument.expect_optional_scalar(values.get("retry_at"), str),
            revision=JsonDocument.expect_scalar(values["revision"], int),
            scaledown_window=JsonDocument.expect_scalar(values["scaledown_window"], int),
            target_inputs=JsonDocument.expect_scalar(values["target_inputs"], int),
            updated_at=JsonDocument.expect_scalar(values["updated_at"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("active_at", True, "str", ""),
                ("buffer_containers", True, "int", ""),
                ("created_at", True, "str", ""),
                ("failures", True, "int", ""),
                ("function", True, "str", ""),
                ("last_failure", True, "str", ""),
                ("max_containers", True, "int", ""),
                ("min_containers", True, "int", ""),
                ("name", True, "str", ""),
                ("path", True, "str", ""),
                ("public", True, "bool", ""),
                ("replicas", True, "Mapping[str, JsonValue]", ""),
                ("retry_at", True, "str", ""),
                ("revision", True, "int", ""),
                ("scaledown_window", True, "int", ""),
                ("target_inputs", True, "int", ""),
                ("updated_at", True, "str", ""),
            ],
        )
