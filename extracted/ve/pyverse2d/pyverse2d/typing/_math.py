# ======================================== IMPORTS ========================================
from typing import Tuple, TypeAlias, Callable
import numpy as np

# ======================================== ALIASES ========================================
EasingFunc: TypeAlias = Callable[[float], float]
Vertex: TypeAlias = Tuple[np.float32, np.float32]

# ======================================== EXPORTS ========================================
__all__ = [
    "EasingFunc",
    "Vertex",
]