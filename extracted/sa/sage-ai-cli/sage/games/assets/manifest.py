"""Asset manifest — what got generated, where it lives on disk.

Engine adapters consume this; each engine knows where its conventions
want sprites/meshes/audio (e.g. Godot wants `res://assets/`, Unity wants
`Assets/Sprites/`, Unreal wants `Content/`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AssetManifest:
    """Maps a logical role (e.g. "player_sprite") to the file we wrote."""

    sprites: dict[str, Path] = field(default_factory=dict)
    meshes: dict[str, Path] = field(default_factory=dict)
    audio: dict[str, Path] = field(default_factory=dict)

    def total_count(self) -> int:
        return len(self.sprites) + len(self.meshes) + len(self.audio)
