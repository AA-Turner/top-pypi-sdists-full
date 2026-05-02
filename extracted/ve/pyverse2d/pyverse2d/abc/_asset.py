# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC, abstractmethod

# ======================================== OBJET ========================================
class Asset(ABC):
    """Classe abstraite des assets"""
    __slots__ = tuple()

    @abstractmethod
    def __init__(self): ...