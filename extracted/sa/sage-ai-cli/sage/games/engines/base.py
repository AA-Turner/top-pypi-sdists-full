"""Engine adapter Protocol + shared types.

Every engine in `sage/games/engines/` exposes the same surface so the
pipeline doesn't need per-engine conditionals. Protocol (not base class)
because engine runtimes vary widely — Godot/Unity/Unreal are subprocess
shells, Bevy/Phaser piggyback on cargo/npm, GameMaker/Construct are
GUI-only with no headless build.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntFlag
from pathlib import Path
from typing import Callable, Optional, Protocol


ProgressFn = Callable[[str], None]
GenerateFn = Callable[[str], str]


class EngineCapability(IntFlag):
    """What a given engine adapter can do. Pipeline uses these to decide
    whether to attempt headless build vs surface a "open in editor" message."""

    NONE = 0
    SCAFFOLD = 1
    SCRIPTS = 2
    ASSETS = 4
    BUILD = 8

    @classmethod
    def full(cls) -> "EngineCapability":
        return cls.SCAFFOLD | cls.SCRIPTS | cls.ASSETS | cls.BUILD


@dataclass
class GameRequest:
    """Parsed prompt → structured game spec the pipeline consumes."""

    task_type: str = "game"
    engine: Optional[str] = None        # e.g. "godot", "unity", or None for default
    genre: Optional[str] = None         # platformer, rpg, fps, ...
    perspective: Optional[str] = None   # 2d, 3d, isometric, first-person
    art_style: Optional[str] = None     # pixel, cartoon, realistic, ...
    target: str = "web"                  # build target — web|win|mac|linux|android
    raw_prompt: str = ""

    def is_3d(self) -> bool:
        return self.perspective in {"3d", "first-person", "third-person", "isometric"}


@dataclass
class GamePlan:
    """The pipeline's working state. Built from GameRequest + decomposed brief."""

    request: GameRequest
    title: str
    description: str
    features: list[str] = field(default_factory=list)
    # (role, prompt) — single-frame static sprite
    sprite_roles: list[tuple[str, str]] = field(default_factory=list)
    # (role, prompt, [states]) — animated sprite. States default to
    # ("idle", "walk") if the caller wants animation without naming
    # specific states. Passing [] explicitly disables animation for the
    # role (the pipeline emits only the static sprite).
    animated_sprite_roles: list[tuple[str, str, list[str]]] = field(default_factory=list)
    mesh_roles: list[tuple[str, str]] = field(default_factory=list)
    audio_roles: list[tuple[str, str, str]] = field(default_factory=list)  # (role, prompt, kind)
    target: str = "web"


@dataclass
class BuildArtifact:
    """What `adapter.build()` returns on success."""

    output_path: Path
    target: str
    size_bytes: int
    duration_s: float


class EngineAdapter(Protocol):
    """Structural Protocol every engine module satisfies.

    Implementations live in sage/games/engines/<name>.py. The pipeline
    picks one by `name` from `GameRequest.engine` (or its default).
    """

    name: str
    capabilities: EngineCapability

    def detect(self) -> Optional[Path]: ...
    def install_hint(self) -> str: ...
    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None: ...
    def emit_scripts(
        self,
        plan: GamePlan,
        out_dir: Path,
        *,
        generate: GenerateFn,
        log: ProgressFn,
    ) -> list[Path]: ...
    def consume_assets(
        self,
        manifest: "AssetManifest",  # noqa: F821 — forward ref to assets.manifest
        out_dir: Path,
        *,
        log: ProgressFn,
    ) -> None: ...
    def build(
        self,
        out_dir: Path,
        *,
        target: str,
        log: ProgressFn,
    ) -> BuildArtifact: ...
