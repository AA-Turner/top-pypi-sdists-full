"""Game-pipeline exceptions.

Mirrors the BuildIncomplete pattern from principal_builder: the pipeline
NEVER returns silently with a broken build. If the heal loop exhausts,
the CLI catches the typed exception and surfaces a red error.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GameBuildIncomplete(Exception):
    """Raised when the game-pipeline heal loop runs out of retries with the
    build still failing. Carries the partial report so the CLI can show
    the user what got scaffolded + which step blew up."""

    message: str
    report: dict

    def __str__(self) -> str:
        return self.message


@dataclass
class EngineNotInstalled(Exception):
    """The requested engine binary wasn't found on the system. Carries the
    install hint so the CLI can show a copy-pasteable next step."""

    engine: str
    install_hint: str

    def __str__(self) -> str:
        return f"{self.engine} is not installed. {self.install_hint}"


@dataclass
class BuildNotSupported(Exception):
    """The adapter explicitly doesn't support headless build (e.g. GameMaker,
    Construct). Scaffold + scripts succeeded; user must open the editor."""

    engine: str
    reason: str

    def __str__(self) -> str:
        return f"{self.engine}: {self.reason}"
