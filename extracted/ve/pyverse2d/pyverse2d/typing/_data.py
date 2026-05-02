# ======================================== IMPORTS ========================================
from typing import TypeAlias, KeysView, ValuesView, TypeVar

# ======================================== CONSTANTS ========================================
K = TypeVar("K")
V = TypeVar("V")

# ======================================== ALIASES ========================================
DictKeys: TypeAlias = KeysView[K]
DictValues: TypeAlias = ValuesView[V]

# ======================================== EXPORTS ========================================
__all__ = [
    "DictKeys",
    "DictValues",
]