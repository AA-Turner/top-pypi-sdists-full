"""Volume"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Volume:
    """Volume"""

    bytes: int
    created_at: str
    files: int
    limit_bytes: int
    name: str
    updated_at: str
    version: int
    warning: str | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Volume:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Volume")
        return cls(
            bytes=JsonDocument.expect_scalar(values["bytes"], int),
            created_at=JsonDocument.expect_scalar(values["created_at"], str),
            files=JsonDocument.expect_scalar(values["files"], int),
            limit_bytes=JsonDocument.expect_scalar(values["limit_bytes"], int),
            name=JsonDocument.expect_scalar(values["name"], str),
            updated_at=JsonDocument.expect_scalar(values["updated_at"], str),
            version=JsonDocument.expect_scalar(values["version"], int),
            warning=JsonDocument.expect_optional_scalar(values.get("warning"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("bytes", True, "int", ""),
                ("created_at", True, "str", ""),
                ("files", True, "int", ""),
                ("limit_bytes", True, "int", ""),
                ("name", True, "str", ""),
                ("updated_at", True, "str", ""),
                ("version", True, "int", ""),
                ("warning", True, "str", ""),
            ],
        )
