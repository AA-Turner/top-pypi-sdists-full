# ======================================== IMPORTS ========================================
from typing import Protocol, runtime_checkable

# ======================================== PROTOCOLS ========================================
@runtime_checkable
class HasPosition(Protocol):
    """Objet positionnel
    
    L'objet doit exposé deux attributs ou propriétés ``x`` et ``y``.
    """
    @property
    def x(self) -> float: ...
    @property
    def y(self) -> float: ...

# ======================================== EXPORTS ========================================
__all__ = [
    "HasPosition",
]