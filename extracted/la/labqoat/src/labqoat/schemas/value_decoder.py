"""Structural decoding boundary implemented by generated finite shape descriptions."""

from typing import Protocol

from labqoat.json_document import JsonValue


class ValueDecoder(Protocol):
    """Decode only values already admitted by the owning captured schema."""

    def decode(self, value: JsonValue) -> object:
        """Restore the exact generated structural type without authored reflection."""
        ...
