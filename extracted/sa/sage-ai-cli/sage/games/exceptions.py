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


@dataclass
class ScaffoldPollution(Exception):
    """The target directory already contains a scaffold for a DIFFERENT engine.

    Real-world example: a user ran sage twice in the same dir — once with
    Godot, then with Unity. The second run wrote Unity files into the same
    directory, producing a hybrid Godot+Unity mess that neither editor
    could open. We refuse instead of silently corrupting their project.

    The CLI catches this and tells the user to clear the directory or
    pass --force to overwrite the existing scaffold."""

    requested_engine: str
    existing_engine: str
    out_dir: str

    def __str__(self) -> str:
        return (
            f"{self.out_dir} already contains a {self.existing_engine} "
            f"scaffold, but you requested {self.requested_engine}. "
            f"Refusing to mix engines — clear the directory or use a "
            f"different one. (Mixing causes both editors to break.)"
        )
