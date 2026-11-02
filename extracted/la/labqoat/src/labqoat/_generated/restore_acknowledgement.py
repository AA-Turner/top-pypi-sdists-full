"""RestoreAcknowledgement"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class RestoreAcknowledgement:
    """RestoreAcknowledgement"""

    checkpoint_id: str
    manifest_digest: str
    plan_digest: str
    progress: Mapping[str, JsonValue]
    state: list[JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> RestoreAcknowledgement:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for RestoreAcknowledgement")
        return cls(
            checkpoint_id=JsonDocument.expect_scalar(values["checkpoint_id"], str),
            manifest_digest=JsonDocument.expect_scalar(values["manifest_digest"], str),
            plan_digest=JsonDocument.expect_scalar(values["plan_digest"], str),
            progress=JsonDocument.expect_dict(values["progress"]),
            state=list(JsonDocument.expect_list(values.get("state", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("checkpoint_id", True, "str", ""),
                ("manifest_digest", True, "str", ""),
                ("plan_digest", True, "str", ""),
                ("progress", True, "Mapping[str, JsonValue]", ""),
                ("state", True, "list[JsonValue]", "JsonValue"),
            ],
        )
