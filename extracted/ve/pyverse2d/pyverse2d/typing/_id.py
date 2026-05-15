# ======================================== IMPORTS ========================================
from typing import TypeAlias

# ======================================== ALIASES ========================================
Button: TypeAlias = int
Key: TypeAlias = int
Input: TypeAlias = int

SystemCursor: TypeAlias = str | None

# ======================================== EXPORTS ========================================
__all__ = [
    "Button",
    "Key",
    "Input",

    "SystemCursor"
]