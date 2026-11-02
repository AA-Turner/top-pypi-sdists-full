"""DistributedGroupPage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.distributed_group import DistributedGroup
from labqoat._generated.distributed_rank import DistributedRank
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DistributedGroupPage:
    """DistributedGroupPage"""

    group: DistributedGroup
    items: list[DistributedRank]
    next_cursor: str | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DistributedGroupPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DistributedGroupPage")
        return cls(
            group=DistributedGroup.from_dict(JsonDocument.expect_dict(values["group"])),
            items=[
                DistributedRank.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("group", True, "DistributedGroup", ""),
                ("items", True, "list[DistributedRank]", "DistributedRank"),
                ("next_cursor", True, "str", ""),
            ],
        )
