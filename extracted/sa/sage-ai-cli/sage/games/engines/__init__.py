"""Engine adapter registry. Map `engine name → factory` so the pipeline
can pick one by string from a parsed prompt.
"""

from __future__ import annotations

from typing import Callable

from .base import EngineAdapter
from .godot import GodotAdapter
from .unity import UnityAdapter
from .unreal import UnrealAdapter
from ._stubs import (
    BevyAdapter,
    ConstructAdapter,
    GameMakerAdapter,
    Love2DAdapter,
    PhaserAdapter,
    PygameAdapter,
    RpgMakerAdapter,
)


REGISTRY: dict[str, Callable[[], EngineAdapter]] = {
    "godot": GodotAdapter,
    "unity": UnityAdapter,
    "unreal": UnrealAdapter,
    "bevy": BevyAdapter,
    "phaser": PhaserAdapter,
    "love2d": Love2DAdapter,
    "pygame": PygameAdapter,
    "gamemaker": GameMakerAdapter,
    "construct": ConstructAdapter,
    "rpgmaker": RpgMakerAdapter,
}

DEFAULT_ENGINE = "godot"


def get_adapter(name: str | None) -> EngineAdapter:
    """Look up an adapter by name. None/unknown → default Godot."""
    key = (name or "").lower().strip()
    factory = REGISTRY.get(key) or REGISTRY[DEFAULT_ENGINE]
    return factory()


__all__ = ["EngineAdapter", "REGISTRY", "DEFAULT_ENGINE", "get_adapter"]
