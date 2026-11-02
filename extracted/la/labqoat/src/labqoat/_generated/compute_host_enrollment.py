"""ComputeHostEnrollment"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.compute_host import ComputeHost
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeHostEnrollment:
    """ComputeHostEnrollment"""

    agent_settings: Mapping[str, JsonValue]
    bootstrap_expires_at: str
    host: ComputeHost

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeHostEnrollment:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeHostEnrollment")
        return cls(
            agent_settings=JsonDocument.expect_dict(values["agent_settings"]),
            bootstrap_expires_at=JsonDocument.expect_scalar(values["bootstrap_expires_at"], str),
            host=ComputeHost.from_dict(JsonDocument.expect_dict(values["host"])),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("agent_settings", True, "Mapping[str, JsonValue]", ""),
                ("bootstrap_expires_at", True, "str", ""),
                ("host", True, "ComputeHost", ""),
            ],
        )
