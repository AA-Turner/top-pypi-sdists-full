"""A workload execution attempt with placement."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Worker:
    """A workload execution attempt with placement."""

    id: str
    active: bool | None = None
    credential_expires_at: str | None = None
    ended_at: str | None = None
    inserted_at: str | None = None
    lease_expires_at: str | None = None
    node_id: str | None = None
    placement: Mapping[str, JsonValue] | None = None
    run_id: str | None = None
    runtime_handle: str | None = None
    started_at: str | None = None
    state: str | None = None
    workload_kind: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Worker:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Worker")
        return cls(
            active=JsonDocument.expect_optional_scalar(values.get("active"), bool),
            credential_expires_at=JsonDocument.expect_optional_scalar(values.get("credential_expires_at"), str),
            ended_at=JsonDocument.expect_optional_scalar(values.get("ended_at"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_optional_scalar(values.get("inserted_at"), str),
            lease_expires_at=JsonDocument.expect_optional_scalar(values.get("lease_expires_at"), str),
            node_id=JsonDocument.expect_optional_scalar(values.get("node_id"), str),
            placement=JsonDocument.expect_optional_dict(values.get("placement")),
            run_id=JsonDocument.expect_optional_scalar(values.get("run_id"), str),
            runtime_handle=JsonDocument.expect_optional_scalar(values.get("runtime_handle"), str),
            started_at=JsonDocument.expect_optional_scalar(values.get("started_at"), str),
            state=JsonDocument.expect_optional_scalar(values.get("state"), str),
            workload_kind=JsonDocument.expect_optional_scalar(values.get("workload_kind"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("active", False, "bool", ""),
                ("credential_expires_at", False, "str", ""),
                ("ended_at", False, "str", ""),
                ("id", True, "str", ""),
                ("inserted_at", False, "str", ""),
                ("lease_expires_at", False, "str", ""),
                ("node_id", False, "str", ""),
                ("placement", False, "Mapping[str, JsonValue]", ""),
                ("run_id", False, "str", ""),
                ("runtime_handle", False, "str", ""),
                ("started_at", False, "str", ""),
                ("state", False, "str", ""),
                ("workload_kind", False, "str", ""),
            ],
        )
