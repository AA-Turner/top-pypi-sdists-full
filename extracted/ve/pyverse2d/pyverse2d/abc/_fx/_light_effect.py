# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC
from typing import ClassVar

# ======================================== ABSTRACT CLASS ========================================
class LightEffect(ABC):
    """Classe abstraite des effets lumineux"""
    __slots__ = tuple()

    _ID: ClassVar[str] = "default"

    @classmethod
    def id(cls) -> str:
        """Renvoie l'identifiant de l'effet"""
        return cls._ID