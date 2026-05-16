# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped

from ._component import Component

from numbers import Real, Integral

# ======================================== ABSTRACT CLASS ========================================
class RendererComponent(Component):
    """Classe abstraite des composants de rendu"""
    __slots__ = ("_opacity", "_z", "_visible")

    def __init__(
            self,
            opacity: Real = 1.0,
            z: Integral = 0,
            visible: bool = True,     
        ):
        # Transtypage et vérifications
        opacity = float(opacity)
        z = int(z)
        visible = bool(visible)   

        if __debug__:
            clamped(opacity)
    
        # Attributs publiques
        self._opacity: float = opacity
        self._z: int = z
        self._visible: bool = visible

    # ======================================== PROPERTIES ========================================
    @property
    def opacity(self) -> float:
        """Facteur d'opacité"""
        return self._opacity
    
    @opacity.setter
    def opacity(self, value: Real):
        value = float(value)
        if __debug__:
            clamped(value)
        self._opacity = value

    @property
    def z(self) -> int:
        """Ordre de rendu"""
        return self._z
    
    @z.setter
    def z(self, value: Integral):
        value = int(value)
        self._z = value

    @property
    def visible(self) -> bool:
        """Visibilité"""
        return self._visible
    
    @visible.setter
    def visible(self, value: bool) -> None:
        value = bool(value)
        self._visible = value

    # ======================================== PREDICATES ========================================
    def is_visible(self) -> bool:
        """Vérifie la visibilité"""
        return self._visible

    # ======================================== INTERFACE ========================================
    def show(self):
        """Rend visible"""
        self._visible = True

    def hide(self):
        """Rend invisible"""
        self._visible = False