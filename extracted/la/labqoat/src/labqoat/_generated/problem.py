"""RFC 9457 Problem Details error representation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Problem:
    """RFC 9457 Problem Details error representation."""

    detail: str
    errors: list[JsonValue]
    instance: str
    status: int
    title: str
    type: str
    code: str | None = None
    remediation: str | None = None
    stage: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Problem:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Problem")
        return cls(
            code=JsonDocument.expect_optional_scalar(values.get("code"), str),
            detail=JsonDocument.expect_scalar(values["detail"], str),
            errors=list(JsonDocument.expect_list(values.get("errors", []))),
            instance=JsonDocument.expect_scalar(values["instance"], str),
            remediation=JsonDocument.expect_optional_scalar(values.get("remediation"), str),
            stage=JsonDocument.expect_optional_scalar(values.get("stage"), str),
            status=JsonDocument.expect_scalar(values["status"], int),
            title=JsonDocument.expect_scalar(values["title"], str),
            type=JsonDocument.expect_scalar(values["type"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("code", False, "str", ""),
                ("detail", True, "str", ""),
                ("errors", True, "list[JsonValue]", "JsonValue"),
                ("instance", True, "str", ""),
                ("remediation", False, "str", ""),
                ("stage", False, "str", ""),
                ("status", True, "int", ""),
                ("title", True, "str", ""),
                ("type", True, "str", ""),
            ],
        )
