"""Person re-identification support for ``people_counting_extended``.

Temporary bridge (see ``plan.md``): the embedding model lives inside the
use case layer until re-identification is integrated at the tracker level.
Nothing here is imported by any other use case, so removing this package
plus ``people_counting_extended.py`` removes the feature entirely.

Imports are lazy -- importing this package must not pull in torch.
"""

from __future__ import annotations

__all__ = ["GalleryMatch", "PersonEmbedder", "ReIDGallery", "get_shared_embedder"]


def __getattr__(name: str):  # PEP 562 lazy re-export
    if name in ("ReIDGallery", "GalleryMatch"):
        from .gallery import GalleryMatch, ReIDGallery

        return {"ReIDGallery": ReIDGallery, "GalleryMatch": GalleryMatch}[name]
    if name in ("PersonEmbedder", "get_shared_embedder"):
        from .model import PersonEmbedder, get_shared_embedder

        return {"PersonEmbedder": PersonEmbedder, "get_shared_embedder": get_shared_embedder}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
