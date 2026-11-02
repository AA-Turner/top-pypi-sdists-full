"""Network-free resolution of explicitly captured schema resources."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, cast

from labqoat.json_document import JsonValue

if TYPE_CHECKING:
    from jsonschema_rs import JsonValue as ValidatorJsonValue


class CapturedResolver:
    """Never retrieve uncaptured URIs from the network or filesystem."""

    def __init__(self, resources: Mapping[str, dict[str, JsonValue]]) -> None:
        """Retain a private copy of the caller's captured documents."""
        self._resources = dict(resources)

    def retrieve(self, uri: str) -> ValidatorJsonValue:
        """Resolve one exact captured URI or fail closed."""
        if uri not in self._resources:
            raise ValueError(f"uncaptured schema resource: {uri}")
        return cast("ValidatorJsonValue", self._resources[uri])
