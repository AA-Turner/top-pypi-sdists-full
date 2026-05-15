# ======================================== IMPORTS ========================================
from typing import TypeAlias, Literal

# ======================================== ALIASES ========================================
BorderAlign: TypeAlias = Literal["in", "center", "out"]
HorizontalAlign: TypeAlias = Literal["left", "center", "right"]

VideoScale: TypeAlias = Literal["letterboxing", "fitting", "resize"]

# ======================================== EXPORTS ========================================
__all__ = [
    "BorderAlign",
    "HorizontalAlign",

    "VideoScale",
]