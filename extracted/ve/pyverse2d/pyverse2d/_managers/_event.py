# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..abc import Manager

from ._context import ContextManager

from pyglet.window import Window as PygletWindow
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .._rendering import Window

# ======================================== MANAGER ========================================
class EventManager(Manager):
    """Gestionnaire des events pyglet"""
    __slots__ = (
        # Clavier
        "_on_key_press",
        "_on_key_release",
        "_on_text",
        "_on_text_motion",
        "_on_text_motion_select",
        # Souris
        "_on_mouse_press",
        "_on_mouse_release",
        "_on_mouse_motion",
        "_on_mouse_drag",
        "_on_mouse_scroll",
        "_on_mouse_enter",
        "_on_mouse_leave",
        # Fenêtre
        "_on_resize",
        "_on_close",
        "_on_activate",
        "_on_deactivate",
        "_on_show",
        "_on_hide",
        "_on_move",
    )

    _ID: str = "event"

    ConsumeFlag = object()

    def __init__(self, context_manager: ContextManager):
        # Initialisation du gestionnaire
        super().__init__(context_manager)

        # Clavier
        self._on_key_press = _EventSlot(self)
        self._on_key_release = _EventSlot(self)
        self._on_text = _EventSlot(self)
        self._on_text_motion = _EventSlot(self)
        self._on_text_motion_select = _EventSlot(self)

        # Souris
        self._on_mouse_press = _EventSlot(self)
        self._on_mouse_release = _EventSlot(self)
        self._on_mouse_motion = _EventSlot(self)
        self._on_mouse_drag = _EventSlot(self)
        self._on_mouse_scroll = _EventSlot(self)
        self._on_mouse_enter = _EventSlot(self)
        self._on_mouse_leave = _EventSlot(self)

        # Fenêtre
        self._on_resize = _EventSlot(self)
        self._on_close = _EventSlot(self)
        self._on_activate = _EventSlot(self)
        self._on_deactivate = _EventSlot(self)
        self._on_show = _EventSlot(self)
        self._on_hide = _EventSlot(self)
        self._on_move = _EventSlot(self)

    # ======================================== PROPERTIES ========================================
    # Clavier
    @property
    def on_key_press(self) -> _EventSlot:
        """Event de pression d'une touche"""
        return self._on_key_press

    @property
    def on_key_release(self) -> _EventSlot:
        """Event de relâchement d'une touche"""
        return self._on_key_release

    @property
    def on_text(self) -> _EventSlot:
        """Event de saisie de texte"""
        return self._on_text

    @property
    def on_text_motion(self) -> _EventSlot:
        """Event de navigation dans le texte"""
        return self._on_text_motion

    @property
    def on_text_motion_select(self) -> _EventSlot:
        """Event de sélection dans le texte"""
        return self._on_text_motion_select

    # Souris
    @property
    def on_mouse_press(self) -> _EventSlot:
        """Event de pression d'un bouton souris"""
        return self._on_mouse_press

    @property
    def on_mouse_release(self) -> _EventSlot:
        """Event de relâchement d'un bouton souris"""
        return self._on_mouse_release

    @property
    def on_mouse_motion(self) -> _EventSlot:
        """Event de déplacement de la souris"""
        return self._on_mouse_motion

    @property
    def on_mouse_drag(self) -> _EventSlot:
        """Event de glissement de la souris"""
        return self._on_mouse_drag

    @property
    def on_mouse_scroll(self) -> _EventSlot:
        """Event de défilement de la molette"""
        return self._on_mouse_scroll

    @property
    def on_mouse_enter(self) -> _EventSlot:
        """Event d'entrée de la souris dans la fenêtre"""
        return self._on_mouse_enter

    @property
    def on_mouse_leave(self) -> _EventSlot:
        """Event de sortie de la souris de la fenêtre"""
        return self._on_mouse_leave

    # Fenêtre
    @property
    def on_resize(self) -> _EventSlot:
        """Event de redimensionnement de la fenêtre"""
        return self._on_resize

    @property
    def on_close(self) -> _EventSlot:
        """Event de fermeture de la fenêtre"""
        return self._on_close

    @property
    def on_activate(self) -> _EventSlot:
        """Event d'activation de la fenêtre"""
        return self._on_activate

    @property
    def on_deactivate(self) -> _EventSlot:
        """Event de désactivation de la fenêtre"""
        return self._on_deactivate

    @property
    def on_show(self) -> _EventSlot:
        """Event d'affichage de la fenêtre"""
        return self._on_show

    @property
    def on_hide(self) -> _EventSlot:
        """Event de masquage de la fenêtre"""
        return self._on_hide

    @property
    def on_move(self) -> _EventSlot:
        """Event de déplacement de la fenêtre"""
        return self._on_move

    # ======================================== BIND WINDOW ========================================
    def bind(self, window: Window) -> None:
        """Lie le gestionnaire à une fenêtre pyglet

        Args:
            window: fenêtre à assigner
        """
        super().bind(window)
        pw: PygletWindow = window.native

        pw.push_handlers(
            # Clavier
            on_key_press=lambda symbol, modifiers: self._on_key_press.emit(symbol),
            on_key_release=lambda symbol, modifiers: self._on_key_release.emit(symbol),
            on_text=lambda text: self._on_text.emit(text),
            on_text_motion=lambda motion: self._on_text_motion.emit(motion),
            on_text_motion_select=lambda motion: self._on_text_motion_select.emit(motion),
        
            # Souris
            on_mouse_press=lambda x, y, button, modifiers: self._on_mouse_press.emit(x, y, button),
            on_mouse_release=lambda x, y, button, modifiers: self._on_mouse_release.emit(x, y, button),
            on_mouse_motion=lambda x, y, dx, dy: self._on_mouse_motion.emit(x, y, dx, dy),
            on_mouse_drag=lambda x, y, dx, dy, buttons, modifiers: self._on_mouse_drag.emit(x, y, dx, dy, buttons),
            on_mouse_scroll=lambda x, y, scroll_x, scroll_y: self._on_mouse_scroll.emit(x, y, scroll_x, scroll_y),
            on_mouse_enter=lambda x, y: self._on_mouse_enter.emit(x, y),
            on_mouse_leave=lambda x, y: self._on_mouse_leave.emit(x, y),
        
            # Fenêtre
            on_resize=lambda width, height: self._on_resize.emit(width, height),
            on_close=lambda: self._on_close.emit(),
            on_activate=lambda: self._on_activate.emit(),
            on_deactivate=lambda: self._on_deactivate.emit(),
            on_show=lambda: self._on_show.emit(),
            on_hide=lambda: self._on_hide.emit(),
            on_move=lambda x, y: self._on_move.emit(x, y),
        )
    
    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation"""
        pass

    def flush(self) -> None:
        """Nettoyage"""
        pass

# ======================================== SUBSCRIPTION ========================================
class _Subscription:
    """Abonnement à un event"""
    __slots__ = ("callback", "priority")

    def __init__(self, callback: Callable, priority: int):
        self.callback = callback
        self.priority = priority


class _EventSlot:
    """Slot d'un event avec priorité et consommation"""
    __slots__ = ("_subs", "_manager")

    def __init__(self, manager: EventManager):
        self._subs: list[_Subscription] = []
        self._manager = manager

    def __call__(self, callback: Callable, priority: int = 0) -> Callable:
        """Abonne un callback"""
        self.subscribe(callback, priority)
        return callback

    def subscribe(self, callback: Callable, priority: int = 0) -> None:
        """Abonne un callback"""
        sub = _Subscription(callback, priority)
        for i, s in enumerate(self._subs):
            if priority > s.priority:
                self._subs.insert(i, sub)
                return
        self._subs.append(sub)

    def unsubscribe(self, callback: Callable) -> None:
        """Désabonne un callback"""
        for s in self._subs:
            if s.callback == callback:
                self._subs.remove(s)
                return

    def emit(self, *args, **kwargs) -> None:
        """Déclenche l'event"""
        for sub in self._subs:
            result = sub.callback(*args, **kwargs)
            if result is self._manager.ConsumeFlag:
                break

# ======================================== EXPORTS ========================================
__all__ = [
    "EventManager",
]