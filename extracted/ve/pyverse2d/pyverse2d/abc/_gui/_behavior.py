# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ._tween import Tween

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from ...scene import GuiLayer
    from ._widget import Widget

# ======================================== BEHAVIOR ========================================
class Behavior(ABC):
    """Class abstraite des comportements UI"""
    __slots__ = ("_owner", "_enabled", "_tweens")
    _ID: str = "default"
    _PRIORITY: int = 0

    def __init__(self):
        self._owner: Widget = None
        self._enabled: bool = True
        self._tweens: dict[Type[Tween], Tween] = {}

    # ======================================== PROPERTIES ========================================
    @property
    def layer(self) -> GuiLayer | None:
        """Layer du composant possesseur"""
        return self._owner.layer if self._owner is not None else None

    @property
    def owner(self) -> Widget:
        """Composant possesseur"""
        return self._owner
    
    # ======================================== PREDICATES ========================================
    def is_enabled(self) -> bool:
        """Vérifie l'activité"""
        return self._enabled

    # ======================================== STATE ========================================
    def attach(self, widget: Widget, _from_widget: bool = False) -> None:
        """Assigne un ``Widget`` possesseur

        Args:
            widget: composant UI maître
        """
        if not _from_widget:
            return widget.add_behavior(self)
        if self._owner is not None:
            raise ValueError("This behavior is already attached")
        if __debug__:
            expect(widget, Widget)
        self._owner = widget
        for tween in self._tweens.values():
            if tween.widget is None:
                tween.bind(widget)
        self._on_attach()

    def detach(self, _from_widget: bool = False) -> None:
        """Supprime l'assignation au ``Widget`` possesseur"""
        if not _from_widget:
            return self._owner.remove_behavior(self)
        self._on_detach()
        self._owner = None

    def enable(self) -> None:
        """Active le ``Behavior``"""
        if self._enabled:
            return
        self._enabled = True
        self._on_enable()

    def disable(self) -> None:
        """Désactive le ``Behavior``"""
        if not self._enabled:
            return
        self._enabled = False
        self._on_disable()

    # ======================================== TWEENS ========================================
    def add_tween(self, tween: Tween, target: Widget = None) -> None:
        """Ajoute une interpolation au behavior

        Args:
            tween: interpolation à associer
            target: widget cible (par défaut le possesseur)
        """
        widget = target or self._owner
        if __debug__:
            expect(widget, Widget)
        if widget is not None:
            tween.bind(widget)
        self._tweens[type(tween)] = tween

    def remove_tween(self, tween_type: Type[Tween]) -> None:
        """Retire une interpolation par type

        Args:
            tween_type: type de l'interpolation à retirer
        """
        if tween_type not in self._tweens:
            raise ValueError(f"This behavior has no tween of type {tween_type.__name__}")
        tween = self._tweens[tween_type]
        tween.unbind()
        del tween

    def get_tween(self, tween_type: Type[Tween]) -> Tween | None:
        """Renvoie une interpolation par type, ou ``None`` si absente

        Args:
            tween_type: type de l'interpolation à récupérer
        """
        return self._tweens.get(tween_type)

    def clear_tweens(self) -> None:
        """Retire toutes les interpolations"""
        self._tweens.clear()

    def _play_tweens(self) -> None:
        """Active les interpolations"""
        for tween in self._tweens.values():
            if self._owner._lock_attr(tween._attribut, self._PRIORITY):
                tween.play()

    def _reverse_tweens(self) -> None:
        """Active les interpolations dans le sens inverse"""
        for tween in self._tweens.values():
            self._owner._unlock_attr(tween._attribut, self._PRIORITY)
            tween.reverse()

    # ======================================== HOOKS ========================================
    @abstractmethod
    def _on_attach(self) -> None: ...

    @abstractmethod
    def _on_detach(self) -> None: ...

    @abstractmethod
    def _on_enable(self) -> None: ...

    @abstractmethod
    def _on_disable(self) -> None: ...

    # ======================================== LIFE CYCLE ========================================
    @abstractmethod
    def _update(self, dt: float) -> None: ...

    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        self._update(dt)
        for tween in self._tweens.values():
            tween.update(dt)

    def delete(self) -> None:
        """Suppression du comportement"""
        self.clear_tweens()
        self.detach()