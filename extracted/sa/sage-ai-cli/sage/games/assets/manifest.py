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
    """Maps a logical role (e.g. "player_sprite") to the file we wrote.

    Static + animated asset maps live side-by-side. Engine adapters pick
    whichever fits their conventions — Godot can use either, Unity wants
    sprites flattened to Assets/Sprites/, Phaser packs sprite sheets, etc.
    """

    sprites: dict[str, Path] = field(default_factory=dict)
    meshes: dict[str, Path] = field(default_factory=dict)
    audio: dict[str, Path] = field(default_factory=dict)
    # Animated sprite strips, keyed (role, state) → sheet PNG path. State
    # is "idle" / "walk" / "attack" / etc. — engine adapters look up by
    # the role first, then iterate states. Empty when generation is
    # skipped (role didn't request animation, or generator unavailable).
    sprite_animations: dict[tuple[str, str], Path] = field(default_factory=dict)
    # Mesh animation clips embedded in the GLB. We track which roles got
    # which clips (e.g. ("player", ["idle", "walk"])) so engine adapters
    # know whether to wire up an AnimationPlayer node or use the static
    # mesh directly. The actual clip data is inside the .glb file itself.
    mesh_animations: dict[str, list[str]] = field(default_factory=dict)

    def total_count(self) -> int:
        return (len(self.sprites) + len(self.meshes) + len(self.audio)
                + len(self.sprite_animations))
