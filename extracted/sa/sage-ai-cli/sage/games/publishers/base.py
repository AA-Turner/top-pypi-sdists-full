"""Publisher Protocol + shared types.

Mirror the EngineAdapter shape: each publisher exposes the same surface
(detect, install_hint, scaffold) so the CLI can pick one by name without
per-publisher conditionals.

A publisher's `scaffold()` writes the deploy script + CI workflow + README
into `out_dir/deploy/<publisher>/`. Once written, the user runs the deploy
script themselves (with their own API keys); sage never uploads anything.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Protocol


ProgressFn = Callable[[str], None]


@dataclass
class PublisherSpec:
    """User-facing config for one publisher integration.

    Fields are kept minimal — anything publisher-specific (Steam app ID,
    itch.io username/game-slug, Play Console package name) is rendered
    into the deploy script as placeholders the user fills in by hand
    before their first deploy."""

    publisher: str             # "itch.io" / "steam" / "github-pages" / ...
    artifact_kind: str          # "web" | "windows" | "mac" | "linux" | "android" | "ios"
    artifact_path: str          # e.g. "build/index.html" or "build/game.exe"

    # Publisher-specific identifiers — None means "user fills in later".
    project_id: Optional[str] = None
    extra_env: dict[str, str] = field(default_factory=dict)


class PublisherAdapter(Protocol):
    """Every publisher implements this. The pipeline picks one by name."""

    name: str

    def detect(self) -> Optional[Path]:
        """Return path to the publisher's CLI binary, or None if missing.
        Detection isn't required to scaffold — only to deploy locally."""
        ...

    def install_hint(self) -> str:
        """How to install the publisher's CLI. Shown when detect() returns None."""
        ...

    def scaffold(
        self, spec: PublisherSpec, out_dir: Path, *, log: ProgressFn,
    ) -> list[Path]:
        """Write deploy script + CI workflow + README into out_dir/deploy/<name>/.
        Returns the list of paths written (for sage's progress report)."""
        ...
