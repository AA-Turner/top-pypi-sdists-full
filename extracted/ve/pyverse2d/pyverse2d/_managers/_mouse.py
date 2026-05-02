# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, clamped
from .._rendering import Camera, Viewport
from ..abc import Manager, MouseCursor
from ..asset import Image

from ._context import ContextManager

import pyglet
import pyglet.window.mouse as _mouse
from pyglet.window import Window as PygletWindow

from typing import TypeAlias, ClassVar, Type
from numbers import Real

# ======================================== CURSORS ========================================
class SystemMouseCursor(MouseCursor):
    """Curseur de souris système

    Args:
        cursor: identifiant ``SystemCursor``
    """
    __slots__ = ("_cursor",)

    def __init__(self, cursor: str = PygletWindow.CURSOR_DEFAULT):
        self._cursor: str = cursor

    def to_pyglet(self, window: PygletWindow) -> pyglet.window.MouseCursor:
        """Renvoie le curseur pyglet
        
        Args:
            window: fenêtre OS courante
        """
        return window.get_system_mouse_cursor(self._cursor)


class ImageMouseCursor(MouseCursor):
    """Curseur de souris basé sur une image

    Args:
        image: image du curseur
        anchor_x: point chaud horizontal [0, 1]
        anchor_y: point chaud vertical [0, 1]
        acceleration: rendu natif OS (sinon OpenGL)
    """
    __slots__ = ("_image", "_anchor_x", "_anchor_y", "_acceleration")

    def __init__(
        self,
        image: Image,
        anchor_x: Real = 0.0,
        anchor_y: Real = 0.0,
        acceleration: bool = False,
    ):
        self._image: Image = expect(image, Image)
        self._anchor_x: float = float(clamped(expect(anchor_x, Real)))
        self._anchor_y: float = float(clamped(expect(anchor_y, Real)))
        self._acceleration: bool = expect(acceleration, bool)

    def to_pyglet(self, window: PygletWindow) -> pyglet.window.ImageMouseCursor:
        """Renvoie le curseur pyglet
        
        Args:
            window: Fenêtre OS courante
        """
        raw = pyglet.image.load(self._image.path)
        hot_x = int(self._anchor_x * raw.width)
        hot_y = int((1.0 - self._anchor_y) * raw.height)
        return pyglet.window.ImageMouseCursor(raw, hot_x, hot_y, self._acceleration)

# ======================================== STR ========================================
_NAMES: dict[MouseManager.Button] = {
    _mouse.LEFT:   "Left Click",
    _mouse.RIGHT:  "Right Click",
    _mouse.MIDDLE: "Middle Click",
}

# ======================================== MANAGER ========================================
class MouseManager(Manager):
    """Gestionnaire de la souris"""
    __slots__ = (
        "_mouse_x", "_mouse_y", "_mouse_out", "_world_position",
        "_mouse_dx", "_mouse_dy",
        "_drag_dx", "_drag_dy",
        "_scroll_dx", "_scroll_dy",
        "_step", "_pressed", "_released_this_frame",
    )

    _ID: str = "mouse"

    # Alias
    Button: TypeAlias = int
    MouseCursor: TypeAlias = MouseCursor
    SystemCursor: TypeAlias = str | None

    # Boutons
    B_LEFT = _mouse.LEFT
    B_MIDDLE = _mouse.MIDDLE
    B_RIGHT = _mouse.RIGHT

    # Curseurs de souris
    SystemMouseCursor: ClassVar[Type[SystemCursor]] = SystemMouseCursor
    ImageMouseCursor: ClassVar[Type[ImageMouseCursor]] = ImageMouseCursor

    # Flags des curseurs système
    CURSOR_DEFAULT = PygletWindow.CURSOR_DEFAULT
    CURSOR_CROSSHAIR = PygletWindow.CURSOR_CROSSHAIR
    CURSOR_HAND = PygletWindow.CURSOR_HAND
    CURSOR_HELP = PygletWindow.CURSOR_HELP
    CURSOR_NO = PygletWindow.CURSOR_NO
    CURSOR_SIZE = PygletWindow.CURSOR_SIZE
    CURSOR_SIZE_UP = PygletWindow.CURSOR_SIZE_UP
    CURSOR_SIZE_UP_RIGHT = PygletWindow.CURSOR_SIZE_UP_RIGHT
    CURSOR_SIZE_RIGHT = PygletWindow.CURSOR_SIZE_RIGHT
    CURSOR_SIZE_DOWN_RIGHT = PygletWindow.CURSOR_SIZE_DOWN_RIGHT
    CURSOR_SIZE_DOWN = PygletWindow.CURSOR_SIZE_DOWN
    CURSOR_SIZE_DOWN_LEFT = PygletWindow.CURSOR_SIZE_DOWN_LEFT
    CURSOR_SIZE_LEFT = PygletWindow.CURSOR_SIZE_LEFT
    CURSOR_SIZE_UP_LEFT = PygletWindow.CURSOR_SIZE_UP_LEFT
    CURSOR_SIZE_UP_DOWN = PygletWindow.CURSOR_SIZE_UP_DOWN
    CURSOR_SIZE_LEFT_RIGHT = PygletWindow.CURSOR_SIZE_LEFT_RIGHT
    CURSOR_TEXT = PygletWindow.CURSOR_TEXT
    CURSOR_WAIT = PygletWindow.CURSOR_WAIT
    CURSOR_WAIT_ARROW = PygletWindow.CURSOR_WAIT_ARROW

    def __init__(self, context_manager: ContextManager):
        # Initialisation du gestionnaire
        super().__init__(context_manager)

        # Position
        self._mouse_x: float = 0.0
        self._mouse_y: float = 0.0
        self._mouse_out: bool = False
        self._world_position: tuple[float, float] = None

        # Deltas
        self._mouse_dx: float = 0.0
        self._mouse_dy: float = 0.0
        self._drag_dx: float = 0.0
        self._drag_dy: float = 0.0
        self._scroll_dx: float = 0.0
        self._scroll_dy: float = 0.0

        # Boutons
        self._step: list[MouseManager.Button] = []
        self._pressed: dict[MouseManager.Button, bool] = {}
        self._released_this_frame: list[MouseManager.Button] = []

        # Abonnements
        self._ctx.event.on_mouse_motion(self._on_motion)
        self._ctx.event.on_mouse_drag(self._on_drag)
        self._ctx.event.on_mouse_press(self._on_press)
        self._ctx.event.on_mouse_release(self._on_release)
        self._ctx.event.on_mouse_enter(self._on_enter)
        self._ctx.event.on_mouse_leave(self._on_leave)
        self._ctx.event.on_mouse_scroll(self._on_scroll)

    # ======================================== BUTTONS ========================================
    @staticmethod
    def name(button: Button) -> str:
        """Renvoie le ``str`` d'un bouton
        
        Args:
            button: identifiant du bouton
        """
        return _NAMES.get(button, "Unknown")

    # ======================================== PROPERTIES ========================================
    @property
    def raw_position(self) -> tuple[float, float]:
        """Position de la souris dans la fenêtre OS"""
        return self._mouse_x  * self._window.physical_scale, self._mouse_y * self._window.physical_scale
    
    @property
    def raw_x(self) -> float:
        """Position horizontale de la souris dans la fenêtre OS"""
        return self._mouse_x * self._window.physical_scale
    
    @property
    def raw_y(self) -> float:
        """Position verticale de la souris dans la fenêtre OS"""
        return self._mouse_y * self._window.physical_scale

    @property
    def position(self) -> tuple[float, float]:
        """Position de la souris dans ``LogicalScreen``"""
        return self._mouse_x, self._mouse_y

    @property
    def x(self) -> float:
        """Position horizontale de la souris dans ``LogicalScreen``"""
        return self._mouse_x

    @property
    def y(self) -> float:
        """Position verticale de la souris dans ``LogicalScreen``"""
        return self._mouse_y
    
    @property
    def motion(self) -> tuple[float, float]:
        """Déplacement de la souris"""
        return self._mouse_dx, self._mouse_dy

    @property
    def dx(self) -> float:
        """Déplacement horizontal de la souris"""
        return self._mouse_dx

    @property
    def dy(self) -> float:
        """Déplacement vertical de la souris"""
        return self._mouse_dy
    
    @property
    def drag(self) -> tuple[float, float]:
        """Glissement lors du maintien"""
        return self._drag_dx, self._drag_dy

    @property
    def drag_dx(self) -> float:
        """Glissement horizontal lors d'un maintien"""
        return self._drag_dx

    @property
    def drag_dy(self) -> float:
        """Glissement vertical lors d'un maintien"""
        return self._drag_dy
    
    @property
    def scroll(self) -> tuple[float, float]:
        """Défilement de la molette cette frame"""
        return self._scroll_dx, self._scroll_dy

    @property
    def scroll_x(self) -> float:
        """Défilement horizontal de la molette cette frame"""
        return self._scroll_dx

    @property
    def scroll_y(self) -> float:
        """Défilement vertical de la molette cette frame"""
        return self._scroll_dy
    
    # ======================================== GETTERS ========================================
    def get_world_position(self, viewport: Viewport = None, camera: Camera = None) -> tuple[float, float]:
        """Renvoie la position monde du curseur
        
        Args:
            viewport: viewport du monde
            camera: camera du monde
        """
        if self._world_position is None:
            return self._ctx.coordinates.logical_to_world(self._mouse_x, self._mouse_y, viewport=viewport, camera=camera)
        return self._world_position
    
    # ======================================== SETTERS ========================================
    def set_exclusive(self, value: bool) -> None:
        """Active ou désactive le mode exclusif de la souris"""
        self._window.native.set_exclusive_mouse(value)

    def set_appearance(self, cursor: MouseCursor) -> None:
        """Définit l'apparence du curseur"""
        assert isinstance(cursor, MouseCursor), f"Cursor must be a MouseCursor instance, not a {type(cursor)}"
        self._window.native.set_mouse_cursor(cursor.to_pyglet(self._window.native))

    # ======================================== PREDICATES ========================================
    def is_out(self) -> bool:
        """Vérifie si la souris est hors du canvas"""
        return self._mouse_out
    
    def is_pressed(self, button: Button) -> bool:
        """Vérifie si un bouton est maintenu enfoncé
        
        Args:
            button: identifiant du bouton
        """
        return self._pressed.get(button, False)

    def just_pressed(self, button: Button) -> bool:
        """Vérifie si un bouton vient d'être pressé cette frame
        
        Args:
            button: identifiant du bouton
        """
        return button in self._step

    def just_released(self, button: Button) -> bool:
        """Vérifie si un bouton vient d'être relâché cette frame
        
        Args:
            button: identifiant du bouton
        """
        return button in self._released_this_frame

    def is_currently_pressed(self, button: Button) -> bool:
        """Vérifie si un bouton est pressé cette frame ou maintenu
        
        Args:
            button: identifiant du bouton
        """
        return self._pressed.get(button, False) or button in self._step
        
    # ======================================== HOOKS ========================================
    def _on_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """Déplacement de la souris
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
            dx: déplacement horizontal
            dy: déplacement vertical
        """
        self._compute_position(x, y)
        self._check_out()
        self._mouse_dx = dx * self._window.width / self._window.screen.width
        self._mouse_dy = dy * self._window.height / self._window.screen.height

    def _on_drag(self, x: float, y: float, dx: float, dy: float, buttons: int) -> None:
        """Glissement lors du maintien
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
            dx: déplacement horizontal
            dy: déplacement vertical
        """
        self._compute_position(x, y)
        self._check_out()
        self._drag_dx = dx * self._window.width / self._window.screen.width
        self._drag_dy = dy * self._window.height / self._window.screen.height

    def _on_press(self, x: float, y: float, button: int) -> None:
        """Pression d'un bouton
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
            button: identifiant du bouton
        """
        self._compute_position(x, y)
        self._check_out()

    def _on_release(self, x: float, y: float, button: int) -> None:
        """Relachement d'un bouton
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
            button: identifiant du bouton
        """
        self._compute_position(x, y)
        self._check_out()

    def _on_enter(self, x: float, y: float) -> None:
        """Entrée dans la fenêtre
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
        """
        self._compute_position(x, y)
        self._check_out()

    def _on_leave(self, x: float, y: float) -> None:
        """Sortie de la fenêtre
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
        """
        self._compute_position(x, y)
        self._mouse_out = True

    def _on_scroll(self, x: float, y: float, scroll_x: float, scroll_y: float) -> None:
        """Défilement de la molette
        
        Args:
            x: coordonnée horizontale
            y: coordonnée verticale
            scroll_x: défilement horizontal
            scroll_y: défilement vertical
        """
        self._scroll_dx = scroll_x
        self._scroll_dy = scroll_y

    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        pass

    def flush(self) -> None:
        """Nettoyage"""
        self._mouse_dx = 0.0
        self._mouse_dy = 0.0
        self._drag_dx = 0.0
        self._drag_dy = 0.0
        self._scroll_dx = 0.0
        self._scroll_dy = 0.0
        for button in self._step:
            if button not in self._released_this_frame:
                self._pressed[button] = True
        self._step.clear()
        self._released_this_frame.clear()

    # ======================================== INTERNALS ========================================
    def _compute_position(self, x: float, y: float) -> None:
        """Convertit les coordonnnées OS en coordonnées logiques
        
        Args:
            x: coordonnée horizontale OS
            y: coordonnée verticale OS
        """
        self._mouse_x, self._mouse_y = self._window.window_to_screen(x, y)

    def _check_out(self) -> None:
        """Vérifie que la souris soit en dehors du canas de la fenêtre"""
        hw, hh = self._window.screen.half_width, self._window.screen.half_height
        self._mouse_out = not (-hw <= self._mouse_x <= hw and -hh <= self._mouse_y <= hh)

    def _refresh_world_position(self) -> None:
        """Actualise la position monde"""
        self._world_position = self._ctx.coordinates.framebuffer_to_world(self._mouse_x, self._mouse_y)

    def _clear_world_position(self) -> None:
        """Nettoie la position monde"""
        self._world_position = None

# ======================================== EXPORTS ========================================
__all__ = [
    "SystemMouseCursor",
    "ImageMouseCursor",
    
    "MouseManager",
]