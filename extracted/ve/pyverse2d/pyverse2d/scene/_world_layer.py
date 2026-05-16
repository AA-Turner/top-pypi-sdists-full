# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, profile_section
from .._rendering import Pipeline, Camera

from ..world import World
from ..abc import Layer

# ======================================== LAYER ========================================
class WorldLayer(Layer):
    """Layer contenant un World

    Args:
        world: monde associé
        camera: caméra locale
    """
    def __init__(self, world: World, camera: Camera = None):
        # Initialisation du layer
        super().__init__(camera)

        # Vérifications
        if __debug__:
            expect(world, World)

        # Attributs publiques
        self._world: World = world
    
    # ======================================== PROPERTIES ========================================
    @property
    def world(self) -> World | None:
        """Monde associé"""
        return self._world

    @world.setter
    def world(self, value: World | None):
        if __debug__:
            expect(value, World)
        self._world = value

    # ======================================== HOOKS ========================================
    def on_start(self):
        """Activation du layer"""
        pass

    def on_stop(self):
        """Désactivation du layer"""
        pass

    # ======================================== LIFE CYCLE ========================================
    def _preload(self) -> None:
        """Préchargement"""
        pass

    @profile_section("scene.world_layer.update")
    def _update(self, dt: float):
        """Actualisation
        
        Args:
            dt: delta-time
        """
        self._world.update(dt)

    @profile_section("scene.world_layer.draw")
    def _draw(self, pipeline: Pipeline):
        """Affichage
        
        Args:
            pipeline: ``Pipeline``de rendu courant
        """
        self._world.draw(pipeline)

# ======================================== EXPORTS ========================================
__all__ = [
    "WorldLayer",
]