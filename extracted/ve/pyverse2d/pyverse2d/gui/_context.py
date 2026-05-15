# ======================================== IMPORTS ========================================
from ..math import Point
from .._rendering import Pipeline

from dataclasses import dataclass
from pyglet.graphics import Group

# ======================================== RENDER CONTEXT ========================================
@dataclass(slots=True)
class RenderContext:
    """Contexte de rendu des widgets
    
    Args:
        pipeline: ``Pipeline``de rendu courant
        x: position horizontal
        y: position verticale
        scale: facteur de redimensionnement
        rotation: angle de rotation
        opacity: facteur d'opacité
        group: ``Group``courant
        z: z-order
    """
    pipeline: Pipeline      # pipeline de rendu
    x: float                # ancre horizontale
    y: float                # ancre verticale
    scale: float            # facteur de redimensionnement cumulée
    rotation: float         # rotation cumulée
    opacity: float          # opacité cumulée
    group: Group            # groupe courant
    z: int                  # z-order relatif

# ======================================== EXPORTS ========================================
__all__ = [
    "RenderContext",
]