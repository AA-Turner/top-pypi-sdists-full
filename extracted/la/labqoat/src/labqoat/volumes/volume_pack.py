"""Where a packed small file's bytes are stored: a range of one shared pack block."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat.json_document import JsonDocument, JsonValue


@dataclass(frozen=True)
class VolumePack:
    """The pack block ``digest`` of ``bytes`` bytes holds the file's content from ``offset``."""

    digest: str
    offset: int
    bytes: int

    @classmethod
    def from_dict(cls, document: Mapping[str, JsonValue]) -> VolumePack:
        """Read the wire form."""
        return cls(
            JsonDocument.expect_scalar(document["digest"], str),
            JsonDocument.expect_scalar(document["offset"], int),
            JsonDocument.expect_scalar(document["bytes"], int),
        )

    def to_dict(self) -> dict[str, JsonValue]:
        """Write the wire form."""
        return {"digest": self.digest, "offset": self.offset, "bytes": self.bytes}
