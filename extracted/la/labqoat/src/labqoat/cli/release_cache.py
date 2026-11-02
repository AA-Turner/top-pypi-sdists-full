"""Remember the last published release so ordinary commands start without a network round trip."""

from __future__ import annotations

import json
import os
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReleaseCache:
    """Keep one bounded, credential-free release observation beside the CLI profiles."""

    path: Path
    lifetime: float = 86_400.0

    @classmethod
    def default(cls) -> ReleaseCache:
        """Use the CLI configuration directory, honouring LABQOAT_CONFIG_DIR."""
        directory = Path(os.environ.get("LABQOAT_CONFIG_DIR", str(Path.home() / ".config" / "labqoat")))
        return cls(directory / "release-check.json")

    def read(self, now: float) -> str | None:
        """Return a release observed within the lifetime; unreadable or stale state means unknown."""
        try:
            document = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        checked = document.get("checked_at") if isinstance(document, dict) else None
        latest = document.get("latest") if isinstance(document, dict) else None
        fresh = isinstance(checked, int | float) and 0 <= now - checked < self.lifetime
        return latest if fresh and isinstance(latest, str) else None

    def write(self, latest: str, now: float) -> None:
        """Record an observation; an unwritable configuration directory never fails the command."""
        with suppress(OSError):
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps({"checked_at": now, "latest": latest}), encoding="utf-8")
