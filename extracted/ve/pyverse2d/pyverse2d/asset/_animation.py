# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, not_null, positive
from ..abc import Asset

from ._image import Image

from numbers import Real
from pathlib import Path
from typing import Iterable, Iterator

# ======================================== ASSET ========================================
class Animation(Asset):
    """
    Descripteur d'animation

    Args:
        frames(Iterable[Image]): succession des images de l'animation
        framerate(float, optional): taux d'images par seconde
    """
    __slots__ = ("_frames", "_framerate")

    def __init__(self, frames: Iterable[Image], framerate: Real = 24.0):
        if not frames:
            raise ValueError("Animation must have at least one frame")
        self._frames: tuple[Image] = expect(tuple(frames), tuple[Image])
        self._framerate: float = float(positive(not_null(expect(framerate, Real))))

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'animation"""
        return f"Animation(frames={len(self._frames)}, framerate={self._framerate})"
    
    def __iter__(self) -> Iterator[Image]:
        """Renvoie les frames dans un itérateur"""
        return iter(self._frames)
    
    def __hash__(self):
        """Renvoie l'entier hash de l'animation"""
        return hash((self._frames, self._framerate))

    # ======================================== GETTERS ========================================
    def __getitem__(self, key: int | slice) -> Image | list[Image]:
        """Renvoie l'image d'index correspondant"""
        return self._frames[key]

    @property
    def frames(self) -> tuple[Image]:
        """Envoie l'ensemble des frames"""
        return self._frames

    @property
    def framerate(self) -> float:
        """Renvoie le taux d'images par seconde"""
        return self._framerate

    @property
    def duration(self) -> float:
        """Renvoie la durée de l'animation en secondes"""
        return len(self._frames) / self._framerate

    # ======================================== FACTORY ========================================
    @classmethod
    def from_folder(
            cls,
            path: str,
            prefix: str = "",
            extensions: Iterable[str] = None,
            width: Real = None,
            height: Real = None,
            scale_factor: Real = 1.0,
            framerate: Real = 24.0,
        ) -> Animation:
        """
        Charge un ensemble de frames depuis un dossier

        Args:
            path(str): chemin du dossier
            prefix(str, optional): préfixe des fichiers à charger
            extensions(Iterable[str], optional): extensions des fichiers à charger
            width(Real, optional): largeur cible en pixels
            height(Real, optional): hauteur cible en pixels
            scale_factor(Real, optional): facteur de redimensionnement
            framerate(float, optional): taux d'images par seconde
        """
        extensions = set(extensions or [".png", ".jpg", ".jpeg"])

        # Récupération du dossier
        folder = Path(expect(path, str))
        if not folder.is_dir():
            raise ValueError(f"Path is not a directory: {path}")

        # Chargement des fichiers
        files = sorted((f for f in folder.iterdir() if f.suffix in extensions and f.name.startswith(prefix)), key=lambda f: f.name)
        if not files:
            raise ValueError(f"No matching files found in: {path}")

        # Génération de l'animation
        frames = [Image(str(f), width=width, height=height, scale_factor=scale_factor) for f in files]
        return cls(frames, framerate)