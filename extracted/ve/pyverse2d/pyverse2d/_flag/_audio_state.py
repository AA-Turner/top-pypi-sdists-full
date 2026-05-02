# ======================================== IMPORTS ========================================
from enum import Enum

# ======================================== FLAG ========================================
class AudioState(Enum):
    """Etat audio"""
    PLAYING = "playing"     # en cours de lecture
    PAUSED = "paused"       # en pause
    SLEEPING = "sleeping"   # en sommeil

# ======================================== EXPORTS ========================================
__all__ = [
    "AudioState",
]