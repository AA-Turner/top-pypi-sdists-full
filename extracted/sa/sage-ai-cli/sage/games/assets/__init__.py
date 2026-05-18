"""Asset generators shared across engines.

Each generator returns a typed Result with the path it wrote and the
backend used. The pipeline accumulates these into an AssetManifest that
engine adapters then consume.
"""

from .audio import AudioGenerator, AudioResult
from .manifest import AssetManifest
from .meshes import MeshGenerator, MeshResult
from .sprites import SpriteGenerator, SpriteResult


__all__ = [
    "AssetManifest",
    "AudioGenerator",
    "AudioResult",
    "MeshGenerator",
    "MeshResult",
    "SpriteGenerator",
    "SpriteResult",
]
