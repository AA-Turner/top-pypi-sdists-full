"""Ordered shell commands executed only by the service-owned image builder."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandStep:
    """Keep command boundaries so every failure stops the corresponding build layer."""

    commands: tuple[str, ...]
