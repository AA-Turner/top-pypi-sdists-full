# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..abc import Manager

from ._context import ContextManager

from typing import Any, Callable, TypeAlias, Type, ClassVar

# ======================================== LISTENER ========================================
class Listener:
    """Représente un listener d'entrée utilisateur"""
    __slots__ = (
        "callback",
        "args", "kwargs",
        "up",
        "condition",
        "once",
        "repeat",
        "priority",
        "give_key",
        "exclude",
        "any_of",
        "keys",
        "_enabled",
        "_active",
        "_remove_fn",
    )

    def __init__(
            self,
            callback: Callable,
            args: list,
            kwargs: dict,
            priority: int,
            remove_fn: Callable,
            *,
            up: bool = False,
            condition: Callable = None,
            once: bool = False,
            repeat: bool = False,
            give_key: bool = False,
            exclude: set = None,
            any_of: set = None,
            keys: set = None,
        ):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.priority = priority
        self.up = up
        self.condition = condition
        self.once = once
        self.repeat = repeat
        self.give_key = give_key
        self.exclude = exclude or set()
        self.any_of = any_of or set()
        self.keys = keys or set()
        self._enabled = True
        self._active = True
        self._remove_fn = remove_fn

    # ======================================== PREDICATES ========================================
    def is_enabled(self) -> bool:
        """Renvoie True si le listener est activé"""
        return self._enabled

    def is_active(self) -> bool:
        """Renvoie True si le listener est encore actif"""
        return self._active

    # ======================================== STATE ========================================
    def enable(self) -> None:
        """Active le listener"""
        self._enabled = True

    def disable(self) -> None:
        """Désactive le listener"""
        self._enabled = False

    def invalidate(self) -> None:
        """Désactive et désinscrit ce listener"""
        if self._active:
            self._active = False
            self._remove_fn(self)

    # ======================================== HELPERS ========================================
    def _fire(self, event_id: int = None) -> None:
        """Appelle le callback avec les arguments enregistrés"""
        kw = dict(self.kwargs)
        if self.give_key and event_id is not None:
            kw["key"] = event_id
        self.callback(*self.args, **kw)
        if self.once:
            self.invalidate()

# ======================================== GESTIONNAIRE ========================================
class InputsManager(Manager):
    """Gestionnaire des entrées utilisateur"""
    __slots__ = (
        "_listeners", "_any_listeners", "_any_of_listeners", "_all_of_listeners",
        "_triggered_combos",
    )

    _ID: str = "inputs"

    Input: TypeAlias = int
    Listener: ClassVar[Type[Listener]] = Listener

    def __init__(self, context_manager: ContextManager):
        # Initialisation du gestionnaire
        super().__init__(context_manager)

        # Listeners
        self._listeners: dict[int, list[Listener]] = {}
        self._any_listeners: list[Listener] = []
        self._any_of_listeners: list[Listener] = []
        self._all_of_listeners: list[Listener] = []
        self._triggered_combos: set = set()

        # Abonnements
        self._ctx.event.on_key_press.subscribe(self._on_press)
        self._ctx.event.on_key_release.subscribe(self._on_release)
        self._ctx.event.on_mouse_press.subscribe(self._on_mouse_press)
        self._ctx.event.on_mouse_release.subscribe(self._on_mouse_release)

    # ======================================== LISTENERS ========================================
    def add_listener(
            self,
            key: Input,
            callback: Callable,
            args: list[Any] = None,
            kwargs: dict[str, Any] = None,
            up: bool = False,
            condition: Callable = None,
            once: bool = False,
            repeat: bool = False,
            priority: int = 0,
            give_key: bool = False,
        ) -> Listener:
        """Ajoute un listener sur une entrée utilisateur

        Args:
            key: identifiant de l'événement
            callback: fonction à appeler
            args: arguments positionnels
            kwargs: arguments nommés
            up: déclenche au relâchement si True
            condition: condition booléenne
            once: supprime après première activation
            repeat: déclenche chaque frame tant que pressé
            priority: priorité d'exécution
            give_key: passe event_id en paramètre key au callback
        """
        if args is None: args = []
        if kwargs is None: kwargs = {}

        def _remove(l: Listener):
            lst = self._listeners.get(key)
            if lst and l in lst:
                lst.remove(l)
                if not lst:
                    del self._listeners[key]

        listener = Listener(
            callback, args, kwargs, priority, _remove,
            up=up, condition=condition, once=once,
            repeat=repeat, give_key=give_key,
        )

        if key not in self._listeners:
            self._listeners[key] = []
        self._insert_by_priority(self._listeners[key], listener)
        return listener

    def remove_listener(self, key: Input, callback: Callable) -> None:
        """Supprime un listener sur une entrée par callback

        Args:
            key: identifiant de l'événement
            callback: callback à supprimer
        """
        if key in self._listeners:
            for l in list(self._listeners[key]):
                if l.callback == callback:
                    l.invalidate()

    def when_any(
            self,
            callback: Callable,
            exclude: list[Input] = None,
            args: list[Any] = None,
            kwargs: dict[str, Any] = None,
            once: bool = False,
            condition: Callable = None,
            priority: int = 0,
            give_key: bool = False,
        ) -> Listener:
        """Déclenche le callback sur n'importe quelle pression sauf les exclusions

        Args:
            callback: fonction à appeler
            exclude: event_id à exclure
            args: arguments positionnels
            kwargs: arguments nommés
            once: supprime après première activation
            condition: condition booléenne
            priority: priorité d'exécution
            give_key: passe event_id en paramètre key
        """
        if exclude is None: exclude = []
        if args is None: args = []
        if kwargs is None: kwargs = {}

        def _remove(l: Listener):
            if l in self._any_listeners:
                self._any_listeners.remove(l)

        listener = Listener(
            callback, args, kwargs, priority, _remove,
            once=once, condition=condition,
            give_key=give_key, exclude=set(exclude),
        )

        self._insert_by_priority(self._any_listeners, listener)
        return listener

    def when_any_of(
            self,
            keys: list[Input],
            callback: Callable,
            args: list[Any] = None,
            kwargs: dict[str, Any] = None,
            up: bool = False,
            condition: Callable = None,
            once: bool = False,
            repeat: bool = False,
            priority: int = 0,
            give_key: bool = False,
        ) -> Listener:
        """Déclenche le callback si l'une des entrées est pressée

        Args:
            keys: entrées dont l'une doit être pressée
            callback: fonction à appeler
            args: arguments positionnels
            kwargs: arguments nommés
            up: déclenche au relâchement si True
            condition: condition booléenne
            once: supprime après première activation
            repeat: déclenche chaque frame tant que pressé
            priority: priorité d'exécution
            give_key: passe event_id en paramètre key au callback
        """
        if args is None: args = []
        if kwargs is None: kwargs = {}

        def _remove(l: Listener):
            if l in self._any_of_listeners:
                self._any_of_listeners.remove(l)

        listener = Listener(
            callback, args, kwargs, priority, _remove,
            up=up, condition=condition, once=once,
            repeat=repeat, give_key=give_key,
            any_of=set(keys),
        )

        self._insert_by_priority(self._any_of_listeners, listener)
        return listener

    def when_all_of(
            self,
            keys: list[Input],
            callback: Callable,
            args: list[Any] = None,
            kwargs: dict[str, Any] = None,
            once: bool = False,
            condition: Callable = None,
            repeat: bool = False,
            priority: int = 0,
        ) -> Listener:
        """Déclenche le callback quand toutes les entrées sont pressées simultanément

        Args:
            keys: entrées devant être pressées simultanément
            callback: fonction à appeler
            args: arguments positionnels
            kwargs: arguments nommés
            once: supprime après première activation
            condition: condition booléenne
            repeat: déclenche chaque frame tant que le combo est maintenu
            priority: priorité d'exécution
        """
        if args is None: args = []
        if kwargs is None: kwargs = {}

        def _remove(l: Listener):
            if l in self._all_of_listeners:
                self._all_of_listeners.remove(l)

        listener = Listener(
            callback, args, kwargs, priority, _remove,
            once=once, condition=condition,
            repeat=repeat, keys=set(keys),
        )
        self._insert_by_priority(self._all_of_listeners, listener)
        return listener

    def remove_callback(self, callback: Callable) -> None:
        """Supprime un callback de tous les types de listeners

        Args:
            callback: callback à supprimer partout
        """
        for lst in self._listeners.values():
            for l in list(lst):
                if l.callback == callback:
                    l.invalidate()

        for l in list(self._any_listeners):
            if l.callback == callback:
                l.invalidate()

        for l in list(self._any_of_listeners):
            if l.callback == callback:
                l.invalidate()

        for l in list(self._all_of_listeners):
            if l.callback == callback:
                l.invalidate()

    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation

        Args:
            dt: delta-time
        """
        # Repeat sur touches individuelles
        for event_id, listeners in list(self._listeners.items()):
            if not self._is_currently_pressed(event_id):
                continue
            for listener in list(listeners):
                if not listener.is_active(): continue
                if not listener.is_enabled(): continue
                if not listener.repeat: continue
                if listener.condition and not listener.condition(): continue
                listener._fire(event_id)

        # Repeat sur when_any_of
        for listener in list(self._any_of_listeners):
            if not listener.is_active(): continue
            if not listener.is_enabled(): continue
            if not listener.repeat: continue
            if not any(self._is_currently_pressed(k) for k in listener.any_of): continue
            if listener.condition and not listener.condition(): continue
            listener._fire()

        # Combos (when_all_of)
        for listener in list(self._all_of_listeners):
            if not listener.is_active(): continue
            if not listener.is_enabled(): continue
            if not all(self._is_currently_pressed(k) for k in listener.keys): continue
            if listener.condition and not listener.condition(): continue

            combo_key = frozenset(listener.keys)

            if listener.repeat:
                listener._fire()
            else:
                if combo_key not in self._triggered_combos:
                    listener._fire()
                    self._triggered_combos.add(combo_key)

    def flush(self) -> None:
        """Nettoie les états courants"""
        # Nettoie les combos qui ne sont plus maintenus
        self._triggered_combos = {combo for combo in self._triggered_combos if all(self._is_currently_pressed(k) for k in combo)}

    # ======================================== INTERNALS ========================================
    def _is_currently_pressed(self, event_id: int) -> bool:
        """Vérifie si une entrée est pressée cette frame ou maintenue

        Args:
            event_id: identifiant de l'entrée
        """
        return (
            self._ctx.key.is_pressed(event_id) or self._ctx.key.just_pressed(event_id) or
            self._ctx.mouse.is_pressed(event_id) or self._ctx.mouse.just_pressed(event_id)
        )

    def _on_press(self, event_id: int) -> None:
        """Traite une pression
        
        Args:
            event_id: identifiant de l'entrée
        """
        for listener in list(self._listeners.get(event_id, [])):
            if not listener.is_active(): continue
            if not listener.is_enabled(): continue
            if listener.up: continue
            if listener.repeat: continue
            if listener.condition and not listener.condition(): continue
            listener._fire(event_id)

        for listener in list(self._any_of_listeners):
            if not listener.is_active(): continue
            if not listener.is_enabled(): continue
            if event_id not in listener.any_of: continue
            if listener.up: continue
            if listener.repeat: continue
            if listener.condition and not listener.condition(): continue
            listener._fire(event_id)

        for listener in list(self._any_listeners):
            if not listener.is_active(): continue
            if not listener.is_enabled(): continue
            if event_id in listener.exclude: continue
            if listener.condition and not listener.condition(): continue
            listener._fire(event_id)

    def _on_release(self, event_id: int) -> None:
        """Traite un relâchement

        Args:
            event_id: identifiant de l'entrée        
        """
        for listener in list(self._listeners.get(event_id, [])):
            if not listener.is_active(): continue
            if not listener.is_enabled(): continue
            if not listener.up: continue
            if listener.condition and not listener.condition(): continue
            listener._fire(event_id)

        for listener in list(self._any_of_listeners):
            if not listener.is_active(): continue
            if not listener.is_enabled(): continue
            if event_id not in listener.any_of: continue
            if not listener.up: continue
            if listener.condition and not listener.condition(): continue
            listener._fire(event_id)

    def _on_mouse_press(self, x: float, y: float, button: int) -> None:
        """Pression d'un bouton souris

        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
            button: identifiant du bouton pressé
        """
        self._on_press(button)

    def _on_mouse_release(self, x: float, y: float, button: int) -> None:
        """Relâchement d'un bouton souris
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
            button: identifiant du bouton pressé
        """
        self._on_release(button)

    def _insert_by_priority(self, lst: list, listener: Listener) -> None:
        """Insère un listener dans une liste triée par priorité décroissante
        
        Args:
            lst: liste des listeners
            listener: listener à insérer
        """
        for i, l in enumerate(lst):
            if listener.priority > l.priority:
                lst.insert(i, listener)
                return
        lst.append(listener)

# ======================================== EXPORTS ========================================
__all__ = [
    "InputsManager",
    "Listener",
]