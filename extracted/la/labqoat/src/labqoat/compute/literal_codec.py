"""Closed string alternatives for authored row fields such as dataset splits."""

from dataclasses import dataclass
from typing import get_args

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class LiteralCodec:
    """Transport a declared string enum without losing its closed set of choices."""

    annotation: object

    def schema(self) -> dict[str, JsonValue]:
        """Require nonempty string alternatives with portable JSON identity."""
        choices = get_args(self.annotation)
        if not choices or any(type(choice) is not str for choice in choices):
            raise TypeError("Compute Literal fields must declare string choices")
        return {"type": "string", "enum": list(choices)}

    def convert(self, value: object) -> JsonValue:
        """Require a string; the enclosing value validates membership once."""
        if type(value) is not str:
            raise TypeError("Expected a declared string choice")
        return value
