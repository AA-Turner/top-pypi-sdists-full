# ======================================== IMPORTS ========================================
from dataclasses import dataclass

# ======================================== ABSOLUTE CONSTANTS ========================================
_BAUMGARTE: float = 0.2         # facteur de correction de position par frame
_MAX_MASS_RATIO: float = 0.95   # ratio masse max pour éviter la correction asymétrique
_WARM_BIAS: float = 0.7         # fraction des impulsions précédentes réappliquées

# ======================================== DATA SET ========================================
@dataclass(slots=True, frozen=True)
class ConstantsDataset:
    SLOP: float
    MAX_CORRECTION: float
    ITER: float
    EXTRA_ITER_THRESHOLD: float
    EXTRA_ITER: float
    RESTITUTION_THRESHOLD: float
    RESTITUTION_MAX_VEL: float
    VEL_ALONG_WAKE_TRESHOLD: float
    BAUMGARTE: float = _BAUMGARTE
    MAX_MASS_RATIO: float = _MAX_MASS_RATIO
    WARM_BIAS: float = _WARM_BIAS

# ======================================== EXPORTS ========================================
__all__ = [
    "ConstantsDataset",
]