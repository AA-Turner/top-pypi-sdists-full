"""RestoreReceipt"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.restore_acknowledgement import RestoreAcknowledgement
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class RestoreReceipt:
    """RestoreReceipt"""

    attempt_id: str
    evidence: RestoreAcknowledgement
    fingerprint: str
    inserted_at: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> RestoreReceipt:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for RestoreReceipt")
        return cls(
            attempt_id=JsonDocument.expect_scalar(values["attempt_id"], str),
            evidence=RestoreAcknowledgement.from_dict(JsonDocument.expect_dict(values["evidence"])),
            fingerprint=JsonDocument.expect_scalar(values["fingerprint"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", True, "str", ""),
                ("evidence", True, "RestoreAcknowledgement", ""),
                ("fingerprint", True, "str", ""),
                ("inserted_at", True, "str", ""),
            ],
        )
