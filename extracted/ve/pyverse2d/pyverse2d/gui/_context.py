# ======================================== IMPORTS ========================================
from ..math import Point
from .._rendering import Pipeline

from dataclasses import dataclass
from pyglet.graphics import Group

# ======================================== RENDER CONTEXT ========================================
@dataclass(slots=True)
class RenderContext:
    """Contexte de rendu des widgets"""
    pipeline: Pipeline      # pipeline de rendu
    x: float                # ancre horizontale
    y: float                # ancre verticale
    scale: float            # facteur de redimensionnement cumulée
    rotation: float         # rotation cumulée
    opacity: float          # opacité cumulée
    group: Group            # groupe courant
    z: int                  # z-order relatif