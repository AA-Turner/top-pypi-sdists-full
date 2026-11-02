"""Explicit source-independent build commands retain their layers across workspace edits."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyCommandStep:
    """Materialize immutable dependencies before copying authored source into the image."""

    commands: tuple[str, ...]
