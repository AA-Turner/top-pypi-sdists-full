"""Immutable produced or dataset asset identities."""

import re
from dataclasses import dataclass

from labqoat.references.resource_id import ResourceId
from labqoat.references.sha256 import Sha256


@dataclass(frozen=True, slots=True, kw_only=True)
class AssetRef:
    """An exact-byte asset with verified content and media metadata."""

    id: ResourceId
    blob_sha256: Sha256
    byte_size: int
    media_type: str

    def __post_init__(self) -> None:
        """Reject negative sizes and invalid media types."""
        if self.byte_size < 0:
            raise ValueError("Asset byte size cannot be negative")
        if re.fullmatch(r"[a-zA-Z0-9!#$&^_.+-]+/[a-zA-Z0-9!#$&^_.+-]+", self.media_type) is None:
            raise ValueError("Expected a valid media type")
