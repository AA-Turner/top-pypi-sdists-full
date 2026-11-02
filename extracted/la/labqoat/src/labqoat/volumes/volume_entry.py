"""One path in a volume as storage and every reader agree on it."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.volumes.volume_pack import VolumePack


@dataclass(frozen=True)
class VolumeEntry:
    """A directory, a symbolic link, or a file whose content is its blocks' contents in order.

    ``mtime`` is in whole seconds. Two entries hold the same thing when kind, mode and content (or link target)
    agree; the modification time alone never makes a change worth committing. A small file may be stored in a
    ``pack`` shared with others; its blocks still name its own content.
    """

    path: str
    kind: str
    mode: int = 0o755
    mtime: int = 0
    size: int = 0
    blocks: tuple[str, ...] = ()
    target: str = ""
    pack: VolumePack | None = None

    @classmethod
    def from_dict(cls, document: Mapping[str, JsonValue]) -> VolumeEntry:
        """Read the wire form, where each kind carries only its own fields."""
        kind = JsonDocument.expect_scalar(document["kind"], str)
        path = JsonDocument.expect_scalar(document["path"], str)
        if kind == "symlink":
            return cls(path, kind, target=JsonDocument.expect_scalar(document["target"], str))
        mode = JsonDocument.expect_scalar(document["mode"], int)
        if kind == "directory":
            return cls(path, kind, mode)
        blocks = tuple(JsonDocument.expect_scalar(block, str) for block in JsonDocument.expect_list(document["blocks"]))
        mtime = JsonDocument.expect_scalar(document["mtime"], int)
        size = JsonDocument.expect_scalar(document["size"], int)
        stored = document.get("pack")
        pack = VolumePack.from_dict(JsonDocument.expect_dict(stored)) if stored is not None else None
        return cls(path, kind, mode, mtime, size, blocks, pack=pack)

    def to_dict(self) -> dict[str, JsonValue]:
        """Write the wire form a commit sends."""
        if self.kind == "symlink":
            return {"path": self.path, "kind": self.kind, "target": self.target}
        if self.kind == "directory":
            return {"path": self.path, "kind": self.kind, "mode": self.mode}
        blocks: list[JsonValue] = list(self.blocks)
        written: dict[str, JsonValue] = {
            "path": self.path,
            "kind": self.kind,
            "mode": self.mode,
            "mtime": self.mtime,
            "size": self.size,
            "blocks": blocks,
        }
        if self.pack is not None:
            written["pack"] = self.pack.to_dict()
        return written

    def packed(self, pack: VolumePack | None) -> VolumeEntry:
        """This entry stored in ``pack``, or as it is without one."""
        return replace(self, pack=pack) if pack is not None else self

    def same(self, other: VolumeEntry | None) -> bool:
        """Whether ``other`` holds the same thing at this path."""
        return (
            other is not None
            and other.kind == self.kind
            and other.target == self.target
            and other.blocks == self.blocks
            and (self.kind == "symlink" or other.mode == self.mode)
        )
