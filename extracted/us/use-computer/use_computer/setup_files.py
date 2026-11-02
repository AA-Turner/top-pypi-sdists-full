"""Setup file manifest helpers."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SetupFile:
    local_name: str
    remote_path: str = ""
    vm_path: str = ""

    @classmethod
    def from_manifest(cls, entry: Mapping[str, Any]) -> SetupFile | None:
        local_name = str(entry.get("local_name") or "")
        if not local_name:
            return None
        return cls(
            local_name=local_name,
            remote_path=str(entry.get("remote_path") or ""),
            vm_path=str(entry.get("vm_path") or ""),
        )

    @property
    def target_path(self) -> str:
        return self.vm_path or self.remote_path

    def local_path(self, setup_dir: Path) -> Path:
        return setup_dir / "files" / self.local_name

    def to_manifest(self) -> dict[str, str]:
        entry = {"local_name": self.local_name}
        if self.remote_path:
            entry["remote_path"] = self.remote_path
        if self.vm_path:
            entry["vm_path"] = self.vm_path
        return entry


def read_setup_files(setup_dir: Path) -> list[SetupFile]:
    manifest_path = setup_dir / "files" / "manifest.json"
    if not manifest_path.exists():
        return []
    raw_entries = json.loads(manifest_path.read_text())
    return [
        setup_file
        for entry in raw_entries
        if isinstance(entry, Mapping)
        if (setup_file := SetupFile.from_manifest(entry))
    ]
