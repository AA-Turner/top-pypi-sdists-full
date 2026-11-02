"""One bounded page of workers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.worker import Worker
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerPage:
    """One bounded page of workers."""

    items: list[Worker]
    next_cursor: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerPage")
        return cls(
            items=[
                Worker.from_dict(JsonDocument.expect_dict(v)) for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[Worker]", "Worker"), ("next_cursor", False, "str", "")]
        )
