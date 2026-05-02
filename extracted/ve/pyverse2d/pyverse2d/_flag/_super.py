# ======================================== IMPORTS ========================================
from enum import Enum

# ======================================== FLAG ========================================
class Super(Enum):
    """Flag de retour de méthodes d'héritage"""
    NONE = 0    # Fonctionnement normal
    STOP = 1    # Requiert une fin d'éxécution

# ======================================== EXPORTS ========================================
__all__ = [
    "Super",
]