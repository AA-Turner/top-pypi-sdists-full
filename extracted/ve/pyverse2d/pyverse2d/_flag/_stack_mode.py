# ======================================== IMPORTS ========================================
from enum import Enum

# ======================================== FLAG ========================================
class StackMode(Enum):
    """Gestion des autres scenes"""
    OVERLAY = "overlay"     # scene du dessous continue tout
    PAUSE = "pause"         # scene du dessous stop draw mais continue update
    HIDE = "hide"           # scene du dessous stop update mais continue draw
    STOP = "stop"           # scene du dessous stop tout

# ======================================== EXPORTS ========================================
__all__ = [
    "StackMode",
]