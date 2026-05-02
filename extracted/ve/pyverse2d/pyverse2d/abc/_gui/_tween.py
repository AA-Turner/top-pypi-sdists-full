# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import positive
from ...math.easing import EasingFunc

from abc import ABC
from typing import TYPE_CHECKING
from numbers import Real

if TYPE_CHECKING:
    from ._widget import Widget

# ======================================== CONSTANTS ========================================
_UNDEFINED = object()

# ======================================== ABC ========================================
class Tween(ABC):
    """Classe abstraite des interpolations

    Args:
        base_value: valeur initiale
        target_value: valeur finale
        duration: durée de transition
        easing: fonction d'atténuation
    """
    __slots__ = (
        "_widget", "_attribut", "_base_value", "_target_value",
        "_duration", "_easing",
        "_t", "_direction",
    )

    def __init__(self, attribut: str, target_value: object, duration: Real, easing: EasingFunc):
        self._widget: Widget = None
        self._attribut: str = attribut
        self._base_value: object = None
        self._target_value: object = target_value
        self._duration: float = float(duration)
        self._t: float = 0.0
        self._easing: EasingFunc = easing
        self._direction: int = 0

        if __debug__:
            positive(self._duration)

    # ======================================== PROPERTIES ========================================
    @property
    def widget(self) -> Widget:
        """Widget cible"""
        return self._widget

    @property
    def base_value(self) -> object:
        """Valeur initiale"""
        return self._base_value

    @property
    def target_value(self) -> object:
        """Valeur cible"""
        return self._target_value
    
    @target_value.setter
    def target_value(self, value: object) -> None:
        self._target_value = value

    @property
    def duration(self) -> float:
        """Durée de transition
        
        La durée doit être un ``Réel`` positif.
        Mettre à 0.0 pour une transition instantannée.
        """
        return self._duration
    
    @duration.setter
    def duration(self, value: float) -> None:
        value = float(value)
        assert value >= 0.0, f"duration ({value}) must be positive"
        self._duration = value

    @property
    def t(self) -> float:
        """progression temporelle"""
        return self._t
    
    @property
    def easing(self) -> EasingFunc:
        """Fonction d'atténuation
        
        La fonction doit être une ``EasingFunc`` du module math.easing
        """
        return self._easing
    
    @easing.setter
    def easing(self, value: EasingFunc) -> None:
        assert callable(value), f"easing ({value}) must be an EasingFunc"
        self._easing = value
    
    # ======================================== PREDICATES ========================================
    def is_played(self) -> bool:
        """Vérifie que l'interpolation soit en progression normale"""
        return self._direction == 1
    
    def is_reversed(self) -> bool:
        """Vérifie que l'interpolation soit en progression inverse"""
        return self._direction == -1

    # ======================================== INTERFACE ========================================
    def bind(self, widget: Widget) -> None:
        """Assigne un widget
        
        Args:
            widget: ``Widget`` à associer
        """
        base_value = getattr(widget, self._attribut, _UNDEFINED)
        if base_value is _UNDEFINED:
            return
        self._widget = widget
        self._base_value = base_value

    def play(self) -> None:
        """Active l'interpolation"""
        if self._widget is None:
            return
        if self._direction == -1:
            self._direction = 1
            return
        self._direction = 1
        self._t = 0.0

    def reverse(self) -> None:
        """Active l'interpolation dans le sens inverse"""
        if self._widget is None:
            return
        if self._direction == 1:
            self._direction = -1
            return
        self._direction = -1
        self._t = self._duration

    def interpolate(self, base: object, target: object, p: float) -> float:
        """Calcul de la valeur intermédiaire
        
        Args:
            base: valeur normale
            target: valeur finale
            p: progression
        """
        return base + (target - base) * p

    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> float:
        """Actualisation

        Args:
            dt: delta-time
        """
        if self._direction == 0:
            return
        if self._duration <= 0.0:
            value = self.target_value if self._direction == 1 else self._base_value
            self._direction = 0
        else:
            self._t = max(0.0, min(self._t + self._direction * dt, self._duration))
            p = self._easing(self._t / self._duration)
            value = self.interpolate(self._base_value, self._target_value, p)
            if self._t >= self._duration:
                self._direction = 0
        setattr(self._widget, self._attribut, value)