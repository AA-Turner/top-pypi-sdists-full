# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC
from typing import ClassVar

# ======================================== ABSTRACT CLASS ========================================
class PostFxEffect(ABC):
    """Classe abstraite des effets post-processing"""
    __slots__ = tuple()

    _ID: ClassVar[str]

    @classmethod
    def id(cls) -> str:
        """Renvoie l'identifiant de l'effet"""
        return cls._ID

# ======================================== EXPORTS ========================================
__all__ = [
    "PostFxEffect",
]