# ======================================== IMPORTS ========================================
from enum import Flag, auto

# ======================================== FLAG ========================================
class Activity(Flag):
    """Etat d'activité"""
    DEFAULT = 0                     # état par défaut
    ENABLED = auto()                # vient d'être activé
    DISABLED = auto()               # vient d'être désativé
    ACTIVE = auto()                 # état actif constant
    INACTIVE = auto()               # état inactif constant

# ======================================== EXPORTS ========================================
__all__ = [
    "Activity",
]