# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .._managers import CoordinatesManager, MouseManager
    from .._rendering import Pipeline
    from ..scene import Camera

# ======================================== ABSTRACT CLASS ========================================
class Layer(ABC):
    """Classe abstraite des layers
    
    Args:
        camera: caméra locale
    """
    __slots__ = ("_camera", "_active", "_visible")

    _IS_FX: bool = False

    _CAMERA_CLASS: Camera = None
    _COORDINATES: CoordinatesManager = None
    _MOUSE: MouseManager = None

    @classmethod
    def _get_camera_type(cls) -> Type[Camera]:
        """Renvoie le type ``Camera``"""
        if cls._CAMERA_CLASS is None:
            from .._rendering import Camera
            cls._CAMERA_CLASS = Camera
        return cls._CAMERA_CLASS
    
    @classmethod
    def _get_coordinates(cls) -> CoordinatesManager:
        """Renvoie le gestionnaire de coordonnées"""
        if cls._COORDINATES is None:
            from pyverse2d import coordinates
            cls._COORDINATES = coordinates
        return cls._COORDINATES
    
    @classmethod
    def _get_mouse(cls) -> MouseManager:
        """Renvoie le gestionnaire de la souris"""
        if cls._MOUSE is None:
            from pyverse2d import mouse
            cls._MOUSE = mouse
        return cls._MOUSE

    def __init__(self, camera: Camera = None):
        self._camera: Camera = expect(camera, (self._get_camera_type(), None))
        self._active: bool = True
        self._visible: bool = True

    # ======================================== PROPERTIES ========================================
    @property
    def camera(self) -> Camera:
        """Caméra clocale

        Si la caméra locale n'est pas définie, celle de la scène est utilisée.
        """
        return self._camera
    
    @camera.setter
    def camera(self, value: Camera) -> None:
        assert value is None or isinstance(value, self._get_camera_type()), f"camera ({value}) must be a Camera object"
        self._camera = value

    # ======================================== PREDICATES ========================================
    def is_fx(self) -> bool:
        """Vérifie que le layer soit un layer d'effets post-process"""
        return self._IS_FX
    
    # ======================================== ACTIVITY ========================================
    def is_active(self) -> bool:
        """Vérifie l'activité"""
        return self._active
    
    def activate(self) -> None:
        """Active le layer"""
        self._active = True

    def deactivate(self) -> None:
        """Désactive le layer"""
        self._active = False
    
    def switch_activity(self) -> None:
        """Bascule l'activité"""
        self._active = not self._active

    def set_activity(self, value: bool) -> None:
        """Fixe l'activité"""
        assert isinstance(value, bool), f"activity ({value}) must be a boolean"
        self._active = value

    # ======================================== VISIBILITY ========================================
    def is_visible(self) -> bool:
        """Vérifie la visibilité"""
        return self._visible
    
    def show(self) -> None:
        """Rend visible le layer"""
        self._visible = True

    def hide(self) -> None:
        """Rend invisible le layer"""
        self._visible = False

    def switch_visibility(self) -> None:
        """Bascule la visibilité"""
        self._visible = not self._visible

    def set_visibility(self, value: bool) -> None:
        """Fixe la visibilité"""
        assert isinstance(value, bool), f"visibility ({value}) must be a boolean"
        self._visible = value

    # ======================================== HOOKS ========================================
    @abstractmethod
    def on_start(self): ...

    @abstractmethod
    def on_stop(self): ...

    # ======================================== LIFE CYCLE ========================================
    @abstractmethod
    def _preload(self): ...

    @abstractmethod
    def _update(self, dt: float) -> None: ...

    def update(self, dt: float):
        """Actualisation
        
        Args:
            dt: delta-time
        """
        if self._camera is not None:
            self._camera.update(dt)
            self._apply_context()
        self._update(dt)
        self._clear_context()

    @abstractmethod
    def _draw(self, pipeline: Pipeline) -> None: ...

    def draw(self, pipeline: Pipeline) -> None:
        """Affichage global

        Args:
            pipeline: ``Pipeline`` de rendu
        """
        if self._camera is not None:
            self._apply_context()
        self._draw(pipeline)
        self._clear_context()

    # ======================================== INTERNALS ========================================
    def _apply_context(self) -> None:
        """Applique le contexte du layer"""
        coos = self._get_coordinates()
        coos.bind_temporary_camera(self._camera)
        coos.apply_context()
        self._get_mouse()._refresh_world_position()

    def _clear_context(self) -> None:
        """Nettoie le contexte du layer"""
        self._get_coordinates().unbind_temporary_camera()