# ======================================== IMPORTS ========================================
from enum import IntEnum, auto

# ======================================== IMPORTS ========================================
class ComponentType(IntEnum):
    """Composants de rendu"""
    CIRCLE = auto()     # Cercle
    SEGMENT = auto()    # Segment
    RECT = auto()       # Rectangle

# ======================================== EXPORTS ========================================
__all__ = [
    "ComponentType",
]