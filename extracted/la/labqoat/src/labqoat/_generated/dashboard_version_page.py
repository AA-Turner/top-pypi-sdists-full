"""One bounded page of dashboard versions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.dashboard import Dashboard
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DashboardVersionPage:
    """One bounded page of dashboard versions."""

    items: list[Dashboard]
    next_cursor: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DashboardVersionPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DashboardVersionPage")
        return cls(
            items=[
                Dashboard.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[Dashboard]", "Dashboard"), ("next_cursor", False, "str", "")]
        )
