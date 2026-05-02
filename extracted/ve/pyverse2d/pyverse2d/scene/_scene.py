# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
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
        "_layers", "_z_orders",
        "_viewport", "_camera",
        "_stack_mode", "_state",
        "_update_callbacks", "_draw_callbacks",
    )

    def __init__(self, viewport: Viewport = None, camera: Camera = None, stack_mode: StackMode = StackMode.OVERLAY):
        self._layers: list[Layer] = []
        self._z_orders: list[int] = []
        self._viewport: Viewport = expect(viewport, Viewport) if viewport else Viewport()
        self._camera: Camera = expect(camera, Camera) if camera else Camera((0, 0))
        self._stack_mode: StackMode = expect(stack_mode, StackMode)
        self._state: SceneState = SceneState.SLEEPING
        self._update_callbacks: list[Callable[[float], None]] = []
        self._draw_callbacks: list[Callable[[], None]] = []

    # ======================================== GETTERS ========================================
    @property
    def viewport(self) -> Viewport:
        """Viewport de rendu"""
        return self._viewport
    
    @viewport.setter
    def viewport(self, value: Viewport) -> None:
        self._viewport = expect(value, Viewport)

    @property
    def camera(self) -> Camera:
        """Caméra principale"""
        return self._camera
    
    @camera.setter
    def camera(self, value: Camera) -> None:
        self._camera = expect(value, Camera)

    @property
    def stack_mode(self) -> StackMode:
        """Mode d'empilement

        Le mode doit être un Enum ``StackMode``.
        """
        return self._stack_mode
    
    @stack_mode.setter
    def stack_mode(self, value: StackMode) -> None:
        self._stack_mode = expect(value, StackMode)

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
    def on_update(self, fn: Callable[[float], None]) -> Callable[[float], None]:
        """Enregistre un callback appelé à chaque update

        Args:
            fn: fonction prenant dt en paramètre
        """
        self._update_callbacks.append(fn)
        return fn

    def on_draw(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Enregistre un callback appelé à chaque draw, après les layers

        Args:
            fn: fonction prenant pipeline en paramètre
        """
        self._draw_callbacks.append(fn)
        return fn

    def on_start(self):
        """Démarre tous les layers"""
        for layer in self._layers:
            layer.on_start()

    def on_stop(self):
        """Arrête tous les layers"""
        for layer in self._layers:
            layer.on_stop()

    # ======================================== LIFE CYCLE ========================================
    def _preload(self, pipeline: Pipeline):
        """Préchargement"""
        for layer in self._layers:
            layer._preload()
        self.update(0.0)
        self.draw(pipeline)

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