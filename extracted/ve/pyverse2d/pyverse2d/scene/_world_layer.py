# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, profile_section
from .._rendering import Pipeline, Camera

from ..world import World, RenderSystem
from ..abc import Layer

# ======================================== LAYER ========================================
class WorldLayer(Layer):
    """Layer contenant un World

    Args:
        world: monde assigné
        camera: caméra locale
    """
    def __init__(self, world: World = None, camera: Camera = None):
        super().__init__(camera)
        self._world: World | None = expect(world, (World, None))
    
    # ======================================== PROPERTIES ========================================
    @property
    def world(self) -> World | None:
        """Monde associé"""
        return self._world

    @world.setter
    def world(self, value: World | None):
        self._world = expect(value, (World, None))

    # ======================================== HOOKS ========================================
    def on_start(self):
        """Activation du layer"""
        ...

    def on_stop(self):
        """Désactivation du layer"""
        ...

    # ======================================== LIFE CYCLE ========================================
    def _preload(self) -> None:
        """Préchargement"""
        pass

    @profile_section("scene.world_layer.update")
    def _update(self, dt: float):
        """Actualisation du layer"""
        if self._world is not None:
            self._world.update(dt)

    @profile_section("scene.world_layer.draw")
    def _draw(self, pipeline: Pipeline):
        """Affichage du layer"""
        if self._world is not None:
            self._world.draw(pipeline)