"""What moving a volume's files needs from the platform, whoever is asking."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

from labqoat.json_document import JsonValue
from labqoat.volumes.volume_entry import VolumeEntry


class VolumeApi(Protocol):
    """One volume's entries, signed block transfers and commits, under a worker's or a person's credentials."""

    def entries(self, path: str = "", recursive: bool = True) -> tuple[int, list[VolumeEntry]]:
        """The volume's version and its entries at or under ``path``."""

    def uploads(self, blocks: Sequence[Mapping[str, JsonValue]]) -> list[Mapping[str, JsonValue]]:
        """Signed uploads for the given blocks (digest and size) that storage does not hold."""

    def downloads(self, digests: Sequence[str]) -> dict[str, str]:
        """Signed GET URLs for the given blocks."""

    def commit(self, document: Mapping[str, JsonValue]) -> int:
        """Merge changed and removed paths and return the version made."""
