# ======================================== IMPORTS ========================================
from ..._managers import MouseManager
from ..._managers._inputs import Listener
from ...abc import Behavior
from ...math import Point

from pyverse2d import mouse, inputs

from typing import Callable, Any

# ======================================== BEHAVIOR ========================================
class ClickBehavior(Behavior):
    """Behavior gérant le clique
    
    Ce ``Behavior`` s'associe automatiquement au ``HoverBehavior`` si le ``Widget`` en possède un.
    """
    __slots__ = ("_down_listeners", "_up_listeners")
    _ID: str = "click"

    def __init__(self):
        # Initialisation du comportement
        super().__init__()

        # Actions
        self._down_listeners: dict[str, Listener] = {}
        self._up_listeners: dict[str, Listener] = {}

    # ======================================== INTERFACE ========================================
    def add(
        self,
        name: str = None,
        key: MouseManager.Button = mouse.B_LEFT,
        callback: Callable = None,
        args: list[Any] = None,
        kwargs: dict[str, Any] = None,
        when_up: Callable = None,
        condition: Callable = None,
        once: bool = False,
        repeat: bool = False,
        priority: int = 0,
        give_key: bool = False,
    ) -> None:
        """Ajoute une action lors du clique sur le widget

        Args:
            name: identifant associé à l'action
            key: ``MouseInput`` à détecter
            callback: ``fonction`` à appeler
            args: arguments à passer à la fonction
            kwargs: arguments nommés à passer à la fonction
            when_up: ``fonction`` à appeler lors du relâchement
            condition: ``fonction`` de confirmation lors du clique
            once: supprime le listener après éxécution
            repeat: répète l'action tant que le clique est maintenu
            priority: priorité de l'action
            give_key: passe un argument ``key`` à la fonction
        """
        if name is None:
            name = f"click_{len(self._down_listeners)}"
        elif name in self._down_listeners:
            raise ValueError(f"This bhavior already has a Listener {name}")

        down_listener: Listener = inputs.add_listener(
            key = key,
            callback = callback,
            args = args,
            kwargs = kwargs,
            condition = lambda: condition() and self._is_hovered() if condition is not None else self._is_hovered(),
            once = once,
            repeat = repeat,
            priority = priority,
            give_key = give_key,
        )
        self._down_listeners[name] = down_listener

        if when_up:
            up_listener: Listener = inputs.add_listener(
                key = key,
                up = True,
            )
            self._up_listeners[name] = up_listener

    def remove(self, name: str) -> None:
        """Supprime une action

        Args:
            name: identifiant de l'action à supprimer
        """
        if name not in self._down_listeners:
            raise ValueError(f"This behavior doesn't have a Listener {name}")
        
        inputs.remove_listener(self._down_listeners[name])
        del self._down_listeners[name]

        if name in self._up_listeners:
            inputs.remove_listener(self._up_listeners[name])
            del self._up_listeners[name]
    
    def remove_with_filters(self, key: MouseManager.Button = None, callback: Callable = None) -> None:
        """Supprime les actions correspondant aux filtres

        Args:
            key: ``MouseInput`` à filtrer
            callback: ``fonction`` à filtrer
        """
        for name, listener in self._down_listeners.items():
            if (key is not None and listener.key != key) or (callback is not None and listener.callback != callback):
                continue
            self.remove(name)

    def clear(self) -> None:
        """Supprime toutes les actions"""
        for name in list(self._down_listeners.keys()):
            self.remove(name)

    def has(self, name: str) -> bool:
        """Vérifie que le comportement possède une action
        
        Args:
            name: nom de l'action
        """
        return name in self._down_listeners
    
    def enable_all(self) -> None:
        """Active toutes les actions"""
        for listener in self._down_listeners.values():
            listener.enable()
        for listener in self._up_listeners.values():
            listener.enable()
    
    def disable_all(self) -> None:
        """Désactive toutes les actions"""
        for listener in self._down_listeners.values():
            listener.disable()
        for listener in self._up_listeners.values():
            listener.disable()

    # ======================================== HOOKS ========================================
    def _on_attach(self) -> None:
        """Hook d'attachement"""
        pass

    def _on_detach(self) -> None:
        """Hook de détachement"""
        self.clear()

    def _on_enable(self) -> None:
        """Hook d'activation"""
        self.enable_all()

    def _on_disable(self) -> None:
        """Hook de désactivation"""
        self.disable_all()

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation"""
        pass

    # ======================================== INTERNALS ========================================
    def _is_hovered(self) -> bool:
        """Vérifie si le widget est survolé"""
        if self._owner.hover is None:
            return self._collides(mouse._get_world_position())
        return self._owner.hover.is_hovered()
    
    def _collides(self, point: Point) -> bool:
        """Vérifie si un point est dans le widget"""
        return self._owner.collidespoint(point)