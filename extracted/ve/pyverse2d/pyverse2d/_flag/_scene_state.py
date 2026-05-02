# ======================================== IMPORTS ========================================
from enum import Enum

# ======================================== FLAG ========================================
class SceneState(Enum):
    """Gestion des autres scenes"""
    RUNNING = "running"     # update + draw
    PAUSED = "paused"       # draw only
    HIDDEN = "hidden"       # update only
    SLEEPING = "sleep"      # none

# ======================================== EXPORTS ========================================
__all__ = [
    "SceneState",
]