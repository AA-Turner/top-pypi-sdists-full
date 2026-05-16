# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, profile_section, CallbackList
from .._flag import StackMode, SceneState
from .._rendering import Pipeline, Camera, Viewport
from .._managers import CoordinatesManager, MouseManager
from ..abc import Layer

from typing import Callable
import bisect

# ======================================== SCENE ========================================
class Scene:
    """Orchestre un ensemble de layers ordonnés par z_order

    Args:
        viewport: viewport de la scene
        camera: Camera principale de la scène
        stack_mode: mode d'empilement par rapport aux autres scenes
    """
    __slots__ = (
        "_viewport", "_camera", "_stack_mode",
        "_layers", "_z_orders",
        "_state",
        "_on_start", "_on_stop", "_on_update", "_on_draw",
    )

    def __init__(self, viewport: Viewport = None, camera: Camera = None, stack_mode: StackMode = StackMode.OVERLAY):
        # Transtypage et vérifications
        if __debug__:
            expect(viewport, (Viewport, None))
            expect(camera, (Camera, None))
            expect(stack_mode, StackMode)
        
        # Attributs publiques
        self._viewport: Viewport = viewport if viewport is not None else Viewport()
        self._camera: Camera = camera if camera is not None else Camera()
        self._stack_mode: StackMode = stack_mode

        # Layers
        self._layers: list[Layer] = []
        self._z_orders: list[int] = []

        # Etat
        self._state: SceneState = SceneState.SLEEPING
        
        # Hooks
        self._on_start: CallbackList = CallbackList()
        self._on_stop: CallbackList = CallbackList()
        self._on_update: CallbackList | None = None
        self._on_draw: CallbackList | None = None

        self.on_start(self._start)
        self.on_stop(self._stop)

    # ======================================== GETTERS ========================================
    @property
    def viewport(self) -> Viewport:
        """Viewport de rendu"""
        return self._viewport
    
    @viewport.setter
    def viewport(self, value: Viewport) -> None:
        if __debug__:
            expect(value, Viewport)
        self._viewport = value

    @property
    def camera(self) -> Camera:
        """Caméra principale"""
        return self._camera
    
    @camera.setter
    def camera(self, value: Camera) -> None:
        if __debug__:
            expect(value, Camera)
        self._camera = value

    @property
    def stack_mode(self) -> StackMode:
        """Mode d'empilement

        Le mode doit être un Enum ``StackMode``.
        """
        return self._stack_mode
    
    @stack_mode.setter
    def stack_mode(self, value: StackMode) -> None:
        if __debug__:
            expect(value, StackMode)
        self._stack_mode = value

    @property
    def state(self) -> SceneState:
        """Etat de la scène
        
        L'état doit être un Enum ``SceneState``.
        """
        return self._state

    # ======================================== LAYERS ========================================
    def add_layer(self, layer: Layer, z: int = 0) -> Scene:
        """Ajoute un layer à la scene

        Args:
            layer: layer à ajouter
            z: ordre de rendu
        """
        if __debug__:
            expect(layer, Layer)
        i = bisect.bisect_right(self._z_orders, z)
        self._z_orders.insert(i, z)
        self._layers.insert(i, layer)
        return self

    def remove_layer(self, layer: Layer) -> Scene:
        """Supprime un layer de la scene

        Args:
            layer: layer à supprimer
        """
        i = self._layers.index(expect(layer, Layer))
        self._layers.pop(i)
        self._z_orders.pop(i)
        return self
    
    def suspend(self):
        """Suspend tous les layers"""
        for layer in self._layers:
            layer.on_stop()

    # ======================================== HOOKS ========================================
    @property
    def on_start(self) -> CallbackList:
        """Hook d'activation"""
        if self._on_start is None:
            self._on_start = CallbackList()
        return self._on_start
    
    @property
    def on_stop(self) -> CallbackList:
        """Hook d'affichage"""
        if self._on_stop is None:
            self._on_stop = CallbackList()
        return self._on_stop

    @property
    def on_update(self) -> CallbackList:
        """Hook d'actualisation"""
        if self._on_update is None:
            self._on_update = CallbackList()
        return self._on_update

    @property
    def on_draw(self) -> CallbackList:
        """Hook d'affichage"""
        if self._on_draw is None:
            self._on_draw = CallbackList()
        return self._on_draw
    
    # ======================================== LIFE CYCLE ========================================
    def _preload(self, pipeline: Pipeline):
        """Préchargement"""
        for layer in self._layers:
            layer._preload()
        self.update(0.0)
        self.draw(pipeline)

    @profile_section("scene.update")
    def update(self, dt: float):
        """Actualisation"""
        self._camera.update(dt)
        self._apply_context()
        for layer in reversed(self._layers):
            if not layer.is_active():
                continue
            layer.update(dt)
        for fn in self._update_callbacks:
            fn(dt)
        self._clear_context()

    @profile_section("scene.draw")
    def draw(self, pipeline: Pipeline):
        """Affichage"""
        self._apply_context()
        pipeline.bind_scene(self)
        
        for layer in self._layers:
            if not layer.is_visible():
                continue

            pipeline.bind_layer(layer)
            pipeline.apply()

            layer.draw(pipeline)

            pipeline.flush()
        pipeline.end()

        for fn in self._draw_callbacks:
            fn()
        self._clear_context()

    # ======================================== INTERNALS ========================================
    def _set_state(self, value: SceneState) -> None:
        """Fixe l'état de la scène"""
        self._state = value

    def _start(self):
        """Démarre tous les layers"""
        for layer in self._layers:
            layer.on_start()

    def _stop(self):
        """Arrête tous les layers"""
        for layer in self._layers:
            layer.on_stop()

    def _apply_context(self) -> None:
        """Applique le contexte de la scène"""
        coord: CoordinatesManager = Pipeline.get_coord()
        coord.bind_viewport(self._viewport)
        coord.bind_camera(self._camera)

    def _clear_context(self) -> None:
        """Nettoie le contexte courant"""
        mouse: MouseManager = MouseManager.get_instance()
        mouse._clear_world_position()
        coord: CoordinatesManager = Pipeline.get_coord()
        coord.clear_context()

# ======================================== EXPORTS ========================================
__all__ = [
    "Scene",
]