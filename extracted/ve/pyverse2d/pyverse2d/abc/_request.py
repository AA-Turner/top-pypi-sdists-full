# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC

# ======================================== ABSTRACT CLASS ========================================
class Request(ABC):
    """Classe abstraites des requête contenant un jeu d'informations ponctuel"""
    __slots__ = tuple()

# ======================================== EXPORTS ========================================
__all__ = [
    "Request",
]