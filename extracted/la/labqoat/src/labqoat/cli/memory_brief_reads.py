"""Brief versions each agent has read, so an edit can prove it builds on the latest version."""

from __future__ import annotations

import json
import os
from pathlib import Path

import click

from labqoat.json_document import JsonDocument


class MemoryBriefReads:
    """Remember the brief version last read per endpoint, environment, project and agent."""

    filename = "memory-brief-reads.json"
    maximum_entries = 256

    def __init__(self, config_dir: Path | None = None) -> None:
        """Use the CLI configuration directory, honouring LABQOAT_CONFIG_DIR."""
        default = Path(os.environ.get("LABQOAT_CONFIG_DIR", str(Path.home() / ".config" / "labqoat")))
        self._path = (config_dir or default) / self.filename

    @staticmethod
    def key(base_url: str, environment: str | None, project: str, agent: str | None) -> str:
        """Scope a read to everything that identifies the brief and its reader."""
        return "|".join((base_url, environment or "default", project, agent or ""))

    def record(self, key: str, brief: object) -> None:
        """Store the version of a brief document; an absent brief is version zero."""
        version = 0 if brief is None else JsonDocument.expect_dict(brief)["version"]
        entries = {name: value for name, value in self._entries().items() if name != key}
        entries[key] = version
        kept = dict(list(entries.items())[-self.maximum_entries :])
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(kept, sort_keys=False), encoding="utf-8")
        except OSError as error:
            click.echo(
                f"warning: this brief read could not be remembered in {self._path} ({error.strerror}). Set "
                "LABQOAT_CONFIG_DIR to a writable directory, or state the version you read when editing the brief.",
                err=True,
            )

    def version(self, key: str) -> int | None:
        """Return the last read version, or None when this agent has not read the brief."""
        value = self._entries().get(key)
        return value if isinstance(value, int) else None

    def _entries(self) -> dict[str, object]:
        """Read stored entries, treating a missing or damaged file as empty."""
        try:
            loaded = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        return loaded if isinstance(loaded, dict) else {}
