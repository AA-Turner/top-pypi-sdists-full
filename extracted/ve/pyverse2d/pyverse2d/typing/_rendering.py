# ======================================== IMPORTS ========================================
from typing import TypeAlias, Literal

# ======================================== ALIASES ========================================
BorderAlign: TypeAlias = Literal["in", "center", "out"]
VideoScale: TypeAlias = Literal["letterboxing", "fitting", "resize"]

# ======================================== EXPORTS ========================================
__all__ = [
    "BorderAlign",
]