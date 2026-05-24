# ======================================== IMPORTS ========================================
from __future__ import annotations

import os
import pyglet
from pyglet.gl import (
    glBindTexture, glTexParameteri,
    GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
    GL_CLAMP_TO_EDGE, GL_REPEAT,
)
from typing import ClassVar

# ======================================== IMAGE LOADER ========================================
class ImageLoader:
    """Chargeur d'images pyglet partagé"""

    _cache: ClassVar[dict[str, pyglet.image.Texture]] = {}

    @classmethod
    def load(cls, path: str, tiling: bool = False) -> pyglet.image.Texture | None:
        """Charge (ou retourne depuis le cache) une texture GL

        Args:
            path: chemin du fichier image
            tiling: si True, wrap mode GL_REPEAT, sinon GL_CLAMP_TO_EDGE

        Returns:
            texture pyglet, ou None si le chargement échoue
        """
        cache_key = f"{path}|{'repeat' if tiling else 'clamp'}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        # Ajout du dossier au resource path pyglet
        directory = os.path.dirname(os.path.abspath(path))
        if directory not in pyglet.resource.path:
            pyglet.resource.path.append(directory)
            pyglet.resource.reindex()

        try:
            raw = pyglet.resource.image(os.path.basename(path), atlas=False)
            texture = raw.get_texture()
            wrap_mode = GL_REPEAT if tiling else GL_CLAMP_TO_EDGE
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_mode)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_mode)
            glBindTexture(GL_TEXTURE_2D, 0)
            cls._cache[cache_key] = texture
            return texture
        
        except pyglet.resource.ResourceNotFoundException:
            print(f"[ImageLoader] Cannot load image: {path}")
            return None

    @classmethod
    def get_id(cls, path: str, tiling: bool = False) -> int:
        """Retourne directement le texture ID GL

        Args:
            path: chemin du fichier image
            tiling: wrap mode

        Returns:
            texture ID GL, ou 0 si le chargement échoue
        """
        texture = cls.load(path, tiling)
        return texture.id if texture is not None else 0

    @classmethod
    def clear_cache(cls) -> None:
        """Vide le cache des textures"""
        cls._cache.clear()

# ======================================== EXPORTS ========================================
__all__ = [
    "ImageLoader",
]