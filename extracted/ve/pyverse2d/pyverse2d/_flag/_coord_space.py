# ======================================== IMPORTS ========================================
from enum import StrEnum

# ======================================== FLAG ========================================
class CoordSpace(StrEnum):
    """Espaces de coordonnées"""
    WORLD = "world"
    FRAMEBUFFER = "framebuffer"
    WINDOW = "window"

# ======================================== EXPORTS ========================================
__all__ = [
    "CoordSpace",
]