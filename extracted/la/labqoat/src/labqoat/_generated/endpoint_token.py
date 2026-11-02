"""EndpointToken"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class EndpointToken:
    """EndpointToken"""

    created_at: str
    last_used_at: str | None
    name: str
    prefix: str
    token: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> EndpointToken:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for EndpointToken")
        return cls(
            created_at=JsonDocument.expect_scalar(values["created_at"], str),
            last_used_at=JsonDocument.expect_optional_scalar(values.get("last_used_at"), str),
            name=JsonDocument.expect_scalar(values["name"], str),
            prefix=JsonDocument.expect_scalar(values["prefix"], str),
            token=JsonDocument.expect_optional_scalar(values.get("token"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("created_at", True, "str", ""),
                ("last_used_at", True, "str", ""),
                ("name", True, "str", ""),
                ("prefix", True, "str", ""),
                ("token", False, "str", ""),
            ],
        )
