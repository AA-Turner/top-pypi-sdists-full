"""ForkPage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.fork_lineage import ForkLineage
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ForkPage:
    """ForkPage"""

    items: list[ForkLineage]
    next_cursor: str | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ForkPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ForkPage")
        return cls(
            items=[
                ForkLineage.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[ForkLineage]", "ForkLineage"), ("next_cursor", True, "str", "")]
        )
