"""What a mount was last in step with, shared by every process of the workload."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.volumes.volume_entry import VolumeEntry


@dataclass
class MountState:
    """The base a mount's changes are measured from: entries as committed or fetched, and files seen unchanged.

    It starts as the state the host laid out, whose files carry their recorded whole-second times, and is kept
    in a file so every process of the workload measures from the same base.
    """

    version: int
    entries: dict[str, VolumeEntry]
    observed: dict[str, tuple[int, int]]

    @classmethod
    def load(cls, path: Path, record: Mapping[str, JsonValue]) -> MountState:
        """Read the saved state, or the host's record of what it laid out."""
        if path.is_file():
            return cls.decode(JsonDocument.expect_dict(json.loads(path.read_text())))
        return cls.laid_out(record)

    @classmethod
    def laid_out(cls, record: Mapping[str, JsonValue]) -> MountState:
        """The state the host laid out: every file as recorded, at its recorded time."""
        entries = [
            VolumeEntry.from_dict(JsonDocument.expect_dict(item))
            for item in JsonDocument.expect_list(record["entries"])
        ]
        observed = {entry.path: (entry.size, entry.mtime * 1_000_000_000) for entry in entries if entry.kind == "file"}
        return cls(
            JsonDocument.expect_scalar(record["version"], int), {entry.path: entry for entry in entries}, observed
        )

    @classmethod
    def decode(cls, document: JsonDocument) -> MountState:
        """Read a saved state."""
        entries = [
            VolumeEntry.from_dict(JsonDocument.expect_dict(item))
            for item in JsonDocument.expect_list(document["entries"])
        ]
        observed = JsonDocument.expect_dict(document["observed"])
        return cls(
            JsonDocument.expect_scalar(document["version"], int),
            {entry.path: entry for entry in entries},
            {path: cls._signature(value) for path, value in observed.items()},
        )

    def save(self, path: Path) -> None:
        """Write the state atomically beside its final name."""
        entries: list[JsonValue] = [entry.to_dict() for entry in self.entries.values()]
        observed: dict[str, JsonValue] = {name: [size, mtime] for name, (size, mtime) in self.observed.items()}
        staged = path.with_name(f".{path.name}.{os.getpid()}")
        staged.write_text(json.dumps({"version": self.version, "entries": entries, "observed": observed}))
        staged.replace(path)

    @staticmethod
    def _signature(value: JsonValue) -> tuple[int, int]:
        """A saved size and modification time."""
        size, mtime = JsonDocument.expect_list(value)
        return JsonDocument.expect_scalar(size, int), JsonDocument.expect_scalar(mtime, int)
